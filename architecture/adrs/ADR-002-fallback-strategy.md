# ADR-002: Fallback Strategy

## 状态
Accepted

## 决策
- 模型超时/失败时，系统进入 fallback：
  - 使用规则化默认策略
  - 标记 `fallback=true`
  - 继续写审计日志

## 理由
- 保证演示与主链路稳定。
- 避免单点失败导致全流程中断。