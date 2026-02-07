# ENV_TEMPLATE.md

## 1. 本地 `.env` 模板

> 注意：`.env` 不可提交到仓库。

```env
# App
APP_ENV=dev
APP_PORT=8000
LOG_LEVEL=INFO
DEMO_MODE=true
DEMO_ENGLISH_ONLY=true

# AI
MODEL_PROVIDER=openai
MODEL_NAME=gpt-4.1-mini
OPENAI_API_KEY=<your_key>

# Database
DB_PROVIDER=sqlite
DATABASE_URL=sqlite:///data/app.db

# Optional PostgreSQL
# DB_PROVIDER=postgres
# DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Runtime guards
REQUEST_TIMEOUT_SEC=20
MAX_RETRIES=1
ENABLE_FALLBACK=true

# Output constraints
OUTPUT_LANGUAGE=en-US
```

## 2. 线上 Secret 模板（平台环境变量）

必须配置：
- `OPENAI_API_KEY`
- `DATABASE_URL`（若接云 DB）
- `DEMO_ENGLISH_ONLY=true`
- `OUTPUT_LANGUAGE=en-US`

建议配置：
- `REQUEST_TIMEOUT_SEC`
- `ENABLE_FALLBACK`
- `LOG_LEVEL`

## 3. Demo 语言强约束

明天演示时，确保：
- `DEMO_ENGLISH_ONLY=true`
- `OUTPUT_LANGUAGE=en-US`

如发现输出非英文：
1. 检查变量是否生效
2. 重新启动进程
3. 使用 `OUTPUT_LANGUAGE_POLICY.md` 里的 guardrail prompt

## 4. 安全注意

- 不要提交 `.env`
- 不要在日志打印 API Key
- 平台上使用 Secret 管理，不写死在代码里
