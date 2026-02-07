# ADR-001: Reasoner-Skill 边界

## 状态
Accepted

## 决策
- `invoice_risk_reasoner` 与 `collection_strategy_reasoner` 只输出结构化判断。
- `execute_and_audit_skill` 负责执行动作与记录审计。

## 理由
- 降低耦合，提升可测试性。
- 避免模型直接执行不可控动作。
- 满足可解释与可审计要求。