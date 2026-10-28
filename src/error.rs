//! Error type shared by every parser in this crate.
//!
//! The parser used to `panic!`/`unwrap()` on malformed input, which is fatal
//! when the crate is used as a PyO3 extension: a Rust panic surfaces in Python
//! as `pyo3_runtime.PanicException`, a `BaseException` that `except Exception`
//! does not catch.  Everything that can fail now returns [`PvfError`] instead.

use std::fmt;

/// Result alias used across the crate.
pub type PvfResult<T> = Result<T, PvfError>;

#[derive(Debug)]
pub enum PvfError {
    /// The underlying file could not be read.
    Io(std::io::Error),
    /// The file is not a Script.pvf archive (bad header, bad magic, ...).
    Format(String),
    /// A structure points past the end of the file.
    Truncated {
        what: &'static str,
        expected: usize,
        actual: usize,
    },
    /// The requested entry does not exist in the archive.
    FileNotFound(String),
    /// The payload cannot be decoded with the configured encoding.
    Encoding(String),
    /// A string table reference is out of range.
    StringTable { index: u32, count: u32 },
    /// A token stream is malformed (unknown type byte, truncated token, ...).
    Token { offset: usize, reason: String },
}

impl PvfError {
    pub fn format(message: impl Into<String>) -> Self {
        PvfError::Format(message.into())
    }

    pub fn token(offset: usize, reason: impl Into<String>) -> Self {
        PvfError::Token {
            offset,
            reason: reason.into(),
        }
    }
}

impl fmt::Display for PvfError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PvfError::Io(err) => write!(f, "io error: {err}"),
            PvfError::Format(message) => write!(f, "invalid pvf: {message}"),
            PvfError::Truncated {
                what,
                expected,
                actual,
            } => write!(
                f,
                "truncated {what}: expected {expected} bytes, got {actual}"
            ),
            PvfError::FileNotFound(path) => write!(f, "file not found in pvf: {path}"),
            PvfError::Encoding(message) => write!(f, "encoding error: {message}"),
            PvfError::StringTable { index, count } => write!(
                f,
                "string index {index} out of range (string table holds {count} entries)"
            ),
            PvfError::Token { offset, reason } => {
                write!(f, "invalid token at offset {offset}: {reason}")
            }
        }
    }
}

impl std::error::Error for PvfError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            PvfError::Io(err) => Some(err),
            _ => None,
        }
    }
}

impl From<std::io::Error> for PvfError {
    fn from(err: std::io::Error) -> Self {
        PvfError::Io(err)
    }
}

#[cfg(feature = "python")]
impl From<PvfError> for pyo3::PyErr {
    fn from(err: PvfError) -> Self {
        pyo3::exceptions::PyValueError::new_err(err.to_string())
    }
}
