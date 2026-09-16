# Line Recovery · 产线恢复助手

用 Penguin 制作中文应用：上传纸箱输送工位资料，分析异常；有工具侧许可时请求恢复，并依据新反馈说明结果。本仓库提供构建所需的业务说明、输入示例、契约和两个演示 MCP 服务，不包含已生成的应用、运行记录或评测产物。

## 两个业务故事

### 停电后已经来电，输送线仍未恢复

生产中的输送段突然停下。现场人员反馈刚才短时停电，现在已来电，但输送带仍没有转动，图片中纸箱分散排列。助手需要结合电压、驱动就绪、速度、计数、日志和生产任务核对经过，不能仅凭图片判定停机原因。

设备采用“不随来电自动重启”的规则。Agent 先查询最新可信状态；供电和运行许可、安全条件均满足时，通过 power-control 请求恢复输送，再核对带速及新的出口计数。不需要再次接通电源，更不能看到“已来电”就直接启动。

### 温度升高，开启散热后再核验

驱动柜温度升高，控制器按温控策略暂停输送，独立风机未开启。助手依据温度趋势、风机指令和反馈判断是否请求散热。cooling-control 只开启批准的风机模式，不修改温度、不解除保护、不启动输送。

风机开启后要观察温度。满足公开恢复条件并由后端重新给出运行许可后，才能通过受控启动入口请求恢复。风机不转、温度不降、状态过期或其他条件不满足时，说明失败/未确认并转人工。

这些是应用需求和公共设备规则，不是逐例答案。正常、计划停机、维护及资料不足也必须能正确处理。

## 给 Penguin 的材料与阅读顺序

1. 本 README：业务背景、功能和分工。
2. [输入格式](contracts/README.md)、[状态 Schema](contracts/device-state.schema.json)、[报告 Schema](contracts/report.schema.json) 和 [模板](contracts/report.template.json)。
3. [供电恢复 MCP](interfaces/power-control/README.md)、[散热 MCP](interfaces/cooling-control/README.md)。
4. 联调时看 [example](examples/README.md)：一份完整但无答案的输入，用来理解文件和数据格式，不是必须照抄的解题范文。

初版制作只使用这一份无答案 example。后续训练、测试输入、参考答案和评测记录不随本仓库提供；`telemetry.csv` 和 `events.jsonl` 是待分析的原始设备资料，不是 Agent 运行记录。

## 应用交付要求

- 上传 ZIP 或加载 example，浏览 CSV、日志、状态和图片。
- 分别展示历史异常判断、证据、动作请求、最新反馈及未确定事项。
- 先查询工具当前状态再决定是否执行，上传快照的许可不授予真实执行权限。
- 前端从实际后端审计记录展示动作，不把模型写出的计划当作已执行。
- 命令受理、风机转动、温度达标、输送运行、出口恢复产出是不同阶段。
- 没有服务时显示“工具未连接”；默认演示模式，不伪造真实恢复。
- Penguin 在 `app/` 编写 Agent、前后端、MCP 客户端和启动说明；MCP 服务已交付到 `interfaces/`。未初始化后端或未连接时，应用仍应如实显示不可用。

### 发给 Penguin 的构建指令

工作区选择仓库根目录 `line-recovery-starter`，勾选应用中的 `agent-initialization` 技能，发送：

> 请使用 agent-initialization，先读 README.md，再看 contracts/、interfaces/ 和 examples/input/，在 app/ 制作产线恢复助手，包括 Agent、后端、中文前端和启动说明。按现有契约实现两个 MCP 的客户端；服务未交付时明确显示未连接，不伪造动作成功。用 example 联调输入读取和页面，保留初始版本，本轮不扩充数据、不做优化或正式评分。

原仓库的指令使用 `agent-creation`；当前版本显示为 `agent-initialization`，上面仅替换技能名称，其余指令沿用原文。两个 MCP 服务已经提供，接入与初始化见 [MCP 使用说明](interfaces/README.md)。应用构建完成后仍需验证模型调用、工具连接和反馈读取。

## 当前文件

```text
line-recovery-starter/
├── README.md             # Penguin 的构建要求与业务说明
├── examples/input/       # 一份无答案输入，未含恢复后的记录
├── contracts/            # 数据和报告结构、输出模板
└── interfaces/
    ├── power-control/    # 可运行的查询与恢复输送 MCP
    ├── cooling-control/  # 可运行的查询与散热 MCP
    ├── shared/           # 共用演示后端、状态版本及操作审计
    ├── tests/            # MCP 服务回归测试
    └── manage.py         # 演示设备初始化、复位与状态查询
```

`app/` 由 Penguin 在构建时生成。制作 example 为供电场景，保持不变。两个 MCP 只操作独立的 dry_run 演示状态，不连接真实设备。

资料是新制作的合成演示工位，使用独立控制供电与 24 V DC 驱动支路，不是电池设备。风机位于闭合控制柜内，不能凭图片判断其状态。

## 获取材料

```bash
git clone https://github.com/rank-Yu/line-recovery-starter.git
cd line-recovery-starter
```

MCP 服务需要 Python 3.11+，仅使用标准库；生成应用所需的其他依赖以 Penguin 交付的启动说明为准。

本文示例使用 DeepSeek V4.1 Flash（提供方 `deepseek`，模型 ID `deepseek-flash`，官方 API 地址 `https://api.deepseek.com`）。Penguin 客户端的模型配置与生成应用的模型配置分别处理；应用启动时还需按其说明配置密钥，不将密钥提交到仓库。

材料来自 [line-recovery](https://github.com/lzh368/line-recovery/tree/1e1f1e33d2ea55feafa89ae22895623179f68cfd)。业务故事与应用交付要求沿用原文，保留现成的 MCP 服务，移除应用成品、运行记录和评测材料。这是基于同一份需求与接口重新构建应用的起点；模型与 Penguin 版本会影响生成结果，不保证生成代码或界面逐字节相同。
