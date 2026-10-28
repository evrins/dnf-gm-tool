/// Text encoding used by an archive.
///
/// The value is the same integer the Python side stores in its configuration
/// (`1` = traditional/BIG5, `2` = simplified/GBK).
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq)]
pub enum PVFEncoding {
    #[default]
    BIG5 = 1,
    GBK = 2,
}

impl PVFEncoding {
    pub fn from_i32(value: i32) -> Option<Self> {
        match value {
            1 => Some(PVFEncoding::BIG5),
            2 => Some(PVFEncoding::GBK),
            _ => None,
        }
    }

    /// Short label used in logs and error messages.
    pub fn label(&self) -> &'static str {
        match self {
            PVFEncoding::BIG5 => "BIG5",
            PVFEncoding::GBK => "GBK",
        }
    }

    /// The other encoding.
    pub fn other(&self) -> Self {
        match self {
            PVFEncoding::BIG5 => PVFEncoding::GBK,
            PVFEncoding::GBK => PVFEncoding::BIG5,
        }
    }
}
