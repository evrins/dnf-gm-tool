pub mod entity;
pub mod parser;

#[cfg(feature = "python")]
use pyo3::prelude::*;

#[cfg(feature = "python")]
#[pymodule]
fn pvf_parser_rs(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(save_parquet, m)?)?;
    Ok(())
}

#[cfg(feature = "python")]
#[pyfunction]
fn save_parquet(py: Python<'_>, fp: &str, encoding: i32, output_dir: &str) {
    use crate::parser::pvf_encoding::PVFEncoding;
    use crate::parser::pvf_reader::PVFReader;
    use crate::parser::pvf_reader::save_dungeon_to_parquet;
    use crate::parser::pvf_reader::save_equipment_to_parquet;
    use crate::parser::pvf_reader::save_exp_to_parquet;
    use crate::parser::pvf_reader::save_magic_seal_to_parquet;
    use crate::parser::pvf_reader::save_quest_to_parquet;
    use crate::parser::pvf_reader::save_skill_to_parquet;
    use crate::parser::pvf_reader::save_stackable_to_parquet;
    use std::fs;
    use std::path::Path;

    tracing_subscriber::fmt().try_init().ok();

    let pvf_encoding = match encoding {
        1 => PVFEncoding::BIG5,
        2 => PVFEncoding::GBK,
        _ => {
            panic!("Invalid encoding")
        }
    };

    py.detach(|| {
        let mut reader = PVFReader::new(fp, pvf_encoding);
        let output_dir = Path::new(output_dir);
        fs::create_dir_all(output_dir).unwrap();

        let equipment_list = reader.get_equipment_list();
        save_equipment_to_parquet(equipment_list, &output_dir.join("equipments.parquet"));

        let stackable_list = reader.get_stackable_list();
        save_stackable_to_parquet(stackable_list, &output_dir.join("stackables.parquet"));

        let quest_list = reader.get_quest_list();
        save_quest_to_parquet(quest_list, &output_dir.join("quests.parquet"));

        let dungeon_list = reader.get_dungeon_list();
        save_dungeon_to_parquet(dungeon_list, &output_dir.join("dungeons.parquet"));

        let skill_list = reader.get_skill_list();
        save_skill_to_parquet(skill_list, &output_dir.join("skills.parquet"));

        let exp_list = reader.get_exp_list();
        save_exp_to_parquet(exp_list, &output_dir.join("exps.parquet"));

        let magic_seal_list = reader.get_magic_seal_list();
        save_magic_seal_to_parquet(magic_seal_list, &output_dir.join("magic_seals.parquet"));
    });
}
