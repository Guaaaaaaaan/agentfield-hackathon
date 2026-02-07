# Intelligent Billing Operations Engine (MVP)

## English

### Overview
This project is built for the AgentField Hackathon (MVP-first).

One-liner: We add an AI reasoning layer to billing backend operations, upgrading overdue invoice handling from brittle hardcoded rules to explainable, auditable autonomous decisions.

### MVP Demo Flow
`Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute Action + Audit`

Core modules:
- `invoice_risk_reasoner`
- `collection_strategy_reasoner`
- `execute_and_audit_skill`

### Why This Project
Common pain points in traditional billing/collection operations:
- Rule trees keep growing and become expensive to maintain.
- Decisions are hard to explain and audit.
- Response is slow and strategy adaptation is limited.

This MVP focuses on:
- Context-aware decisions by Reasoners.
- Deterministic execution by Skills.
- End-to-end structured audit evidence.

### MVP Scope
In Scope:
- Overdue invoice risk classification (`low`, `medium`, `high`)
- Risk-based collection strategy (`channel`, `tone`, `next_action`)
- Simulated execution actions (`email/sms/call queue`)
- Structured audit logs (`reason`, `action`, `status`, `time`)

Out of Scope:
- Real production messaging provider integration
- Complex frontend UI
- More than 3 agents/modules in MVP

### Required Output Contract
Each flow output must include:
- `risk_level`
- `confidence`
- `reasons`
- `next_action`
- `audit_event`
- `language` (`en-US`)
- `fallback` (`true|false`)

### Project Documents
- MVP submission plan: `docs/FINAL_MVP_SUBMISSION_PLAN.md`
- Operating plan: `docs/OPERATING_PLAN.md`
- Product requirements: `docs/PRD.md`
- Data model / ERD: `docs/ERD.md`
- Demo script: `docs/DEMO_SCRIPT.md`
- Submission checklist: `docs/SUBMISSION_CHECKLIST.md`
- Agent operation notes: `docs/Agents/CLAUDE.md`
- Architecture index: `architecture/README.md`

### Current Project Structure
```text
agentfield_Hackthon/
├── README.md
├── architecture/
├── docs/
│   ├── Agents/
│   ├── PRD.md
│   ├── ERD.md
│   ├── FINAL_MVP_SUBMISSION_PLAN.md
│   ├── OPERATING_PLAN.md
│   ├── DEMO_SCRIPT.md
│   └── SUBMISSION_CHECKLIST.md
├── src/
├── data/
├── tests/
└── scripts/
```

### Quick Start
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API key (required for AI reasoning)
cp .env.example .env
# Edit .env and set your GEMINI_API_KEY

# 3. Run
python app.py              # formatted demo output
python app.py --json       # raw JSON output
python app.py --use-mock   # offline mode (no API key needed)

# 4. Test
python -m pytest -q
```

> **Note:** Without a valid `GEMINI_API_KEY` in `.env`, the system automatically falls back to rule-based reasoning. AI reasoning requires a [Google Gemini API key](https://aistudio.google.com/apikey).

### Demo Input And Expected Output (English)
Demo input (`app.py` default):
- `invoice_id`: `INV-1001`
- `overdue_days`: `52`
- `amount`: `1200.0`
- `late_payments_180d`: `4`

Expected output shape:
- Includes `risk_level`, `confidence`, `reasons`, `next_action`, `audit_event`, `language`, `fallback`
- `language` must be `en-US`

---

## 中文

### 项目简介
这是 AgentField Hackathon 的 MVP 项目（先跑通主链路）。

一句话：在账单后端引入 AI 推理层，把逾期发票处理从硬编码规则流升级为可解释、可审计的自动决策流。

### MVP 演示主链路
`Overdue Invoice -> Risk Reasoning -> Collection Strategy -> Execute Action + Audit`

核心模块：
- `invoice_risk_reasoner`
- `collection_strategy_reasoner`
- `execute_and_audit_skill`

### 为什么做这个项目
传统账单/催收运营常见问题：
- 规则树持续膨胀，维护成本高
- 决策难解释，审计难
- 响应慢，策略难根据上下文动态调整

本 MVP 聚焦：
- Reasoner 做上下文判断
- Skill 做确定性执行
- 全链路保留结构化审计证据

### MVP 范围
In Scope：
- 逾期发票风险分级（低/中/高）
- 按风险生成催收策略（渠道、语气、下一步动作）
- 模拟执行动作（email/sms/call queue）
- 输出结构化审计日志（原因、动作、状态、时间）

Out of Scope：
- 真实消息通道生产联调
- 复杂前端
- MVP 阶段超过 3 个模块

### 关键输出契约
每条流程输出至少包含：
- `risk_level`
- `confidence`
- `reasons`
- `next_action`
- `audit_event`

### 快速开始
```powershell
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 API Key（AI 推理需要）
cp .env.example .env
# 编辑 .env，填入你的 GEMINI_API_KEY

# 3. 运行
python app.py              # 格式化 Demo 输出
python app.py --json       # 原始 JSON 输出
python app.py --use-mock   # 离线模式（不需要 API key）

# 4. 测试
python -m pytest -q
```

> **注意：** 如果 `.env` 中没有有效的 `GEMINI_API_KEY`，系统会自动降级为规则推理。AI 推理需要 [Google Gemini API key](https://aistudio.google.com/apikey)。

### 文档索引
- 最终提交计划：`docs/FINAL_MVP_SUBMISSION_PLAN.md`
- 运营执行计划：`docs/OPERATING_PLAN.md`
- 产品需求：`docs/PRD.md`
- 数据实体关系：`docs/ERD.md`
- Demo 讲稿：`docs/DEMO_SCRIPT.md`
- 提交检查清单：`docs/SUBMISSION_CHECKLIST.md`
- Agent 说明：`docs/Agents/CLAUDE.md`
- 架构文档入口：`architecture/README.md`
