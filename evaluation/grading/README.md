# 评测端材料

本目录与优化集 10 例、测试集 7 例一一对应，每例包含：

- `reference.json`：诊断参考、动作约束和预期反馈，供评分使用。
- `backend-fixture.json`：模拟设备初始状态及响应规则，由评测端装载。

这些文件不是 Agent 的运行结果，也不能作为输入提供给被评测的 Agent。`manifest.json` 记录文件校验信息和输入绑定关系。

每个案例、每个版本都使用全新的数据库。以下命令示范如何装载某一案例；数据库路径由评测端自行选择，两个 MCP 服务须使用同一个案例数据库：

```bash
python3 interfaces/manage.py --db /tmp/lr_101-eval/state.sqlite3 init --fixture evaluation/grading/optimization/lr_101/backend-fixture.json --time-scale 20
```

运行前确认数据库不存在，或改用新的运行目录。MCP 通过 `LINE_RECOVERY_STATE_DB` 指定该数据库。不得让被评测的 Agent 直接读取数据库或本目录。详细评分方式见 `evaluation/SCORING.md`。
