# Line Recovery Starter

使用 Penguin Harness 从零构建产线巡检 Agent 的起始材料。仓库提供业务需求、输入示例、数据与报告规范，以及两个可运行的模拟设备 MCP 服务。`app/` 由 Penguin Harness 在后续构建时生成。

## 获取材料

```bash
git clone https://github.com/rank-Yu/line-recovery-starter.git
cd line-recovery-starter
```

在 Penguin Harness 中选择 `line-recovery-starter` 作为工作区，并配置可用的模型。模拟设备服务需要 Python 3.11 或更高版本，只使用标准库。

## 业务需求

制作一个中文产线巡检应用：用户上传输送工位资料后，Agent 结合运行记录、日志、设备状态快照和工位图片分析异常，给出判断依据；需要操作时查询设备当前状态，确认条件后调用工具，并根据后续反馈说明结果。

- **来电后仍然停机。** 设备不随供电恢复自动重启。Agent 核对停机经过，再查询当前供电、运行许可等条件，通过 power-control 请求恢复输送，并核对带速和出口计数。
- **温度升高导致暂停。** Agent 根据温度与风机记录判断是否需要散热，通过 cooling-control 请求开启风机。温度持续达标且运行许可恢复后，再查询状态并请求恢复输送。

条件不满足、信息不足、风机故障或结果尚未确认时，应保留实际状态并说明原因。所有设备操作都在本地模拟环境中执行，不连接真实设备。

## 材料与阅读顺序

| 材料 | 用途 |
| --- | --- |
| 本 README | 业务需求与交付目标 |
| [contracts/](contracts/README.md) | 输入格式、设备状态、动作结果、报告 Schema 与模板 |
| [examples/input/](examples/input/README.md) | 一份完整的供电恢复场景输入 lr_001，不含答案与执行结果 |
| [interfaces/](interfaces/README.md) | 输送恢复和散热控制 MCP 的源码、接口说明与联调方式 |

输入示例中的 `events.jsonl` 和 `telemetry.csv` 是待分析的原始设备资料，不是 Agent 的运行记录。状态快照反映采集时刻，不是执行操作的实时授权。工位图片只用于核对可见物料，不能单独证明停机原因。

## 开始构建

先在 Penguin Harness 中查看当前可用的 Agent 构建技能，再发送下面的指令；需要指定技能时，使用当前版本中的实际名称。

> 阅读根目录 README.md，以及 contracts/、interfaces/ 和 examples/input/，按照业务需求在 app/ 中构建产线巡检 Agent、后端与中文网页应用。接入两个已提供的模拟 MCP 服务，让 Agent 先查询当前状态、满足条件后请求操作，并读回反馈确认结果。用 examples/input/ 联调资料读取、诊断与报告展示，提供依赖安装、模型配置、模拟设备初始化和启动说明。未连接工具或未配置模型时明确提示，不伪造执行结果。本轮只完成初始构建和联调，不扩充数据、不优化或正式评分，不修改原始输入与接口契约。

## 交付要求

- 支持加载 `examples/input/`，以及上传以 `request.json` 为根文件的 ZIP。
- 页面展示原始资料、历史异常判断、证据、工具调用及操作后的反馈。
- Agent 调用查询与操作工具；页面根据真实工具记录展示动作，不把模型的计划当作已执行。
- 区分命令受理、设备运行反馈和出口恢复产出；报告符合 `contracts/report.schema.json`。
- 生成代码、依赖和应用说明放在 `app/`；模型密钥从环境变量或本地 `.env` 读取，不进入代码和报告。
- 工具未连接、状态过期或条件不足时，明确显示未执行或需人工处理。
- 保存初始应用版本，说明如何启动、验证及重新初始化演示状态。

## 目录

```text
line-recovery-starter/
├── README.md
├── contracts/
├── examples/
│   └── input/
└── interfaces/
    ├── power-control/
    ├── cooling-control/
    ├── shared/
    ├── tests/
    └── manage.py
```

仓库不包含应用成品、Agent 会话、运行数据库、执行日志、评测答案或成绩。MCP 服务源码属于预先提供的设备能力，数据库和审计记录在运行时创建。

材料整理自 [line-recovery](https://github.com/lzh368/line-recovery)，该仓库可作为完整实现与后续实验的参考；本仓库使用独立提交历史作为构建起点。
