# PRD.md — Intelligent Billing Operations Engine (MVP)

## 1. 背景与问题

账单运营对逾期发票处理依赖静态规则与人工经验：
- 难以快速适配不同客户和账龄场景
- 规则维护成本持续上升
- 缺乏统一可解释证据链，审计成本高

## 2. 产品目标

构建一个可演示的 AI Backend MVP，让系统能够：
1. 自动识别逾期风险等级
2. 自动生成催收策略
3. 自动执行模拟动作并记录审计事件

## 3. 用户与场景

### 目标用户
- Billing Ops / Collection Ops
- Finance Compliance Reviewer
- Engineering Maintainer

### 核心场景
- 当发票进入逾期状态时，系统自动评估风险并建议/执行策略。

## 4. 范围定义

### In Scope（MVP）
- 单流程：逾期发票 -> 风险推理 -> 策略推理 -> 执行与审计
- 结构化决策输出
- 样例数据驱动演示

### Out of Scope（MVP）
- 实际支付网关和外部渠道生产联调
- 自动扣款等高风险写操作
- 多租户与复杂权限系统

## 5. 功能需求（Functional Requirements）

### FR-1 风险推理
- 输入：发票、客户历史、支付行为
- 输出：`risk_level`, `confidence`, `reasons`

### FR-2 策略推理
- 输入：风险结果、客户偏好、账龄
- 输出：`channel`, `tone`, `next_action`, `escalation`

### FR-3 执行与审计
- 输入：策略对象
- 行为：模拟执行动作
- 输出：`status`, `audit_event`

### FR-4 可解释性
- 每次推理必须提供非空 `reasons`

### FR-5 流程稳定性
- 任一模块失败时，系统进入 fallback，不得整链路中断

## 6. 非功能需求（NFR）

- NFR-1 端到端单条处理延迟：<= 8 秒
- NFR-2 主链路成功率：>= 95%
- NFR-3 输出必须结构化（可被程序消费）
- NFR-4 审计日志完整且可追溯

## 7. 数据与契约

核心实体：
- Customer
- Invoice
- RiskAssessment
- CollectionStrategy
- ExecutionAction
- AuditEvent

字段约束参考：`ERD.md`

## 8. 验收标准（MVP）

- 至少 6 条样例（低/中/高风险）跑通
- 结果字段齐全：`risk_level/confidence/reasons/next_action`
- 审计事件具备时间戳、策略、执行状态
- Demo 3 分钟内可完成演示

## 9. 里程碑

- M1：数据模型与契约冻结
- M2：三模块实现
- M3：主链路联调通过
- M4：文档与 Demo 完成

## 10. 风险与缓解

- 模型不稳定：固定样例 + fallback 策略
- 网络异常：本地离线演示
- 时间不足：冻结范围，只保主链路

## 11. 发布与回滚

- 发布标记：`v0.1.0-mvp`
- 回滚策略：切换本地规则兜底，保留可解释日志