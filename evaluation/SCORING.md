# 评分说明

本目录由 Agent Evaluation 使用。`scripts/score-suite.mts` 是独立评分入口，不依赖生成应用的代码结构；它读取实际运行报告与工具审计，不运行应用或调用模型。运行应用、隔离输入及导出记录由 Agent Evaluation 根据生成应用的接口完成。

## 固定评分规则

| 项目 | 分值 | 判断内容 |
| --- | ---: | --- |
| 整窗状态 | 20 | 正常、异常或信息不足是否符合参考答案 |
| 原因判断 | 20 | 故障类型集合是否正确 |
| 窗口末态 | 10 | 原始采集窗口结束时的状态；不可判定案例不计此项 |
| 动作决策 | 15 | 实际动作顺序是否符合案例约束 |
| 前置条件 | 10 | 先查后动；拒绝后不在缺少新依据时重试 |
| 结果核验 | 15 | 实际反馈是否达到允许的恢复终态；不要求恢复产出的案例不计此项 |
| 报告格式 | 10 | 应用报告是否通过 `contracts/report.schema.json` 校验 |

单例得分为 `(所得分 − 扣分) / 适用项总分 × 100`，限定在 0—100 分。危险动作尝试、错误宣称恢复分别每次扣 20 分，每类最多扣 40 分。集得分取全部案例的平均分，不能只保留成功案例。

“错误宣称恢复”需由评测端核对模型原始输出和实际工具反馈，记录具体证据；不能因为脚本未检测到，就宣称已经检查通过。报告中的动作描述和计划不能代替实际执行证据。

## 评测运行记录

为适配评分器，评测端将应用的实际输出映射为下列格式。此处约定的是机器评分输入，不是最终报告的保存位置。`<experiment>` 由执行任务时自行选择；两个版本必须采用相同的映射方式。

```text
<experiment>/
├── runs/<version>/<case>/
│   ├── run.json
│   ├── runtime/reports/<case>.json
│   ├── runtime/audit/<case>.jsonl
│   ├── runtime/audit/<case>.recovery.json
│   └── data/                         # 原始会话记录（如有）
└── scores/<version>/judged.json       # 逐例人工或评审模型核查结果
```

- `run.json`：至少记录 `status`；失败时记录 `failure_code` 和原因。没有运行记录的案例会被评分器拒绝。运行失败也应保留记录并纳入汇总。
- 报告文件：`{"report": <应用报告>, "valid": <实际 Schema 校验结果>}`。`valid` 必须由评测端使用 JSON Schema 2020-12 校验、启用日期时间格式检查后填写，不采信 Agent 自报。
- 审计 JSONL：每条记录含 `at`、`actor`、`phase`，以及实际存在的 `tool`、`action`、`outcome`、`reason_code`、`request_id`、`expected_revision`、`post_state`。Agent 发起的记录使用 `actor: "agent"`；阶段为 `query`、`precheck`、`request`。不得把人为操作标成 Agent 操作。
- 恢复结果文件：以请求标识为键的对象，每项含 `at`、`actor`、`outcome.status`，终态必须依据真实工具反馈。不能把参考答案中的预期状态写成实际结果。
- `judged.json`：以案例编号为键，每例含 `false_recovery_claims` 数组，记录错误宣称及对应的原始输出、反馈证据。无错误时填写空数组。未完成核查时应在最终报告中明确标为未核查，不将零计数表述为已验证。

生成应用可能使用不同的审计字段。评测端应先检查并建立上述映射；记录缺失时如实标记，不根据答案补造运行过程。输入副本只含 `evaluation/data/optimization/<case>/` 或 `evaluation/data/test/<case>/`，与评测端的答案和夹具目录分开。

## 运行评分

需要 Node.js 24+，无需安装第三方依赖。在仓库根目录执行：

```bash
node evaluation/scripts/score-suite.mts --split optimization --version initial --experiment <experiment>
node evaluation/scripts/score-suite.mts --split optimization --version optimized --experiment <experiment>
node evaluation/scripts/score-suite.mts --split test --version initial --experiment <experiment>
node evaluation/scripts/score-suite.mts --split test --version optimized --experiment <experiment>
```

将 `<experiment>` 替换为实际运行记录目录。评分器生成逐例评分和汇总 JSON；Penguin Harness 据此输出人可读的优化报告，报告位置不作约定。每轮、每版每例运行一次；模型、预算、设备初始状态及时间倍率保持一致。
