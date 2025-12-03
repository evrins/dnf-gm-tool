use enum_as_inner::EnumAsInner;

#[derive(EnumAsInner, Debug, Clone)]
pub enum BinaryItem {
    Int(i32),
    UInt(u32),
    Float(f32),
    String(String),
    Segment(String),
}
