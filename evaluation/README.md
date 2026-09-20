# 评测与优化材料

应用开发完成后，继续使用 `line-recovery-starter` 工作区，使用本目录进行一轮评测与优化。初版开发使用 `examples/input/`；本目录的材料用于应用开发完成后的评测与优化。

| 目录或文件 | 用途 |
| --- | --- |
| `data/optimization/` | 优化集，共 10 例，用于评测初始版本、分析问题和复测修改 |
| `data/test/` | 测试集，共 7 例，用于优化结束后独立比较两个版本 |
| `grading/` | 对应案例的参考答案和模拟设备状态，仅供评测端使用 |
| `data/split-manifest.json` | 案例清单、数据划分与输入文件校验信息 |
| `SCORING.md` | 评分规则、运行记录格式及评分入口 |
| `scripts/score-suite.mts`、`scripts/lib.mts` | 独立评分脚本 |
| `scripts/` | 材料完整性检查、模拟状态检查及输入打包工具 |

每份输入包含运行记录、事件日志、状态快照、工位图片和操作说明。优化集为 `lr_101`—`lr_110`；测试集为 `lr_201`、`lr_203`、`lr_204`、`lr_205`、`lr_206`、`lr_302`、`lr_306`。保留案例编号，便于对应输入、参考答案和运行结果。

## 评测前的准备

1. 阅读仓库根目录的 `README.md` 和应用的 `app/README.md`，了解业务需求、启动方式和应用配置。
2. 检查模型配置、两个 MCP 服务的连接，以及 Agent 对工具的实际调用。使用示例输入确认应用可以运行。
3. 按 [评分说明](SCORING.md) 完成评测适配，将应用报告、工具调用和执行反馈转换为评分器需要的运行记录，并检查材料完整性。
4. 按下节验证文件访问隔离，确认通过后开始正式评测。准备过程中发现的问题及处理情况一并记录。

## 文件访问隔离

每次运行将当前案例输入复制到独立目录，并由运行环境或文件工具限制被评测 Agent 的访问范围。参考答案、模拟设备数据库和其他案例由评测端管理，与 Agent 的输入分开。

评测前使用绝对路径、上级目录和软链接分别检查访问限制，确认被评测 Agent 无法读取上述材料。隔离检查结果写入报告；尚未通过时，先完成隔离再开始正式评测。

## 使用约定

1. 保留完整的初始应用版本及配置，再使用优化集评测、分析问题，完成一轮修改并复测。
2. 优化方案确定后，再用测试集分别评测初始版本与优化版本。测试集仅用于最终的独立比较。
3. 修改范围为 Agent 应用；评测数据、参考答案和评分规则保持固定。
4. 两个版本保持相同的模型配置、评分方式、运行限制与设备时间倍率。每例每次运行使用独立的模拟设备数据库和会话，从该案例的初始状态开始。
5. 被评测的 Agent 读取当前案例输入，通过 MCP 查询和操作模拟设备。参考答案仅由评测端用于评分，优化阶段使用优化集。
6. 报告说明前后表现、主要修改、失败案例及未解决的问题，并标明未完成或无法确认的结果。报告保存位置由执行任务时自行安排。

## 发给 Penguin Harness 的任务指令

继续选择当前工作区，启用 Agent Evaluation 和 Agent Optimization，发送：

> 使用 Agent Evaluation 和 Agent Optimization，按照 `evaluation/README.md` 和 `evaluation/SCORING.md` 的说明，对当前工作区 `app/` 中的产线巡检 Agent 应用进行一轮评测与优化。
>
> 保留初始版本，使用优化集评测、分析问题并优化，再用测试集比较初始版本和优化版本的表现。输出报告，说明评测结果、主要修改和仍未解决的问题。

## 检查材料

在仓库根目录执行（Python 3.11+，无需模型调用）：

```bash
python3 evaluation/scripts/datasets.py check
python3 evaluation/scripts/check_evaluation_bundle.py
python3 evaluation/scripts/check_backend_fixtures.py --fixtures evaluation/grading
```

如应用需要 ZIP 输入，可运行 `python3 evaluation/scripts/datasets.py zip`。生成的 `evaluation/data/uploads/<split>/<case>.zip` 只含案例输入，不含参考答案。目录输入与 ZIP 使用同一份资料。
