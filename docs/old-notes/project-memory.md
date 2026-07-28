# 守墓人攻略 — 项目记忆

## 项目性质

- 静态交互式指南页面，挂载在服务面板 8899 端口的子路由 `/game/graveyard-keeper`
- 不是独立服务，是 FastAPI 应用中的一个路由

## 架构要点

| 条目 | 说明 |
|------|------|
| **模板加载** | HTML 模板在服务启动时一次性读入内存，存为 `GUIDE_PAGE` 全局变量 |
| **数据读取** | JSON 数据文件（`static/graveyard-keeper-data.json`、`static/graveyard-keeper-npc.json`）每次请求时读取 |
| **模板修改** | 修改 HTML 后必须 `systemctl restart` 重启服务 |
| **数据修改** | 修改 JSON 后无需重启，刷新页面即可生效 |

## 数据文件

| 文件 | 内容 | 说明 |
|------|------|------|
| `static/graveyard-keeper-data.json` | 合成配方（crafting）+ 任务线（quests） | 按 module 分组，含 unlock_order 排序 |
| `static/graveyard-keeper-npc.json` | NPC 商店数据 | 按 NPC 分组，含 phase 阶段性解锁 |

## 时间线

- **2026-07-23（初始）**：实现 graveyard-keeper.html 模板，作为服务面板子路由
- **2026-07-23（服务注册）**：注册为 `route` 类型服务，加入服务面板监控
- **2026-07-23（链接配置）**：在 `SERVICE_LINKS` 中配置跳转 URL

## 路径约定

- 数据文件路径使用 `Path(__file__).parent / 'static/...'` 相对路径
- HTML 文件路径同理，确保在不同部署环境下路径正确
