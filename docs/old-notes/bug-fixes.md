# 守墓人攻略 — 避坑指南

> 记录开发、维护过程中遇到的所有问题及其解决方案。

## 1. 游戏数据不准确（主教任务线）

**问题描述**：主教（Bishop）任务线数据存在多处错误：
- 任务顺序不对
- 物品名称不正确
- 解锁条件有误

**根因**：数据来源为网页搜索抓取，未经人工逐条验证。

**解决方案**：
- 需要与官方 wiki 或游戏内数据逐条比对
- 优先校对主教任务线，因其错误较多
- 修改 `static/graveyard-keeper-data.json` 中的对应条目
- 修改后刷新页面即可生效（JSON 文件不需重启服务）

## 2. HTML 修改后页面不刷新

**问题描述**：修改了 `graveyard-keeper.html` 模板，刷新浏览器后页面内容没有变化。

**根因**：HTML 模板在服务启动时一次性读入内存，存为 `GUIDE_PAGE` 全局变量。修改磁盘上的 HTML 文件不会影响内存中的内容。

**解决方案**：
```bash
systemctl restart service-dashboard
```
重启后内存中的 `GUIDE_PAGE` 重新从磁盘读取，页面更新生效。

**预防措施**：修改 .html 文件后务必执行重启命令。

## 3. JSON 数据文件路径问题

**问题描述**：数据文件（`graveyard-keeper-data.json`、`graveyard-keeper-npc.json`）路径容易写错，导致运行时找不到文件。

**根因**：直接使用相对路径或绝对路径硬编码，部署环境变化时路径失效。

**解决方案**：使用 `Path(__file__).parent / 'static/...'` 相对路径：
```python
from pathlib import Path
DATA_FILE = Path(__file__).parent / 'static/graveyard-keeper-data.json'
NPC_FILE = Path(__file__).parent / 'static/graveyard-keeper-npc.json'
```

## 4. 服务类型判断错误

**问题描述**：守墓人攻略不是独立服务（没有自己的端口），容易误判为独立 HTTP 服务。

**根因**：它是 FastAPI 应用中的一个子路由，依赖父应用（端口 8899）提供服务。

**解决方案**：
- 在 `KNOWN_SERVICES` 中以 `route` 类型注册，而非 `web` / `http` 类型
- 服务健康检测检测父端口（8899）存活状态
- 检测方式：检查父进程端口或请求父 URL

## 5. 模板渲染陷阱

**问题描述**：模板中的 Jinja2 语法错误不会在页面加载时显示，只有在访问子路由时才会报错。

**解决方案**：修改模板后先访问子路由 `/game/graveyard-keeper` 确认渲染正常，同时注意检查服务日志中的 Jinja2 错误信息。
