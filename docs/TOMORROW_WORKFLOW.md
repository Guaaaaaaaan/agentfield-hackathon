# TOMORROW_WORKFLOW.md

## Date and Deadline
- Date: **2026-02-07 (SGT)**
- Submission deadline: **15:30 SGT**

## One-Line Operating Mode
You orchestrate. Codex executes most coding tasks. Claude Code reviews and quality-gates.

## Fixed Roles (Do Not Change Midway)

### You
- Decide priorities
- Copy task cards between Codex and Claude Code
- Approve final submit

### Codex
- Implement the assigned coding task
- Return changed files, commands, results, blockers
- Apply fixes after Claude Code review feedback

### Claude Code
- Review Codex output with PASS/FAIL
- Focus on correctness, regressions, edge cases, and missing tests
- Return minimal fix list with clear file-level actions

## Main Time Blocks (SGT)

### 10:30-12:30
- Only one goal: end-to-end MVP flow runs once
- No polishing, no UI expansion

### 13:00-14:00
- Stabilize and add fallback
- Ensure English-only output for demo

### 14:00-14:45
- Rehearse demo (3-minute + 90-second backup)
- Run judge Q&A prep

### 14:45-15:15
- Freeze features
- Only P0 fixes

### 15:15-15:30
- Final checklist and submission

## Loop Per Task (20-40 Minutes)

1. Ask Codex for one smallest coding task and have Codex implement it.
2. Paste Codex result to Claude Code for strict review.
3. Get Claude PASS/FAIL and fix list.
4. If FAIL, send fix list back to Codex for patching.
5. Continue only after Claude Code returns PASS.

## Prompt Templates (Copy/Paste)

### A) Ask Codex for the next task
```text
按 MVP 目标，请你直接完成下一步唯一最高优先编码任务（30分钟内），并返回：
1) 要改的文件
2) 实际改动
3) 运行了什么命令
4) 当前结果与阻塞
```

### B) Send Codex result to Claude Code (review)
```text
请对以下 Codex 改动做严格代码审查，返回：
1) PASS/FAIL
2) 按严重级别排序的问题列表（含文件）
3) 最小修复任务卡（只保留必须改）
[粘贴 Codex 执行结果]
```

### C) Ask Codex to fix Claude review findings
```text
按以下 Claude 审查意见修复，保持最小改动，完成后返回：
1) 修复了哪些问题
2) 改了哪些文件
3) 验证结果
[粘贴 Claude 审查意见]
```

## Hard Rules

1. Never let Codex and Claude Code edit the same file in parallel.
2. If MVP flow is not stable, do not add features.
3. Demo screen output must be English-only.
4. If blocked for >15 minutes, switch to fallback path immediately.

## Priority Order for Tomorrow

1. Run core flow once
2. Make core flow stable
3. Rehearse demo
4. Submit

## Start Command (Tomorrow First Action)

At session start, send this to Codex:

```text
今天是 2026-02-07，我按 TOMORROW_WORKFLOW.md 执行。
你作为主开发先完成第一个 30 分钟编码任务（MVP 主链路优先），然后我交给 Claude Code 做审查。
```

## 4-CLI Parallel Mode (Recommended)

Use 1 controller + 2 coding executors + 1 dedicated reviewer. Do not run overlapping file edits.

### Role Split

- CLI-1 (Controller): planning, task dispatch, acceptance checks, integration decisions. No business-code edits.
- CLI-2 (Codex Coding Lane A): `src/agents/` + `src/orchestration/`
- CLI-3 (Codex Coding Lane B): `src/models/` + `data/samples/` + `tests/`
- CLI-4 (Claude Review Lane): review only (`PASS/FAIL`, findings, minimal fix card)

### Hard Parallel Rules

1. No overlapping file edits across CLIs.
2. Every coding round must pass Claude review before merge/integration.
3. No new feature after 14:45 SGT; P0 fixes only.
4. Demo-visible output must remain English-only.

### Round Structure

- Round 1 (30 min): freeze output contract and file ownership.
- Round 2-3: parallel implementation by CLI-2/3, review by CLI-4.
- Round 4: integrate only Claude-PASS changes and stabilize.
- Final round: demo rehearsal + submission checklist.

### First Message to Controller CLI

```text
按 4-CLI 并行模式给我第 1 轮任务卡（Codex主开发 + Claude审查）：
1) 每个 CLI 的唯一任务（含审查任务）
2) 文件边界（禁止重叠）
3) 30 分钟验收标准
4) 集成顺序
```
