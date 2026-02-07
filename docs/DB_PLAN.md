# DB_PLAN.md

## 1. MVP 数据库策略

### 目标
- 明天演示优先：稳定、可复现、低复杂度。

### 方案（按优先级）
1. 本地演示：`SQLite`（零运维，启动快）
2. 云演示可选：`PostgreSQL`（Neon / Supabase）

结论：**先 SQLite 跑通，再按时间切 PostgreSQL**。

## 2. 数据模型（与 ERD 对齐）

核心表：
- `customer`
- `invoice`
- `risk_assessment`
- `collection_strategy`
- `execution_action`
- `audit_event`

关键字段约束：
- `risk_level` in (`low`, `medium`, `high`)
- `confidence` in `[0, 1]`
- `action_status` in (`queued`, `sent`, `failed`, `skipped`)

## 3. MVP 建表建议（最小）

### 必须先建
- `invoice`
- `risk_assessment`
- `collection_strategy`
- `audit_event`

### 可后建
- `customer`
- `execution_action`

## 4. 读写策略

- 默认只做 MVP 必要写入：`risk_assessment`、`collection_strategy`、`audit_event`
- 禁止破坏性 SQL（drop/truncate）进入演示流程
- 所有写入操作按 `trace_id` 可追踪

## 5. 迁移与初始化

### SQLite
- 文件：`data/app.db`
- 初始化脚本：`scripts/init_db.sql`（后续补代码时创建）

### PostgreSQL（可选）
- 连接串由 `DATABASE_URL` 提供
- 先跑同一份 DDL，再导入样例

## 6. 明天执行顺序

1. SQLite 建最小表
2. 导入样例发票（6~10 条）
3. 跑主链路并确认审计事件落库
4. 若时间允许再切 PostgreSQL

## 7. 验收标准

- [ ] 主链路落库成功
- [ ] `audit_event` 可按 `trace_id` 查询
- [ ] `risk_level/confidence/reasons/next_action` 字段完整
- [ ] 连续 3 次演示无数据库错误
