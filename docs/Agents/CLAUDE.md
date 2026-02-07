# CLAUDE.md — AgentField Hackathon 作战版（MVP First）

## 1. 项目定位

- **Hackathon**: AgentField Hackathon
- **比赛日期**: **2026-02-07 (SGT)**
- **提交截止**: **2026-02-07 15:30 SGT**
- **项目名**: Intelligent Billing Operations Engine
- **一句话**: 用 AgentField 在账单后端构建“会推理的运营层”，替代硬编码规则和人工串行处理。

## 2. 先赢再扩：明天只做一个杀手流程

只做这条主流程（必须跑通）：

`逾期发票 -> 异常与风险推理 -> 自动生成催收策略 -> 执行动作 + 审计记录`

不做（明天先砍掉）：

- 全量对账系统
- 多渠道真实消息发送集成
- 复杂前端界面
- 过多 Agent（>3）

## 3. MVP Agent 架构（3 个就够）

### A. `invoice_risk_reasoner`（Reasoner）

- 输入: 发票 + 客户历史 + 最近支付行为
- 输出: `risk_level`, `reasons`, `confidence`
- 作用: 替代大量逾期/异常 if-else 规则

### B. `collection_strategy_reasoner`（Reasoner）

- 输入: `risk_level` + 客户偏好 + 账龄
- 输出: `channel`, `tone`, `next_action`, `escalation`
- 作用: 从固定催收脚本升级为上下文决策

### C. `execute_and_audit_skill`（Skill）

- 输入: 催收策略
- 执行: 模拟发送动作（email/sms/call queue）
- 输出: 审计事件（时间、策略、原因、执行状态）

## 4. Reasoner vs Skill 边界（必须清晰）

- **Reasoner**: 做“判断和选择”
- **Skill**: 做“确定性执行”
- **Memory**: Agent 之间共享状态（风险、策略、证据）
- **Discovery**: 按能力名调用，不写死服务路由

## 5. 为什么这个题更容易拿分

对应评审标准：

1. **New problem space**: 不是聊天机器人，而是账单运营后端决策层。
2. **Replaced complexity**: 把硬编码规则和人工工单流替换为推理 + 自动执行。
3. **High leverage**: 每张逾期发票都会跑，频率高、业务价值直接。
4. **Previously impossible**: 能根据历史效果动态调整催收策略，不是静态规则能轻松做到的。

## 6. Demo 设计（3 分钟固定脚本）

### 0:00 - 0:30 问题

- 传统账单运营依赖规则 + 人工判断
- 结果: 维护成本高、响应慢、策略僵化

### 0:30 - 1:30 架构

- 展示 3 个 Agent：
  - `invoice_risk_reasoner`
  - `collection_strategy_reasoner`
  - `execute_and_audit_skill`
- 强调：Reasoner 决策，Skill 执行，Memory 共享证据

### 1:30 - 2:30 现场跑一次

- 输入 1~3 条样例逾期发票
- 输出风险等级与策略差异（高风险 vs 中风险）
- 展示审计日志（可解释）

### 2:30 - 3:00 收尾量化

- “过去: 规则树 + 手工决策；现在: 推理后端自动给出策略和执行动作”
- 给出 2~3 个量化指标（示例）：
  - 策略生成时间: 分钟级 -> 秒级
  - 规则维护点数: 大幅减少
  - 高风险工单覆盖率: 提升

## 7. 今晚执行清单（按优先级）

1. 搭最小工程骨架（`src/agents/`, `src/models/`, `src/orchestration/`, `data/samples/`, `tests/`）。
2. 先跑通单条主流程（1 条发票输入，3 个 Agent 全链路输出）。
3. 准备 5~10 条高质量样例数据（低/中/高风险各有）。
4. 加审计输出，保证每次决策都有原因文本。
5. 录一条 30~60 秒 fallback demo 视频（现场网络异常可兜底）。

## 8. 明天现场分工建议（<=6 人）

- 1 人: Agent 编排与 Memory
- 1 人: 风险/策略提示词与输出结构
- 1 人: Skill 执行与审计日志
- 1 人: 样例数据与评估指标
- 1 人: Demo 与讲述
- 1 人: 机动（修 bug / 集成）

## 9. 项目结构（精简版）

```text
agentfield_Hackthon/
├── README.md
├── architecture/
│   ├── diagrams/
│   ├── adrs/
│   ├── contracts/
│   └── runbooks/
├── docs/
│   ├── PRD.md
│   ├── ERD.md
│   ├── FINAL_MVP_SUBMISSION_PLAN.md
│   ├── OPERATING_PLAN.md
│   ├── DEMO_SCRIPT.md
│   ├── FINAL_DEMO_FLOW.md
│   ├── SUBMISSION_CHECKLIST.md
│   ├── OUTPUT_LANGUAGE_POLICY.md
│   └── Agents/
│       └── CLAUDE.md
├── src/
│   ├── agents/
│   ├── orchestration/
│   ├── models/
│   ├── skills/
│   ├── services/
│   └── common/
├── data/
│   └── samples/
├── tests/
│   ├── unit/
│   └── integration/
└── scripts/
```

## 10. 快速启动（按你本机环境）

```bash
# Python 环境
python -m venv .venv
.venv\\Scripts\\activate
pip install agentfield pydantic

# 若 AgentField CLI 可用
af dev
```

如果 `af` 不可用，先用 Python 入口跑通核心流程：

```bash
python app.py
```

## 11. 编码硬约束（比赛版）

- 全部数据结构强类型（Pydantic）。
- Reasoner 输出必须结构化（不要自由文本）。
- 每个决策必须带 `reasons` 字段（便于评委看可解释性）。
- 每个 Skill 调用都写审计日志。
- 演示屏幕上所有 AI 输出必须英文（English-only）。
- 先稳定，再扩展；明天中午前不要新增第 4 个 Agent。

## 12. 评委面前的一句话

`This is not an AI chatbot. This is an AI reasoning layer embedded in billing backend operations, replacing brittle hardcoded workflows with context-aware autonomous decisions.`
