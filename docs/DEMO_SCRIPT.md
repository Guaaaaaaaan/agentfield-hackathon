## Demo Output Language Gate (Mandatory)

For the live demo on 2026-02-07, **all AI outputs shown on screen must be English only**.

Rules:
- Do not output Chinese in runtime responses.
- Keep labels, explanations, reasons, and audit messages in English.
- If user input is Chinese, the system may understand it but must still respond in English in demo mode.
- If a non-English output appears, rerun with enforced English prompt before continuing.

中文说明（仅文档说明，不用于屏幕输出）：
- 明天现场演示时，屏幕上出现的 AI 输出必须全部是英文。
- 即使输入中文，输出也必须是英文。

# DEMO_SCRIPT.md

## English

### Usage
- Use the **3-minute full version** by default.
- If interrupted or short on time, switch to the **90-second version**.
- If network/model is unstable, switch to **offline fallback**.

---

### A. 90-Second Pitch

#### 0:00 - 0:20 Problem
Overdue billing operations rely on hardcoded rules and manual decisions. This causes high maintenance cost, slow response, and weak auditability.

#### 0:20 - 0:50 Solution
We built an AI backend MVP:
`Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute + Audit`

Three modules:
- `invoice_risk_reasoner`
- `collection_strategy_reasoner`
- `execute_and_audit_skill`

#### 0:50 - 1:20 Result
Given one overdue invoice, the system returns structured outputs in seconds:
- `risk_level`
- `confidence`
- `reasons`
- `next_action`
And it writes audit logs for traceability.

#### 1:20 - 1:30 Closing
This is not a chatbot. It is an AI reasoning layer embedded in billing backend operations.

---

### B. 3-Minute Full Script

#### 0:00 - 0:30 Problem
We are building **Intelligent Billing Operations Engine**.
Traditional overdue handling has three issues:
1. Rule trees keep growing and are hard to maintain.
2. Manual decisions are slow.
3. Decisions are hard to explain for audit/compliance.

#### 0:30 - 1:10 Architecture
We split the system into three modules:
1. `invoice_risk_reasoner`: invoice + customer behavior -> risk level + reasons.
2. `collection_strategy_reasoner`: risk + aging -> strategy.
3. `execute_and_audit_skill`: execute action and write audit events.

Key boundary: **Reasoner decides, Skill executes.**

#### 1:10 - 2:10 Live Demo
For one overdue invoice:
1. Input invoice and behavior data.
2. Output `risk_level=high` with reasons.
3. Generate strategy (example: `channel=email + call_queue`, `tone=firm`, `next_action=escalate_after_24h`).
4. Show audit event with timestamp, strategy, and status.

Focus points:
- Structured and explainable decisions.
- Traceable and reproducible execution.

#### 2:10 - 2:40 Judge Mapping
1. New Problem Space: AI backend decision layer, not chatbot UX.
2. Replaced Complexity: replaces hardcoded rules + manual triage.
3. High Leverage: reusable for high-frequency overdue workflows.
4. Previously Hard: dynamic strategy + explainability + auditability together.

#### 2:40 - 3:00 Closing
`This is an AI reasoning layer embedded in billing backend operations.`
It upgrades overdue handling from rule-driven to context-driven with full audit trail.

---

### C. Offline Fallback

Trigger conditions:
- Model timeout
- Network unavailable
- Unstable environment

Fallback steps:
1. Use local fixed sample.
2. Show pre-generated structured output.
3. Clarify that fields/contracts are the same as online mode.

Fallback line:
"The network is unstable right now, so I’m showing an offline replay with the same pipeline contract and outputs."

---

## 中文

### 使用说明
- 默认使用 **3 分钟完整版**。
- 时间紧或被打断时，切换 **90 秒版**。
- 网络/模型不稳定时，切换 **离线兜底版**。

---

### A. 90 秒电梯稿

#### 0:00 - 0:20 痛点
传统逾期处理依赖硬编码规则和人工判断，维护成本高、响应慢、审计困难。

#### 0:20 - 0:50 方案
我们做了 AI Backend MVP：
`Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute + Audit`

三个模块：
- `invoice_risk_reasoner`
- `collection_strategy_reasoner`
- `execute_and_audit_skill`

#### 0:50 - 1:20 结果
输入一条逾期发票后，系统秒级输出结构化结果：
- `risk_level`
- `confidence`
- `reasons`
- `next_action`
并写入审计日志。

#### 1:20 - 1:30 收尾
这不是聊天机器人，而是嵌入账单后端的 AI 推理层。

---

### B. 3 分钟完整版

#### 0:00 - 0:30 问题
我们做的是 **Intelligent Billing Operations Engine**。
逾期处理有三个典型问题：
1. 规则树持续膨胀，维护困难。
2. 人工判断慢。
3. 决策难解释，不利于审计。

#### 0:30 - 1:10 架构
系统拆成三模块：
1. `invoice_risk_reasoner`：发票+客户行为 -> 风险等级与原因。
2. `collection_strategy_reasoner`：风险+账龄 -> 催收策略。
3. `execute_and_audit_skill`：执行动作并写审计事件。

关键边界：**Reasoner 判断，Skill 执行。**

#### 1:10 - 2:10 演示
对一条逾期发票：
1. 输入发票与行为数据。
2. 输出 `risk_level=high` 与原因。
3. 生成策略（例如 `email + call_queue`, `tone=firm`, `escalate_after_24h`）。
4. 展示审计事件（时间、策略、状态）。

重点：
- 决策结构化且可解释。
- 执行可追踪、可复现。

#### 2:10 - 2:40 评审映射
1. New Problem Space：后端决策层，不是聊天交互。
2. Replaced Complexity：替代硬编码规则与人工串行流。
3. High Leverage：高频场景复用，价值直接。
4. Previously Hard：动态策略 + 可解释审计同时满足。

#### 2:40 - 3:00 收尾
`This is an AI reasoning layer embedded in billing backend operations.`
它将逾期处理从规则驱动升级为上下文驱动，并保留完整审计链路。

---

### C. 离线兜底

触发条件：
- 模型超时
- 网络不可用
- 环境不稳定

兜底步骤：
1. 使用本地固定样例。
2. 展示预生成结构化输出。
3. 说明线上/离线字段契约一致。

兜底话术：
“现场网络不稳定，我先展示离线复现输出，字段和流程与线上模式一致。”
