pub mod entity;
pub mod error;
pub mod parser;

#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use pyo3::types::{PyBytes, PyDict};

#[cfg(feature = "python")]
#[pymodule]
fn pvf_parser_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(save_parquet, m)?)?;
    m.add_function(wrap_pyfunction!(detect_encoding, m)?)?;
    m.add_class::<PvfArchive>()?;
    Ok(())
}

#[cfg(feature = "python")]
fn parse_encoding(encoding: i32) -> PyResult<crate::parser::pvf_encoding::PVFEncoding> {
    use crate::parser::pvf_encoding::PVFEncoding;
    match encoding {
        1 => Ok(PVFEncoding::BIG5),
        2 => Ok(PVFEncoding::GBK),
        other => Err(pyo3::exceptions::PyValueError::new_err(format!(
            "invalid pvf encoding {other}: expected 1 (BIG5) or 2 (GBK)"
        ))),
    }
}

/// Build every parquet cache from `fp` and return per-dataset row counts.
///
/// `progress`, when given, is called as `progress(stage: str, done: int, total: int)`
/// after every dataset so the UI can show what is going on.
#[cfg(feature = "python")]
#[pyfunction]
#[pyo3(signature = (fp, encoding, output_dir, progress = None))]
fn save_parquet(
    py: Python<'_>,
    fp: &str,
    encoding: i32,
    output_dir: &str,
    progress: Option<Py<PyAny>>,
) -> PyResult<Py<PyDict>> {
    use crate::parser::pvf_reader::{
        PVFReader, save_dungeon_to_parquet, save_equipment_to_parquet, save_exp_to_parquet,
        save_magic_seal_to_parquet, save_quest_to_parquet, save_skill_to_parquet,
        save_stackable_to_parquet,
    };
    use std::path::PathBuf;

    tracing_subscriber::fmt().try_init().ok();

    let encoding = parse_encoding(encoding)?;
    let output_dir = PathBuf::from(output_dir);
    std::fs::create_dir_all(&output_dir)?;

    let mut reader = PVFReader::open(fp, encoding)?;

    let counts = PyDict::new(py);
    counts.set_item("uuid", reader.uuid().to_string())?;
    counts.set_item("version", reader.version())?;
    counts.set_item("files", reader.file_count())?;

    const TOTAL: u32 = 7;
    let mut done = 0u32;

    macro_rules! stage {
        ($name:literal, $get:expr, $save:expr, $file:literal) => {{
            let items = py.detach($get);
            let count = items.len();
            $save(items, output_dir.join($file));
            counts.set_item($name, count)?;
            done += 1;
            if let Some(callback) = &progress {
                callback.call1(py, ($name, done, TOTAL))?;
            }
        }};
    }

    stage!(
        "equipment",
        || reader.get_equipment_list(),
        save_equipment_to_parquet,
        "equipments.parquet"
    );
    stage!(
        "stackable",
        || reader.get_stackable_list(),
        save_stackable_to_parquet,
        "stackables.parquet"
    );
    stage!(
        "quest",
        || reader.get_quest_list(),
        save_quest_to_parquet,
        "quests.parquet"
    );
    stage!(
        "dungeon",
        || reader.get_dungeon_list(),
        save_dungeon_to_parquet,
        "dungeons.parquet"
    );
    stage!(
        "skill",
        || reader.get_skill_list(),
        save_skill_to_parquet,
        "skills.parquet"
    );
    stage!(
        "exp",
        || reader.get_exp_list(),
        save_exp_to_parquet,
        "exps.parquet"
    );
    stage!(
        "magic_seal",
        || reader.get_magic_seal_list(),
        save_magic_seal_to_parquet,
        "magic_seals.parquet"
    );

    Ok(counts.unbind())
}

/// Guess whether an archive stores BIG5 or GBK text. Returns 1 or 2.
#[cfg(feature = "python")]
#[pyfunction]
fn detect_encoding(fp: &str) -> PyResult<i32> {
    use crate::parser::pvf_encoding::PVFEncoding;
    use crate::parser::pvf_reader::PVFReader;
    use crate::parser::utils::guess_encoding;

    let reader = PVFReader::open(fp, PVFEncoding::GBK)?;

    let mut samples = Vec::new();
    // dictionaries hold the actual Chinese text of an archive
    for path in reader.list_files("", ".str", Some(3)) {
        if let Ok(buf) = reader.read_file(&path) {
            samples.push(buf);
        }
    }
    if samples.is_empty()
        && let Ok(buf) = reader.read_file("stringtable.bin")
    {
        samples.push(buf);
    }

    Ok(guess_encoding(&samples) as i32)
}

/// Read-only view of a `Script.pvf` archive.
#[cfg(feature = "python")]
#[pyclass]
struct PvfArchive {
    reader: crate::parser::pvf_reader::PVFReader,
}

#[cfg(feature = "python")]
#[pymethods]
impl PvfArchive {
    #[new]
    #[pyo3(signature = (path, encoding = 2))]
    fn new(path: &str, encoding: i32) -> PyResult<Self> {
        let encoding = parse_encoding(encoding)?;
        Ok(Self {
            reader: crate::parser::pvf_reader::PVFReader::open(path, encoding)?,
        })
    }

    #[getter]
    fn uuid(&self) -> &str {
        self.reader.uuid()
    }

    #[getter]
    fn version(&self) -> u32 {
        self.reader.version()
    }

    #[getter]
    fn encoding(&self) -> i32 {
        self.reader.encoding() as i32
    }

    #[getter]
    fn file_count(&self) -> usize {
        self.reader.file_count()
    }

    /// `{uuid, version, files, bytes, directories, by_suffix}`.
    fn stats(&self, py: Python<'_>) -> PyResult<Py<PyDict>> {
        let stats = self.reader.stats();
        let dict = PyDict::new(py);
        dict.set_item("uuid", stats.uuid)?;
        dict.set_item("version", stats.version)?;
        dict.set_item("files", stats.files)?;
        dict.set_item("bytes", stats.bytes)?;
        dict.set_item("directories", stats.directories)?;
        dict.set_item("by_suffix", stats.by_suffix)?;
        Ok(dict.unbind())
    }

    #[pyo3(signature = (prefix = "", suffix = "", limit = None))]
    fn list_files(&self, prefix: &str, suffix: &str, limit: Option<usize>) -> Vec<String> {
        self.reader.list_files(prefix, suffix, limit)
    }

    fn directories(&self) -> Vec<String> {
        self.reader.directories()
    }

    fn exists(&self, path: &str) -> bool {
        self.reader.exists(path)
    }

    /// Raw (decrypted) content of one file.
    fn read_file<'py>(&mut self, py: Python<'py>, path: &str) -> PyResult<Bound<'py, PyBytes>> {
        let buf = self.reader.read_file(path)?;
        Ok(PyBytes::new(py, &buf))
    }

    /// Content of one file decoded as text.
    fn read_text(&mut self, path: &str) -> PyResult<String> {
        Ok(self.reader.read_file_as_text(path)?)
    }

    /// `[(kind, value)]` tokens of one file, for exploration.
    fn tokens(&mut self, path: &str) -> PyResult<Vec<(String, String)>> {
        use crate::parser::binary_item::BinaryItem;

        let items = self.reader.read_file_as_list(path)?;
        Ok(items
            .iter()
            .map(|item| {
                let kind = match item {
                    BinaryItem::Int(_) => "int",
                    BinaryItem::UInt(_) => "uint",
                    BinaryItem::Float(_) => "float",
                    BinaryItem::String(_) => "string",
                    BinaryItem::Segment(_) => "segment",
                };
                (kind.to_string(), item.to_display_string())
            })
            .collect())
    }

    /// `[(tag, value)]` view of one file.
    fn entries(&mut self, path: &str) -> PyResult<Vec<(String, String)>> {
        Ok(self.reader.read_file_as_dict(path)?)
    }

    fn search_strings(&mut self, needle: &str, limit: Option<usize>) -> Vec<(u32, String)> {
        self.reader.search_strings(needle, limit)
    }

    #[pyo3(signature = (dest, prefix = "", suffix = ""))]
    fn extract_all(&mut self, dest: &str, prefix: &str, suffix: &str) -> (usize, Vec<String>) {
        let report = self.reader.extract_all(dest, prefix, suffix);
        (report.files, report.failed)
    }

    fn __len__(&self) -> usize {
        self.reader.file_count()
    }

    fn __repr__(&self) -> String {
        format!(
            "<PvfArchive {} files={} encoding={}>",
            self.reader.uuid(),
            self.reader.file_count(),
            self.reader.encoding().label()
        )
    }
}
