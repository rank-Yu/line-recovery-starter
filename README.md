# 用 Penguin Harness 开发产线巡检 Agent 应用

这个仓库准备了开发“产线恢复助手”所需的业务需求、示例数据和 MCP 服务。你可以将它作为 Penguin Harness 的工作区，先开发应用，再用仓库中的评测材料检查效果、改进应用。

这里的“Agent 应用”包括 Agent 本体、后端和中文前端，代码放在 `app/` 中。两个 MCP 服务都在本地模拟环境中运行。

## 应用要完成什么任务

产线恢复助手需要读取工位资料，分析输送带为什么停机，判断是否可以操作设备，并在操作后检查实际结果。主要演示以下两个场景。

### 场景一：已经恢复供电，输送带却没有启动

现场刚发生过停电。现在供电已经恢复，但输送带仍然不动。Agent 需要结合电压、带速、驱动状态、产出计数和事件日志，判断停机经过。

这套设备恢复供电后，需要新的运行许可才能启动。Agent 应先通过 `power-control` 查询设备当前状态，确认供电、运行许可和安全条件都满足后，再请求恢复输送。随后继续检查带速和出口计数，确认输送带是否真的恢复运行、有新的纸箱通过。

### 场景二：温度过高导致停机，需要先散热

控制柜温度升高，输送带因温控保护而暂停。Agent 需要检查温度、风机状态和操作许可，必要时通过 `cooling-control` 开启风机散热。

开启风机后，Agent 继续观察风机反馈和温度变化。温度达标且重新取得运行许可后，再通过输送恢复服务请求启动输送带。

应用也应识别正常运行、计划停机、维护和资料不足等情况，并采取相应的处理方式。条件不满足、状态过期或结果无法确认时，应说明原因并转交人工处理。

## 仓库里有什么

| 文件或目录 | 用途 |
| --- | --- |
| `README.md` | 业务需求、开发要求和使用步骤 |
| `examples/input/` | 一份示例输入数据，用于开发和联调 |
| `contracts/` | 输入数据、设备状态、操作结果和报告的格式规范 |
| `interfaces/` | 输送恢复与散热控制两个 MCP 服务，以及接入说明 |
| `evaluation/` | 10 例优化集、7 例测试集、评分材料和评测脚本 |
| `app/` | 开发完成后的 Agent 应用 |

示例输入包含运行记录、事件日志、状态快照、工位图片和操作说明。其中，`telemetry.csv` 记录设备运行数据，`events.jsonl` 记录设备事件。

初版开发使用 `examples/input/` 中的示例输入；应用开发完成后，再使用 `evaluation/` 中的材料进行评测与优化。

## 如何开始开发

### 1. 准备工作区

将仓库克隆到本地：

```bash
git clone https://github.com/rank-Yu/line-recovery-starter.git
```

打开 Penguin Harness，新建对话，选择本地的 `line-recovery-starter` 文件夹作为工作区。若工作区中已有开发好的 `app/`，可以先按应用的 README 启动检查，再进入评测阶段。

两个 MCP 服务需要 Python 3.11+。应用所需的其他依赖，由 Penguin Harness 在交付的启动说明中列出。

### 2. 让 Penguin Harness 开发应用

选择 `agent-initialization` 技能，发送以下指令：

> 请使用 agent-initialization，先阅读 README.md，再查看 contracts/、interfaces/ 和 examples/input/，在 app/ 中开发产线恢复助手，包括 Agent、后端、中文前端和启动说明。接入已有的两个 MCP 服务，用示例数据检查输入读取和页面功能。展示工具的连接状态和实际执行结果。开发阶段使用 examples/input/ 联调，完成后保留初始版本，供后续评测与优化。

Penguin Harness 可以按以下顺序了解材料：先读本页的业务需求，再看 [输入与报告格式](contracts/README.md)、[MCP 接入说明](interfaces/README.md)，最后用 [示例输入](examples/README.md) 联调。报告结构见 [报告格式规范](contracts/report.schema.json)，[报告模板](contracts/report.template.json) 展示了各字段的组织方式。

### 3. 检查交付的应用

应用至少应做到以下几点：

- 支持加载示例或上传 ZIP，展示运行数据、日志、设备状态和图片。
- 展示诊断结论及依据，让读者能看出判断来自哪些资料。
- 操作前通过 MCP 查询当前设备状态，确认操作许可和前置条件。
- 根据后端的实际记录展示工具调用和执行结果。
- 区分“请求已受理”和“结果已确认”：启动请求被接受后，还要检查带速和产出；开启风机后，还要检查风机反馈和温度。
- 模型未配置、设备未初始化、工具无法连接或反馈不足时，明确说明问题和需要补充的配置或信息。

完成开发后，按 `app/README.md` 安装依赖、配置模型并启动应用，检查模型调用、两个 MCP 服务的连接和执行反馈。

示例使用 DeepSeek V4.1 Flash，模型 ID 为 `deepseek-flash`，API 地址为 `https://api.deepseek.com`。Penguin Harness 客户端和生成的应用分别配置模型；在客户端填过密钥后，仍需检查应用自己的配置。密钥保存在本地配置中。

## 如何评测和优化

继续使用同一个工作区，对 `app/` 中的应用进行一轮评测与优化：先保留初始版本，用优化集发现问题、修改应用并复测；优化完成后，用测试集比较两个版本的表现。

在 Penguin Harness 中新建对话，选择当前工作区，启用 Agent Evaluation 和 Agent Optimization，发送以下指令：

> 使用 Agent Evaluation 和 Agent Optimization，按照 `evaluation/README.md` 和 `evaluation/SCORING.md` 的说明，对当前工作区 `app/` 中的产线巡检 Agent 应用进行一轮评测与优化。
>
> 保留初始版本，使用优化集评测、分析问题并优化，再用测试集比较初始版本和优化版本的表现。输出报告，说明评测结果、主要修改和仍未解决的问题。

材料介绍见 [评测与优化说明](evaluation/README.md)，评分方式见 [评分说明](evaluation/SCORING.md)。报告由 Penguin Harness 生成并给出查看方式。

参考答案由评测端读取，具体的数据隔离要求见评测说明。
