//! Inspect a `Script.pvf` archive from the command line.
//!
//! ```text
//! pvf_dump info
//! pvf_dump --pvf /path/to/Script.pvf list --prefix equipment/ --suffix .equ --limit 20
//! pvf_dump tokens equipment/equipment.lst
//! pvf_dump entries n_quest/alphraira/darkelfcemetary/epic_39_darkelfcemetary_drake_1.qst
//! pvf_dump search 太刀 --limit 5
//! pvf_dump extract /tmp/pvf --suffix .lst
//! ```
//!
//! The archive path defaults to `Script.pvf` in the current directory and can
//! be overridden with the global `--pvf` flag, which works before or after the
//! subcommand.

use clap::{Parser, Subcommand, ValueEnum};
use pvf_parser_rs::error::PvfError;
use pvf_parser_rs::parser::binary_item::BinaryItem;
use pvf_parser_rs::parser::pvf_encoding::PVFEncoding;
use pvf_parser_rs::parser::pvf_reader::PVFReader;
use std::path::{Path, PathBuf};
use std::process::ExitCode;

/// Anything that can go wrong is reported through `Box<dyn Error>`, so `?`
/// works for both [`PvfError`] and the formatted messages below.
type Outcome = Result<(), Box<dyn std::error::Error>>;

/// Inspect a `Script.pvf` archive.
#[derive(Parser, Debug)]
#[command(
    name = "pvf_dump",
    version,
    about = "Inspect a Script.pvf archive",
    after_help = "Examples:
  pvf_dump info
  pvf_dump list --prefix equipment/ --suffix .equ --limit 20
  pvf_dump tokens equipment/equipment.lst
  pvf_dump read equipment/equipment.lst --hex --limit 8
  pvf_dump search 太刀 --limit 5
  pvf_dump extract /tmp/pvf --suffix .lst"
)]
struct Cli {
    /// Path to the archive.
    #[arg(
        short,
        long,
        global = true,
        value_name = "ARCHIVE",
        help_heading = "Archive",
        default_value = "Script.pvf"
    )]
    pvf: PathBuf,

    /// Text encoding of the archive.
    #[arg(
        short,
        long,
        global = true,
        value_enum,
        help_heading = "Archive",
        default_value_t = Encoding::Gbk
    )]
    encoding: Encoding,

    #[command(subcommand)]
    command: Command,
}

/// Encoding of the Chinese text stored in the archive.
///
/// The traditional (`BIG5`) and simplified (`GBK`) clients ship different
/// archives; the number aliases keep the old `--encoding 1|2` calls working.
#[derive(Copy, Clone, Debug, PartialEq, Eq, ValueEnum)]
enum Encoding {
    /// Simplified Chinese client.
    #[value(alias = "2")]
    Gbk,
    /// Traditional Chinese client.
    #[value(alias = "1")]
    Big5,
}

impl From<Encoding> for PVFEncoding {
    fn from(value: Encoding) -> Self {
        match value {
            Encoding::Gbk => PVFEncoding::GBK,
            Encoding::Big5 => PVFEncoding::BIG5,
        }
    }
}

#[derive(Subcommand, Debug)]
enum Command {
    /// Show archive statistics (uuid, version, size, file count per suffix).
    Info,

    /// List file paths, optionally filtered by prefix and suffix.
    List {
        /// Only keep paths starting with this prefix.
        #[arg(long, value_name = "PREFIX", default_value = "")]
        prefix: String,

        /// Only keep paths ending with this suffix (".equ", ".lst", ...).
        #[arg(long, value_name = "SUFFIX", default_value = "")]
        suffix: String,

        /// Stop after N paths.
        #[arg(short, long, value_name = "N")]
        limit: Option<usize>,
    },

    /// Print one file: tokens by default, raw bytes with --hex, text with --text.
    Read {
        /// Path inside the archive, e.g. `equipment/equipment.lst`.
        path: String,

        /// Dump the raw decrypted bytes as a hex dump.
        #[arg(long, conflicts_with = "text")]
        hex: bool,

        /// Decode the file with its own encoding and print it.
        #[arg(long)]
        text: bool,

        /// Stop after N hex lines or N tokens.
        #[arg(short, long, value_name = "N")]
        limit: Option<usize>,
    },

    /// Print the token stream of one file with type names.
    Tokens {
        /// Path inside the archive.
        path: String,

        /// Stop after N tokens.
        #[arg(short, long, value_name = "N")]
        limit: Option<usize>,
    },

    /// Print one file as `[tag] = value` pairs.
    Entries {
        /// Path inside the archive, e.g. a `.qst` or `.equ` file.
        path: String,
    },

    /// Search the string table and the `*.str` dictionaries.
    Search {
        /// Text to look for.
        needle: String,

        /// Stop after N matches.
        #[arg(short, long, value_name = "N")]
        limit: Option<usize>,
    },

    /// Print string table entries starting at an index.
    String {
        /// First string index to print.
        index: u32,

        /// How many consecutive entries to print.
        #[arg(short, long, value_name = "N", default_value_t = 3)]
        count: u32,
    },

    /// Extract matching files to a directory.
    Extract {
        /// Destination directory.
        dest: PathBuf,

        /// Only extract paths starting with this prefix.
        #[arg(long, value_name = "PREFIX", default_value = "")]
        prefix: String,

        /// Only extract paths ending with this suffix.
        #[arg(long, value_name = "SUFFIX", default_value = "")]
        suffix: String,
    },
}

fn main() -> ExitCode {
    let cli = Cli::parse();

    match run(cli) {
        Ok(()) => ExitCode::SUCCESS,
        Err(err) => {
            eprintln!("error: {err}");
            ExitCode::FAILURE
        }
    }
}

fn run(cli: Cli) -> Outcome {
    let mut reader = PVFReader::open(&cli.pvf, cli.encoding.into()).map_err(|err| match err {
        // `FileNotFound` normally means "no such entry inside the archive"; when
        // it comes from `open` it is the archive itself that is missing.
        PvfError::FileNotFound(_) => format!("archive not found: {}", cli.pvf.display()),
        other => format!("cannot open {}: {other}", cli.pvf.display()),
    })?;

    match cli.command {
        Command::Info => info(&reader, &cli.pvf),
        Command::List {
            prefix,
            suffix,
            limit,
        } => list(&reader, &prefix, &suffix, limit),
        Command::Read {
            path,
            hex,
            text,
            limit,
        } => read(&mut reader, &path, hex, text, limit),
        Command::Tokens { path, limit } => tokens(&mut reader, &path, limit),
        Command::Entries { path } => entries(&mut reader, &path),
        Command::Search { needle, limit } => search(&mut reader, &needle, limit),
        Command::String { index, count } => strings(&mut reader, index, count),
        Command::Extract {
            dest,
            prefix,
            suffix,
        } => extract(&mut reader, &dest, &prefix, &suffix),
    }
}

fn info(reader: &PVFReader, pvf: &Path) -> Outcome {
    let stats = reader.stats();

    println!("archive     : {}", pvf.display());
    println!("uuid        : {}", stats.uuid);
    println!("version     : {}", stats.version);
    println!("files       : {}", stats.files);
    println!("bytes       : {}", stats.bytes);
    println!("directories : {}", stats.directories);
    println!("encoding    : {}", reader.encoding().label());
    println!("suffixes    :");

    for (suffix, count) in &stats.by_suffix {
        println!(
            "  {:<8} {count}",
            if suffix.is_empty() { "-" } else { suffix }
        );
    }

    Ok(())
}

fn list(reader: &PVFReader, prefix: &str, suffix: &str, limit: Option<usize>) -> Outcome {
    for path in reader.list_files(prefix, suffix, limit) {
        println!("{path}");
    }
    Ok(())
}

fn read(
    reader: &mut PVFReader,
    path: &str,
    hex: bool,
    text: bool,
    limit: Option<usize>,
) -> Outcome {
    if hex {
        let bytes = reader.read_file(path)?;
        for (index, chunk) in bytes
            .chunks(16)
            .enumerate()
            .take(limit.unwrap_or(usize::MAX))
        {
            let hex = chunk
                .iter()
                .map(|byte| format!("{byte:02x}"))
                .collect::<Vec<_>>()
                .join(" ");
            println!("{:08x}  {hex}", index * 16);
        }
        return Ok(());
    }

    if text {
        print!("{}", reader.read_file_as_text(path)?);
        return Ok(());
    }

    for item in reader
        .read_file_as_list(path)?
        .iter()
        .take(limit.unwrap_or(usize::MAX))
    {
        println!("{}", item.to_display_string());
    }
    Ok(())
}

fn tokens(reader: &mut PVFReader, path: &str, limit: Option<usize>) -> Outcome {
    let items = reader.read_file_as_list(path)?;
    println!("{} tokens", items.len());

    for (index, item) in items.iter().take(limit.unwrap_or(usize::MAX)).enumerate() {
        let kind = match item {
            BinaryItem::Int(_) => "int    ",
            BinaryItem::UInt(_) => "uint   ",
            BinaryItem::Float(_) => "float  ",
            BinaryItem::String(_) => "string ",
            BinaryItem::Segment(_) => "segment",
        };
        println!("{index:5}  {kind}  {}", item.to_display_string());
    }
    Ok(())
}

fn entries(reader: &mut PVFReader, path: &str) -> Outcome {
    for (key, value) in reader.read_file_as_dict(path)? {
        println!("{key} = {value}");
    }
    Ok(())
}

/// Search the string table, then the `*.str` dictionaries.
///
/// The string table only stores keys (`name_780104`), so searching for visible
/// text has to look inside the dictionaries, which hold the `key>value` pairs.
fn search(reader: &mut PVFReader, needle: &str, limit: Option<usize>) -> Outcome {
    let limit = limit.unwrap_or(usize::MAX);
    let mut shown = 0usize;

    for (index, value) in reader.search_strings(needle, Some(limit)) {
        println!("string {index:8}  {value}");
        shown += 1;
        if shown >= limit {
            return Ok(());
        }
    }

    for path in reader.list_files("", ".str", None) {
        let Ok(text) = reader.read_file_as_text(&path) else {
            continue;
        };
        for line in text.lines() {
            if !line.contains(needle) {
                continue;
            }
            println!("{path}: {line}");
            shown += 1;
            if shown >= limit {
                return Ok(());
            }
        }
    }

    if shown == 0 {
        eprintln!("no match for {needle:?}");
    }
    Ok(())
}

fn strings(reader: &mut PVFReader, index: u32, count: u32) -> Outcome {
    let table = reader.string_table();

    for offset in 0..count {
        let current = index.saturating_add(offset);
        match table.try_get_item(current) {
            Ok(value) => println!("{current:8}  {value}"),
            Err(err) => println!("{current:8}  <{err}>"),
        }
    }
    Ok(())
}

fn extract(reader: &mut PVFReader, dest: &Path, prefix: &str, suffix: &str) -> Outcome {
    let report = reader.extract_all(dest, prefix, suffix);

    println!(
        "extracted {} files ({} failed)",
        report.files,
        report.failed.len()
    );

    for failed in report.failed.iter().take(10) {
        println!("  failed: {failed}");
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    /// Parse a command line the way `main` would.
    fn parse(args: &[&str]) -> Result<Cli, clap::Error> {
        Cli::try_parse_from(std::iter::once("pvf_dump").chain(args.iter().copied()))
    }

    #[test]
    fn archive_path_defaults_to_the_current_directory() {
        let cli = parse(&["info"]).unwrap();
        assert_eq!(cli.pvf, PathBuf::from("Script.pvf"));
        assert_eq!(cli.encoding, Encoding::Gbk);
        assert!(matches!(cli.command, Command::Info));
    }

    #[test]
    fn global_options_work_before_and_after_the_subcommand() {
        for args in [["-p", "/tmp/a.pvf", "info"], ["info", "-p", "/tmp/a.pvf"]] {
            let cli = parse(&args).unwrap();
            assert_eq!(cli.pvf, PathBuf::from("/tmp/a.pvf"));
        }
    }

    #[test]
    fn encoding_accepts_names_and_the_legacy_numbers() {
        assert_eq!(
            parse(&["-e", "big5", "info"]).unwrap().encoding,
            Encoding::Big5
        );
        assert_eq!(
            parse(&["-e", "1", "info"]).unwrap().encoding,
            Encoding::Big5
        );
        assert_eq!(parse(&["-e", "2", "info"]).unwrap().encoding, Encoding::Gbk);
        assert!(parse(&["-e", "latin1", "info"]).is_err());
    }

    #[test]
    fn list_takes_prefix_suffix_and_limit() {
        let cli = parse(&[
            "list",
            "--prefix",
            "equipment/",
            "--suffix",
            ".equ",
            "-l",
            "20",
        ])
        .unwrap();

        match cli.command {
            Command::List {
                prefix,
                suffix,
                limit,
            } => {
                assert_eq!(prefix, "equipment/");
                assert_eq!(suffix, ".equ");
                assert_eq!(limit, Some(20));
            }
            other => panic!("expected list, got {other:?}"),
        }
    }

    #[test]
    fn list_defaults_to_no_filter() {
        match parse(&["list"]).unwrap().command {
            Command::List {
                prefix,
                suffix,
                limit,
            } => {
                assert!(prefix.is_empty());
                assert!(suffix.is_empty());
                assert_eq!(limit, None);
            }
            other => panic!("expected list, got {other:?}"),
        }
    }

    #[test]
    fn hex_and_text_are_mutually_exclusive() {
        assert!(parse(&["read", "a.lst", "--hex", "--text"]).is_err());
        assert!(parse(&["read", "a.lst", "--hex"]).is_ok());
        assert!(parse(&["read", "a.lst", "--text"]).is_ok());
    }

    #[test]
    fn commands_that_need_a_target_reject_an_empty_call() {
        assert!(parse(&["read"]).is_err());
        assert!(parse(&["tokens"]).is_err());
        assert!(parse(&["entries"]).is_err());
        assert!(parse(&["search"]).is_err());
        assert!(parse(&["extract"]).is_err());
    }

    #[test]
    fn string_takes_a_numeric_index() {
        assert!(parse(&["string", "10000"]).is_ok());
        assert!(parse(&["string", "not-a-number"]).is_err());
    }

    #[test]
    fn a_missing_subcommand_is_an_error() {
        assert!(parse(&[]).is_err());
    }
}
