# 模拟设备 MCP 服务

本目录提供 `power-control` 和 `cooling-control`，用于生成应用时接入。两个服务使用 Python 3.11+ 标准库，通过 MCP stdio 运行，共享一个 SQLite 模拟设备数据库，不调用模型，也不连接真实设备。

| 服务 | 查询工具 | 操作工具 |
| --- | --- | --- |
| power-control | get_device_status | resume_conveyor：供电恢复后请求启动输送 |
| cooling-control | get_cooling_status | start_cooling：开启散热，不直接启动输送 |

## 初始化设备状态

在仓库根目录运行以下命令，为 `examples/input/` 中的 lr_001 准备供电恢复演示环境：

```bash
python3 interfaces/manage.py init --profile power-return
python3 interfaces/manage.py status
```

默认数据库为 `interfaces/runtime/demo.sqlite3`，首次初始化时创建，不随仓库分发。已有数据库时 `init` 拒绝覆盖。需要重新演示时，先停止使用这份数据库的服务，再运行：

```bash
python3 interfaces/manage.py reset --profile power-return
```

`reset` 开始新一轮模拟，同时保留旧状态与审计。内置场景还有 `cooling`、`maintenance` 和 `fan-failure`，用于验证接口行为，不是额外的 Agent 测试案例。

## 由应用连接 MCP

构建应用时，让 Penguin Harness 根据以下配置管理两个 stdio 子进程。下面的路径以仓库根目录作为进程工作目录；如果应用使用其他工作目录，应解析为绝对路径或相应调整。

```json
{
  "power-control": {
    "command": "python3",
    "args": ["interfaces/power-control/server.py"]
  },
  "cooling-control": {
    "command": "python3",
    "args": ["interfaces/cooling-control/server.py"]
  }
}
```

这是客户端接入信息，具体配置格式由生成的应用或 SDK 决定。直接在终端运行 `server.py` 会等待 MCP JSON-RPC 消息，不会打开网页。

两个进程默认使用同一份数据库。需要指定数据库时，给它们设置相同的 `LINE_RECOVERY_STATE_DB` 绝对路径。应用的模型配置与 MCP 配置分别处理；MCP 本身不需要 API Key。

## 调用与反馈

先调用查询工具，再根据返回的条件、`revision` 和有效期请求操作。写请求包含 `device_id`、`expected_revision` 和 `request_id`；完整参数见两个服务的 `tools.json`。操作受理后继续查询，确认真实的模拟反馈，不能把 `accepted` 当作完成。

供电恢复场景先返回带速反馈，再出现新的出口计数。散热场景先返回风机反馈，再逐步降温；满足连续达标条件后，才能另行请求恢复输送。演示按经过时间推进，不按查询次数推进。默认 `--time-scale 20` 表示一秒真实时间对应二十秒演示时间，不能用作真实设备性能数据。

服务只支持 `dry_run`；`live` 模式会被拒绝。不提供解除急停、维护锁定、屏蔽保护或任意脚本执行工具。

## 验证服务

```bash
python3 -m unittest discover -s interfaces/tests -v
```

测试使用临时数据库，覆盖状态检查、幂等、反馈和真实 stdio 协议交互，不调用模型、不生成 Agent 评分。
