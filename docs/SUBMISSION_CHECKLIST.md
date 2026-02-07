# SUBMISSION_CHECKLIST.md

## 0. 提交目标

在截止前提交一个 **可运行 + 可演示 + 可解释** 的 MVP 包。

---

## 1. 代码与运行检查

- [ ] 主链路可运行：`Overdue Invoice -> Risk -> Strategy -> Execute + Audit`
- [ ] 本地连续运行 3 次无崩溃
- [ ] 关键输出字段齐全：`risk_level/confidence/reasons/next_action`
- [ ] 失败场景有 fallback（不因单点失败中断全流程）
- [ ] 样例数据可直接复用演示

## 2. 文档检查

- [ ] 根目录 `README.md` 可独立指导复现
- [ ] `docs/PRD.md` 完整描述需求范围与验收标准
- [ ] `docs/ERD.md` 与实际数据结构一致
- [ ] `docs/FINAL_MVP_SUBMISSION_PLAN.md` 与当前实现一致
- [ ] `docs/DEMO_SCRIPT.md` 已彩排（至少 2 次）

## 3. 安全与合规检查

- [ ] 未提交 `.env` 或任何明文密钥
- [ ] 日志中无敏感信息（邮箱、手机号、账户标识）
- [ ] 演示数据为脱敏样例
- [ ] 没有高风险写操作直连生产环境

## 4. 提交资产清单

- [ ] 代码仓库（可运行）
- [ ] README（安装、运行、示例输出）
- [ ] PRD + ERD + MVP Plan
- [ ] Demo 讲稿（90 秒版 + 3 分钟版）
- [ ] 演示备份材料（离线输出或短视频）

## 5. 评分映射核对

- [ ] New Problem Space：明确说明“AI backend reasoning layer”
- [ ] Replaced Complexity：说明替代了哪些硬编码/人工流程
- [ ] High Leverage：说明高频可复用场景和业务杠杆
- [ ] Previously Hard：说明动态策略 + 可解释审计为何以前难做

## 6. 最后 30 分钟流程（建议）

### T-30 ~ T-20
- [ ] 冻结功能，不再新增需求
- [ ] 仅修复 P0 问题

### T-20 ~ T-10
- [ ] 完整走一遍演示流程
- [ ] 检查提交内容完整性

### T-10 ~ T-0
- [ ] 最终提交
- [ ] 备份提交材料到本地和云端

## 7. 阻塞应急预案

- 模型超时：切换 fallback 策略
- 网络异常：切换离线演示
- 环境故障：切换备机或录屏演示
- 时间不够：删增强项，只保主链路
## 8. Demo 语言门禁（强制）

- [ ] 演示时屏幕输出仅英文（English-only）
- [ ] `reasons/next_action/audit_event` 全部英文
- [ ] 无中文错误信息/回退提示泄露到屏幕
- [ ] 演示前已做一次 English-only 彩排
