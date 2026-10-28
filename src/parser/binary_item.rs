use enum_as_inner::EnumAsInner;

/// One token of a decoded payload.
///
/// `enum_as_inner` generates `as_int()`, `as_string()`, `into_string()`, ...
/// which return `Option<&T>`; the helpers below are the non-panicking
/// counterparts used by the entity parsers.
#[derive(EnumAsInner, Debug, Clone)]
pub enum BinaryItem {
    Int(i32),
    UInt(u32),
    Float(f32),
    String(String),
    Segment(String),
}

impl BinaryItem {
    /// The token as an integer, converting numbers of any width.
    pub fn as_int_value(&self) -> Option<i32> {
        match self {
            BinaryItem::Int(value) => Some(*value),
            BinaryItem::UInt(value) => Some(*value as i32),
            BinaryItem::Float(value) => Some(*value as i32),
            _ => None,
        }
    }

    /// The token as an unsigned integer, converting numbers of any width.
    pub fn as_uint_value(&self) -> Option<u32> {
        match self {
            BinaryItem::UInt(value) => Some(*value),
            BinaryItem::Int(value) => Some(*value as u32),
            BinaryItem::Float(value) => Some(*value as u32),
            _ => None,
        }
    }

    /// The token as a float, converting numbers of any width.
    pub fn as_float_value(&self) -> Option<f32> {
        match self {
            BinaryItem::Float(value) => Some(*value),
            BinaryItem::Int(value) => Some(*value as f32),
            BinaryItem::UInt(value) => Some(*value as f32),
            _ => None,
        }
    }

    /// The token as text; segments are *not* text values.
    pub fn as_text(&self) -> Option<&str> {
        match self {
            BinaryItem::String(value) => Some(value),
            _ => None,
        }
    }

    /// Human readable form used by the dump/debug helpers.
    pub fn to_display_string(&self) -> String {
        match self {
            BinaryItem::Int(value) => value.to_string(),
            BinaryItem::UInt(value) => value.to_string(),
            BinaryItem::Float(value) => value.to_string(),
            BinaryItem::String(value) => value.clone(),
            BinaryItem::Segment(value) => format!("[{value}]"),
        }
    }
}
