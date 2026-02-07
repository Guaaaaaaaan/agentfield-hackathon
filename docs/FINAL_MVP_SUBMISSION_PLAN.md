# FINAL_MVP_SUBMISSION_PLAN.md

## 1. Objective and KPIs

### 项目目标
在 **2026-02-07 15:30 SGT** 前，交付可演示、可复现、可解释的 MVP：
`逾期发票 -> 风险推理 -> 催收策略 -> 执行动作 + 审计记录`

### 成功指标（MVP 级）
- 主链路成功率：`>= 95%`（本地连续跑 20 次）
- 单条样例端到端耗时：`<= 8s`
- 每次决策必须输出：`risk_level + confidence + reasons + next_action`
- Demo 时长：`3 分钟内可完整讲述并跑通`
- 复现门槛：新环境 `<= 10 分钟` 跑起

## 2. Scope

### In Scope（必须）
- 3 个 Agent/模块：
  - `invoice_risk_reasoner`
  - `collection_strategy_reasoner`
  - `execute_and_audit_skill`
- 样例数据（低/中/高风险）
- 结构化输出与审计日志
- 一键运行入口（`python app.py`）
- 最终提交文档（README + 架构图/流程图 + Demo 脚本）

### Out of Scope（本次不做）
- 真实短信/邮件供应商联调
- 复杂 Web 前端
- 超过 3 个 Agent
- 大规模多租户能力

## 3. Architecture and Tooling

### 架构
- **Reasoner 层**：
  - 风险推理（基于发票+客户行为）
  - 策略推理（基于风险+账龄+偏好）
- **Skill 层**：
  - 执行动作（模拟渠道发送）
  - 写审计事件
- **Memory/State**：
  - 在流程上下文共享风险结论、策略、执行状态

### 技术栈
- Python 3.11+
- Pydantic（数据契约）
- Agentfield SDK（可用则接入；不可用则本地流程编排兜底）
- pytest（最小测试）

## 4. Milestones and Timeline (SGT)

### 2026-02-06（今晚）
- M1：冻结 MVP 范围与数据契约
- M2：确认 Demo 脚本与评分映射

### 2026-02-07（比赛日）
- 10:30-11:30：实现模型与 3 个模块骨架
- 11:30-12:30：串联主链路并产出结构化输出
- 13:00-14:00：补样例数据与审计日志展示
- 14:00-14:45：稳定性修复 + fallback
- 14:45-15:15：Demo 彩排（至少 2 次）
- 15:15-15:30：最终打包与提交

## 5. Work Breakdown (Epics -> Tasks)

### Epic A：核心流程
- A1 定义数据模型（Invoice/Customer/Decision/AuditEvent）
- A2 实现风险推理模块
- A3 实现策略推理模块
- A4 实现执行与审计模块
- A5 编排端到端流程入口

### Epic B：数据与验证
- B1 准备 6-10 条样例数据
- B2 定义预期输出样本
- B3 跑主链路回归（>=20 次）

### Epic C：提交资产
- C1 README（安装、运行、示例输出）
- C2 Demo 讲稿（3 分钟）
- C3 评审映射页（问题空间、复杂度替代、杠杆价值、新能力）

## 6. Permissions and Security Constraints

- 默认只读处理样例数据，不接生产数据库写操作。
- 所有密钥使用环境变量；禁止提交 `.env`。
- 输出日志中禁止敏感字段（手机号、邮箱、账号）明文。
- 若接外部 API，必须超时与错误降级。

## 7. Testing and Quality Strategy

- 单元测试：
  - 风险等级映射
  - 策略路由逻辑
  - 审计事件结构
- 集成测试：
  - `app.py` 单输入端到端
- 回归测试：
  - 固定样例 + 固定参数，验证输出结构稳定

质量门槛（DoD）：
1. 输入输出契约一致
2. 异常不导致全链路崩溃
3. 每次决策有可解释 reasons
4. 本地连续 3 次运行无异常

## 8. Observability and Operations

- 结构化日志字段：
  - `trace_id`, `invoice_id`, `risk_level`, `strategy`, `action_status`, `latency_ms`
- 审计日志：记录 `决策原因 + 执行动作 + 时间戳`
- 现场演示模式：支持 `demo_mode=true` 固定样例输入

## 9. Release and Rollback Plan

### 发布
- Tag 候选版本：`v0.1.0-mvp`
- 提交前冻结分支，仅修复 P0 问题

### 回滚
- 若 Agentfield 运行异常：切换本地编排兜底
- 若模型输出不稳定：启用 fallback 规则策略
- 若网络异常：使用本地样例 + 预生成日志演示

## 10. Cost and Capacity Considerations

- MVP 阶段控制在小样本推理，不做大批量处理
- 限制模型调用次数：Demo 单次 <= 10 次推理
- 如模型成本/延迟过高：降级到轻量模型或规则兜底

## 11. Risks and Mitigations

- 风险：模型超时/抖动
  - 处置：超时阈值 + fallback 策略
- 风险：结果不可解释
  - 处置：强制 `reasons` 非空校验
- 风险：现场网络失败
  - 处置：本地离线 demo 包
- 风险：时间不足
  - 处置：只保主链路，冻结增强项

## 12. Acceptance Criteria and Next Actions

### 最终提交前验收（15:20 SGT 前）
- [ ] 主链路可稳定运行
- [ ] 3 分钟 Demo 可讲可跑
- [ ] 关键输出字段齐全（risk/confidence/reasons/action）
- [ ] README 可被他人复现
- [ ] 提交包完整（代码 + 文档 + 演示说明）

### 下一步执行顺序（立即）
1. 先按 Epic A 跑通端到端最小链路
2. 再完成 Epic B 的样例与回归
3. 最后完成 Epic C 的提交资产与彩排