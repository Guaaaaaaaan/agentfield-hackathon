# ADR-003: Structured Decision Contract

## 状态
Accepted

## 决策
所有决策输出必须包含：
- `risk_level`
- `confidence`
- `reasons`
- `next_action`

## 理由
- 便于程序消费和测试。
- 提高可解释性与评审可见性。