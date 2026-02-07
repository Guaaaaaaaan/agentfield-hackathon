# Architecture Overview

本目录用于管理 MVP 的架构资产：
- 架构图（流程/上下文）
- ADR（架构决策记录）
- 契约（输入输出规范）
- Runbook（故障处置）

## 目录说明

- `diagrams/`：Mermaid 架构图
- `adrs/`：架构决策记录（ADR）
- `contracts/`：模块间数据契约
- `runbooks/`：稳定性与故障预案

## MVP 架构原则

1. Reasoner 只负责判断与选择。
2. Skill 只负责确定性执行。
3. 决策输出必须结构化并可审计。
4. 任一模块失败时有 fallback，不中断整链路。

## 对应代码目录（已创建）

- `src/agents/`
- `src/orchestration/`
- `src/models/`
- `src/skills/`
- `src/services/`
- `src/common/`
- `data/samples/`
- `tests/unit/`
- `tests/integration/`
- `scripts/`