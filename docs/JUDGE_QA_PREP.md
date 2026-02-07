# JUDGE_QA_PREP.md

## English Q&A

### Q1. How is this different from a normal LLM chatbot?
A: It is a backend reasoning layer. Input is business objects (invoice/behavior), output is structured decisions plus audit events.

### Q2. Why this problem matters?
A: Overdue handling is high-frequency and directly impacts cash flow, so automation has strong leverage.

### Q3. What complexity did you replace?
A: Growing hardcoded rule trees and manual triage workflows.

### Q4. How do you ensure explainability?
A: Decision output must include non-empty `reasons`, and all actions are logged as audit events.

### Q5. How do you keep it controllable?
A: Reasoners decide, Skills execute deterministic actions, with fallback and audit guardrails.

### Q6. What if model output is unstable?
A: We switch to fallback strategy and mark `fallback=true` while keeping the pipeline alive.

### Q7. How do you address compliance?
A: Every action emits traceable events with timestamp, strategy, status, and rationale.

### Q8. Is this real production data?
A: No. Demo uses masked sample data. Production integration follows least-privilege and data masking.

### Q9. Is it scalable?
A: Yes. Contracts are structured, so we can add channels and strategies incrementally.

### Q10. What is MVP success?
A: Stable end-to-end run, complete output contract, and a reproducible 3-minute demo.

## 中文问答

### Q1. 这和普通 LLM 聊天机器人有什么不同？
A：它是后端推理层，输入是业务对象，输出是结构化决策和审计事件。

### Q2. 这个问题为什么值得做？
A：逾期处理高频且影响现金流，自动化决策杠杆很高。

### Q3. 你们替代了什么复杂度？
A：替代了不断膨胀的硬编码规则树和人工串行处理。

### Q4. 如何保证可解释性？
A：决策输出强制包含 `reasons`，并记录结构化审计事件。

### Q5. 如何保证可控性？
A：Reasoner 只判断，Skill 只执行，并有 fallback 与审计护栏。

### Q6. 模型不稳定怎么办？
A：启用 fallback 并标记 `fallback=true`，确保链路不中断。

### Q7. 如何满足合规与审计？
A：每次动作都记录可追溯事件：时间、策略、状态、依据。

### Q8. 使用的是生产数据吗？
A：不是，Demo 用脱敏样例；生产接入遵循最小权限和脱敏策略。

### Q9. 系统可以扩展吗？
A：可以，契约结构化后可逐步扩展策略与执行通道。

### Q10. MVP 成功标准是什么？
A：主链路稳定、输出字段完整、3 分钟 Demo 可复现。