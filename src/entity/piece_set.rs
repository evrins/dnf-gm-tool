use crate::entity::piece_set_ability::PieceSetAbility;

#[derive(Default, Debug)]
pub struct PieceSet {
    pub set_name: String,
    pub piece_set_ability: Vec<PieceSetAbility>,
    pub parameter_basic_explain: String,
    pub part_set_index: i32,
}
