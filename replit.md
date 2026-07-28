# KurdLingo Bot

A Telegram bot for Kurdish language learning (Badini dialect), supporting 10 world languages with gamification, subscription plans, referral system, and certificate generation.

## Stack
- **Language:** Python 3.12
- **Telegram library:** pyTelegramBotAPI (telebot) 4.15.4
- **Database:** SQLite via aiosqlite (async)
- **Scheduling:** APScheduler
- **Image generation:** Pillow + qrcode

## How to run
```
python -m bot.main
```

The workflow **Run Bot** is configured for this command.

## Environment variables
All required values live in `.env` (already populated):
- `BOT_TOKEN` — Telegram bot token
- `ADMIN_ID` / `DEVELOPER_ID` — admin Telegram user IDs
- `DATABASE_URL` — SQLite path (default `data/kurdingo.db`)
- `REDIS_URL` — Redis (optional; not used in the current synchronous telebot setup)
- Payment wallet addresses: `FIB`, `FASTPAY`, `TON_WALLET`, `USDT_TRC20`

## Project structure
```
bot/
  config.py        — Central configuration (loaded from .env)
  database.py      — Async SQLite DB layer (Database class + module-level db & init_database)
  main.py          — Bot entry point; registers handlers and calls bot.infinity_polling()
  handlers/        — Per-feature message/callback handlers
  keyboards/       — Inline and reply keyboard builders
  models/          — Pydantic models for type safety
  services/        — Business logic (lessons, quizzes, certificates, scheduler)
  states.py        — StatesGroup for multi-step conversations
data/              — SQLite DB file, language JSON files, level definitions
utils/             — Shared helpers and validators
```

## User preferences
- Keep the project's existing structure; do not restructure or migrate unless explicitly asked.
