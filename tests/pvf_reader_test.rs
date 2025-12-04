use pvf_parser_rs::entity::quest::Quest;
use pvf_parser_rs::parser::binary_item_parser::BinaryItemParser;
use pvf_parser_rs::parser::pvf_encoding::PVFEncoding;
use pvf_parser_rs::parser::pvf_reader::{
    PVFReader, decrypt_bytes, save_dungeon_to_parquet, save_equipment_to_parquet,
    save_exp_to_parquet, save_magic_seal_to_parquet, save_quest_to_parquet, save_skill_to_parquet,
    save_stackable_to_parquet,
};
use std::fs::File;
use std::io::{BufWriter, Write};
use tracing::info;

const SC_PVF: &str = "/Users/evrins/workspace/python/dnf_gm_tool/Script.简体.pvf";
const TC_PVF: &str = "/Users/evrins/workspace/python/dnf_gm_tool/Script.pvf";

#[test]
fn test_read_pvf_header() {
    let reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let leaf_map = reader.header.leaf_map;
    let mut leafs = leaf_map.values().cloned().collect::<Vec<_>>();
    leafs.sort_unstable_by(|a, b| a.file_path.cmp(&b.file_path));
    let output_file = File::create("dump/pvf_header.json").unwrap();
    let writer = BufWriter::new(output_file);
    serde_json::to_writer_pretty(writer, &leafs).unwrap();
}

#[test]
fn test_decrypt_bytes() {
    let buf = vec![1, 2, 3, 4, 5, 6, 7, 8];
    let crc = 12345;

    let output = decrypt_bytes(buf, crc);
    info!("{:?}", output);
}

#[test]
fn test_read_file_as_list() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let equ_file = "equipment/character/partset/upperset.equ";
    let res = reader.read_file_as_list(equ_file);
    info!(
        "{}",
        res.iter()
            .map(|it| format!("{:?}", it))
            .collect::<Vec<_>>()
            .join("\n")
    );
}

#[test]
fn test_read_lst_file() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let lst = reader.load_lst_file("equipment/equipment.lst");
    let file = File::create("dump/equipment_list.txt").unwrap();
    let mut bw = BufWriter::new(file);
    let mut keys = lst.cache.keys().copied().collect::<Vec<u32>>();
    keys.sort();
    for key in keys {
        if let Some(v) = lst.cache.get(&key) {
            writeln!(bw, "{:11}: {}", key, v).unwrap();
        }
    }
}

#[test]
fn test_binary_item_parse_equipment() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let equ_file = "equipment/character/swordman/avatar/face/chn_equ_special_avatar_swordman_face_101570538.equ";
    let res = reader.read_file_as_list(equ_file);
    let mut parser = BinaryItemParser::new(res);
    let equ = parser.parse_equipment();
    info!("{:?}", equ);
}

#[test]
fn test_parse_equipment_list_sc() {
    let mut reader = PVFReader::new(SC_PVF, PVFEncoding::GBK);
    let equ_list = reader.get_equipment_list();
    let file = File::create("dump/equipment_list.sc.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &equ_list).unwrap();
}

#[test]
fn test_parse_equipment_list_tc() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let equ_list = reader.get_equipment_list();
    let file = File::create("dump/equipment_list.tc.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &equ_list).unwrap();
}

#[test]
fn test_parse_quest_list_sc() {
    let mut reader = PVFReader::new(SC_PVF, PVFEncoding::GBK);
    let quest_list = reader.get_quest_list();
    let file = File::create("dump/quest_list.sc.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &quest_list).unwrap();
}

#[test]
fn test_parse_quest_list_ts() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let quest_list = reader.get_quest_list();
    let file = File::create("dump/quest_list.ts.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &quest_list).unwrap();
}

#[test]
fn test_save_equipment_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let equ_list = reader.get_equipment_list();

    save_equipment_to_parquet(equ_list, "equipments.parquet");
}

#[test]
fn test_validate_item_category_list_size() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let equ_list = reader.get_equipment_list();
    for it in equ_list.iter() {
        if it.item_category.len() > 1 {
            println!("{:?}", it);
        }
    }
}

#[test]
fn test_parse_stackable_list() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let stackable_list = reader.get_stackable_list();
    let file = File::create("dump/stackable.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &stackable_list).unwrap();
}

#[test]
fn test_save_stackable_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let stackable_list = reader.get_stackable_list();

    save_stackable_to_parquet(stackable_list, "dump/stackables.parquet");
}

#[test]
fn test_save_quest_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let quest_list = reader.get_quest_list();

    save_quest_to_parquet(quest_list, "dump/quests.parquet");
}

#[test]
fn test_save_dungeon_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let dungeon_list = reader.get_dungeon_list();

    save_dungeon_to_parquet(dungeon_list, "dungeons.parquet");
}
#[test]
fn test_save_skill_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let skill_list = reader.get_skill_list();

    save_skill_to_parquet(skill_list, "skills.parquet");
}

#[test]
fn test_get_skill_list() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let skill_list = reader.get_skill_list();
    let file = File::create("dump/skill_list.tc.json").unwrap();
    let bw = BufWriter::new(file);
    serde_json::to_writer_pretty(bw, &skill_list).unwrap();
}

#[test]
fn test_save_exp_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let exp_list = reader.get_exp_list();

    save_exp_to_parquet(exp_list, "exps.parquet");
}

#[test]
fn test_save_magic_seal_to_parquet() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let magic_seal_list = reader.get_magic_seal_list();

    save_magic_seal_to_parquet(magic_seal_list, "magic_seals.parquet");
}

#[test]
fn test_create_test_data_for_orb() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);
    let stackable_list = reader.get_stackable_list();
    save_stackable_to_parquet(stackable_list, "dump/stackables.parquet");

    let skill_list = reader.get_skill_list();
    save_skill_to_parquet(skill_list, "dump/skills.parquet");
}

#[test]
fn test_get_lst_file() {
    let mut reader = PVFReader::new(TC_PVF, PVFEncoding::BIG5);

    let lsf_file = reader.load_lst_file("skill/autoskill.lst");

    let mut res: Vec<Quest> = vec![];

    for (id, fp) in lsf_file.cache.iter() {
        let quest_file = format!("{}/{}", lsf_file.base_dir, fp);
        let buf = reader.read_file_as_list(&quest_file);
        let mut parser = BinaryItemParser::new(buf);
        let mut q = parser.parse_quest();
        q.id = *id;
        res.push(q);
    }
}
