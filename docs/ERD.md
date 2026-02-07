# ERD.md — Intelligent Billing Operations Engine (MVP)

## 1. 实体关系图（Mermaid）

```mermaid
erDiagram
    CUSTOMER ||--o{ INVOICE : owns
    CUSTOMER ||--o{ PAYMENT_BEHAVIOR_SNAPSHOT : has
    INVOICE ||--|| RISK_ASSESSMENT : evaluated_as
    RISK_ASSESSMENT ||--|| COLLECTION_STRATEGY : drives
    COLLECTION_STRATEGY ||--o{ EXECUTION_ACTION : executes
    EXECUTION_ACTION ||--o{ AUDIT_EVENT : emits

    CUSTOMER {
      string customer_id PK
      string segment
      string preferred_channel
      int delinquency_count_90d
      int disputes_count_180d
      datetime created_at
    }

    INVOICE {
      string invoice_id PK
      string customer_id FK
      decimal amount_due
      string currency
      int overdue_days
      datetime due_date
      string invoice_status
      datetime created_at
    }

    PAYMENT_BEHAVIOR_SNAPSHOT {
      string snapshot_id PK
      string customer_id FK
      decimal avg_days_to_pay
      int late_payments_180d
      decimal collected_ratio_180d
      datetime snapshot_time
    }

    RISK_ASSESSMENT {
      string risk_id PK
      string invoice_id FK
      string risk_level
      float confidence
      string reasons_json
      datetime assessed_at
    }

    COLLECTION_STRATEGY {
      string strategy_id PK
      string risk_id FK
      string channel
      string tone
      string next_action
      bool escalation
      datetime generated_at
    }

    EXECUTION_ACTION {
      string action_id PK
      string strategy_id FK
      string provider
      string action_type
      string action_status
      datetime executed_at
    }

    AUDIT_EVENT {
      string event_id PK
      string action_id FK
      string trace_id
      string event_type
      string payload_json
      datetime event_time
    }
```

## 2. 关系说明

- 一个 `CUSTOMER` 可拥有多张 `INVOICE`。
- 每张 `INVOICE` 在一次流程中对应一个 `RISK_ASSESSMENT`。
- 每个 `RISK_ASSESSMENT` 生成一个 `COLLECTION_STRATEGY`。
- 一个策略可触发多个 `EXECUTION_ACTION`（例如重试、升级动作）。
- 每个执行动作会产生多个 `AUDIT_EVENT` 用于追踪和审计。

## 3. 关键字段约束

- `risk_level`：`low | medium | high`
- `confidence`：`0.0 - 1.0`
- `action_status`：`queued | sent | failed | skipped`
- `event_type`：`decision | execution | fallback | error`

## 4. 审计最小必填字段

每条 `AUDIT_EVENT.payload_json` 至少包含：
- `invoice_id`
- `customer_id`
- `risk_level`
- `reasons`
- `next_action`
- `status`

## 5. MVP 实现建议

- 数据层先用 JSON/内存对象模拟，保持与该 ERD 字段一致。
- 正式接入数据库时，优先落地：
  - `invoice`
  - `risk_assessment`
  - `collection_strategy`
  - `audit_event`