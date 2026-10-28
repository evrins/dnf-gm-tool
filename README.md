# Seria 自用的 DOF GM 工具

一方面满足自己玩单机时的需求, 不过最近都不玩了

一方面用来练习一下 pyside6 实现桌面应用, 整体用下来 Qt 自带的 Designer 用起来还不错, 整个生态还是太弱了, 没有的控件还得自定义
以同步代码的方式来写 UI 还是太吃亏了, 有时间用 async python 或者 electron 实现一次

中间使用了 rust 来实现 pvf 文件缓存文件的生成, 处理时间从 30 秒 降低到 4.8 秒 

## 使用说明

使用前需要在设置页面, 配置数据库和导入 Scripts.pvf 文件生成缓存数据, 然后在角色列表中选择角色

使用修改角色属性 / 任务状态 / 装备参数 时, 需要切换角色以避免数据被服务端覆盖

## 页面介绍

### 角色列表

<img src="./docs/tab_character_list.png" alt="character list tab" width="75%" >

对中文名称的处理不完善, 通过角色名来筛选是在客户端处理的, 数据量大的话会卡顿 

### 角色信息

<img src="./docs/tab_character_info.png" alt="character info tab" width="75%" >

角色信息相关的修改项, 不能修改名称, 对中文处理的不完善

### 装备搜索

<img src="./docs/tab_equipment_search.png" alt="equipment search tab" width="75%" >

选中装备后, 点击**发送到邮件**后, 会跳转到邮件页面, 可以在邮件页面再编辑属性, 默认品级为 232 最上级 99%, 以邮件形式发送给角色

### 物品搜索

<img src="./docs/tab_item_search.png" alt="equipment search tab" width="75%" >

选中装备后, 点击**发送到邮件**后, 可以在邮件页面再编辑数量, 以邮件形式发送给角色

### 物品

<img src="./docs/tab_item.png" alt="equipment search tab" width="75%" >

可以编辑当前角色的**穿戴栏** / **背包** / **宠物栏** / **角色金库** / **账号金库** 中的物品

### 邮件

<img src="./docs/tab_mail.png" alt="equipment search tab" width="75%" >

可以删除邮件, 作为发送**装备** / **物品**的二次编辑页面

### 任务

<img src="./docs/tab_quest.png" alt="equipment search tab" width="75%" >

完成任务, 查看任务详情, 对于需要**装备** / **物品**的任务会使用邮件来发送

### 设置

<img src="./docs/tab_settings.png" alt="equipment search tab" width="75%" >

配置数据库连接, 连接成功的数据库配置, 会保存到配置文件, 下次打开的时候会尝试使用上次使用的配置

新增 / 更新 / 删除 / 选择当前使用的 pvf 缓存


## Script.pvf 解析

解析全部由 `pvf_parser_rs`（`src/` 下的 Rust crate）完成，Python 侧只消费生成的 parquet 缓存。
crate 也可以单独使用：

```rust
use pvf_parser_rs::parser::pvf_encoding::PVFEncoding;
use pvf_parser_rs::parser::pvf_reader::PVFReader;

let mut reader = PVFReader::open("Script.pvf", PVFEncoding::GBK)?;
println!("{} files, uuid {}", reader.file_count(), reader.uuid());

for path in reader.list_files("equipment/", ".equ", Some(10)) {
    println!("{path}");
}

// 任意文件的原始内容 / token 流 / [tag] = value 视图
// read_file 只借用 &self（定位读），解析 token 才需要 &mut（要写字符串缓存）
let bytes = reader.read_file("equipment/equipment.lst")?;
let tokens = reader.read_file_as_list("equipment/equipment.lst")?;
let entries = reader.read_file_as_dict("n_quest/alphraira/darkelfcemetary/epic_39_darkelfcemetary_drake_1.qst")?;
```

调试时可以直接用附带的命令行工具（clap 实现，`pvf_dump --help` 看全部子命令）：

```bash
cargo run --release --bin pvf_dump -- info
cargo run --release --bin pvf_dump -- list --prefix equipment/ --suffix .equ --limit 20
cargo run --release --bin pvf_dump -- entries n_quest/alphraira/darkelfcemetary/epic_39_darkelfcemetary_drake_1.qst
cargo run --release --bin pvf_dump -- search 太刀 --limit 5
cargo run --release --bin pvf_dump -- extract /tmp/pvf --suffix .lst
```

归档路径默认是当前目录的 `Script.pvf`，用全局参数 `-p/--pvf` 指定（放在子命令前后都行），
`-e/--encoding gbk|big5` 选择编码（旧写法 `--encoding 1|2` 仍然可用）。
`cargo install --path . --bin pvf_dump` 之后可以直接当 `pvf_dump` 用。

`search` 先查字符串表（那里只有 `name_780104` 这样的键），再查 `*.str` 字典里的正文，
所以搜中文要搜的那一段会从 `equipment/equipment.kor.str: key>value` 这种形式返回。

要点：

- 头部 / 目录树 / 每个文件都按 `crc32 ^ 0x81A79011` 异或后再循环右移 6 位（4 字节为一组），
  目录树的 crc 来自头部，文件的 crc 来自目录树里的叶子节点。
- 载荷是 `类型字节 + u32` 的 token 流：`2/3/4` 为数字，`5/6/8` 为 `[tag]` 段，`7` 为字符串，
  `9` 为间接字符串（`n_string.lst` → `*.str` 字典），最后按 4 字节对齐补齐。
- 字符串表 `stringtable.bin` 的偏移量是相对偏移表本身（不含开头的 `count`）计算的。
- 编码不是存在文件里的：字符串表用配置的 BIG5/GBK 解码，`*.str` 字典则按内容自动判断
  （同一份 pvf 里混用两种编码是常见情况）。
- 读取走定位读（`pread`）而不是 seek + 缓冲读，解密在同一个缓冲区里原地完成；
  全部 7 个数据集（33 万个文件里的约 8 万个）解析并落 parquet 约 **3.2 秒**（release）。
- 出错一律返回 `PvfError`，不会 panic：文件不存在、截断、字符串表越界、token 越界都有独立分支。

## 项目过程中借鉴了很多前人的项目

- [Zageku/DNF_pvf_python](https://github.com/Zageku/DNF_pvf_python)
- [Riles_Lee/ay.dnf.gmtool](https://gitee.com/Riles_Lee/dnf__-gm_-tools?skip_mobile=true) 

