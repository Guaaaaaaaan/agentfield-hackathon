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

# FINAL_DEMO_FLOW.md

## English

### Goal
Deliver a stable 3-minute story that clearly answers:
1. What problem we solve
2. How we solve it
3. Why it creates real leverage

### Fixed 3-Minute Flow

#### 0:00 - 0:30 Problem
- Overdue handling depends on static rules + manual decisions.
- High maintenance, slow response, weak explainability.

#### 0:30 - 1:10 Solution
- AI backend reasoning pipeline:
  `Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute + Audit`
- Three modules:
  - `invoice_risk_reasoner`
  - `collection_strategy_reasoner`
  - `execute_and_audit_skill`

#### 1:10 - 2:10 Demo
- Input one overdue invoice sample.
- Show structured output: `risk_level/confidence/reasons/next_action`.
- Show execution result + audit event.

#### 2:10 - 2:40 Judge Mapping
- New Problem Space
- Replaced Complexity
- High Leverage
- Previously Hard

#### 2:40 - 3:00 Closing
- This is an AI reasoning layer in billing backend operations.
- Outcome: faster decisions, lower maintenance burden, better auditability.

### 90-Second Backup
1. Pain point (20s)
2. Architecture (30s)
3. Output & impact (30s)
4. Closing (10s)

### Offline Backup
- Use local fixed sample and pre-generated output.
- Explain online/offline contract consistency.

---

## 中文

### 目标
在 3 分钟内稳定传达：
1. 我们解决了什么问题
2. 我们如何解决
3. 为什么这件事有业务杠杆

### 固定 3 分钟流程

#### 0:00 - 0:30 问题
- 逾期处理依赖静态规则 + 人工判断。
- 维护成本高、响应慢、可解释性弱。

#### 0:30 - 1:10 方案
- AI 后端推理链路：
  `Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute + Audit`
- 三个模块：
  - `invoice_risk_reasoner`
  - `collection_strategy_reasoner`
  - `execute_and_audit_skill`

#### 1:10 - 2:10 演示
- 输入一条逾期发票样例。
- 展示结构化输出：`risk_level/confidence/reasons/next_action`。
- 展示执行结果和审计事件。

#### 2:10 - 2:40 评审映射
- New Problem Space
- Replaced Complexity
- High Leverage
- Previously Hard

#### 2:40 - 3:00 收尾
- 这是账单后端中的 AI 推理层。
- 结果：更快决策、更低维护成本、更强审计能力。

### 90 秒备稿
1. 痛点（20s）
2. 架构（30s）
3. 结果与价值（30s）
4. 收尾（10s）

### 离线兜底
- 使用本地固定样例与预生成输出。
- 强调线上/离线字段契约一致。
