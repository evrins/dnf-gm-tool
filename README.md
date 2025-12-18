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


## 项目过程中借鉴了很多前人的项目

- [Zageku/DNF_pvf_python](https://github.com/Zageku/DNF_pvf_python)
- [Riles_Lee/ay.dnf.gmtool](https://gitee.com/Riles_Lee/dnf__-gm_-tools?skip_mobile=true) 

