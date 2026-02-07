# Incident Runbook (MVP)

## 常见故障与处置

1. 模型超时
- 现象：Reasoner 调用超时
- 处置：切换 fallback；记录 `fallback=true`

2. 输出不合法
- 现象：缺失 `risk_level/reasons`
- 处置：结构校验失败后重试一次；仍失败则 fallback

3. 演示环境网络异常
- 现象：外部依赖不可用
- 处置：切换本地样例与预生成输出

## 终止条件
- 连续 3 次关键链路失败后停止实时调用，进入离线演示模式。