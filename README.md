# Telegram News Maker

AI-генератор постів для Telegram. Сервіс збирає новини з сайтів та Telegram-каналів,
фільтрує/дедуплікує їх, генерує текст поста через OpenAI і автоматично публікує
в цільовий Telegram-канал. Адміністрування джерел, ключових слів і перегляд
історії постів — через REST API.

## Стек

- **FastAPI** + **granian** (ASGI) — REST API
- **PostgreSQL** + **SQLAlchemy 2.0** (async) + **Alembic** — зберігання даних
- **Celery** + **Redis** — фоновий пайплайн збору/генерації/публікації
- **Telethon** — читання Telegram-каналів (user-сесія) та публікація (bot-сесія)
- **OpenAI** — генерація тексту постів
- **feedparser** / **BeautifulSoup** — парсинг сайтів (RSS, з fallback на HTML-скрейпінг)
- **rapidfuzz** — нечітка дедуплікація новин за заголовком

## Архітектура пайплайну

```
pipeline.run
  ├─ collect.sites      ─┐
  └─ collect.tg         ─┴─> pipeline.merge_collected
                              -> filter.dedup
                              -> generate.post (OpenAI)
                              -> publish.post (Telethon)
```

`celery_beat` запускає `pipeline.run` автоматично кожні `COLLECT_INTERVAL_MINUTES`.

## Запуск

1. Скопіюй `.env.example` у `.env` і заповни значення (Telegram API ID/Hash,
   bot token, OpenAI key, канал публікації тощо).
2. Підніми всі сервіси:
   ```bash
   docker compose up -d
   ```
   Це піднімає `postgres`, `redis`, `app` (FastAPI + granian, з автоматичними
   міграціями при старті), `celery_worker`, `celery_beat`, `flower`.
3. Один раз авторизуй Telethon-сесію для читання каналів (вимагає коду
   підтвердження з Telegram, тому виконується локально, не в контейнері):
   ```bash
   uv run python -c "
   from telethon.sync import TelegramClient
   from app.config import settings
   with TelegramClient(settings.TELEGRAM_SESSION, settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH) as client:
       print('Session ok:', client.is_user_authorized())
   "
   ```
4. Додай бота як адміністратора каналу публікації (`TELEGRAM_PUBLISH_CHANNEL`).

## API

Swagger UI: `http://localhost:8000/docs`

| Endpoint | Опис |
|---|---|
| `POST /api/sources/` | Додати джерело (`type`: `site` або `tg`) |
| `GET /api/sources/` | Список джерел |
| `PUT /api/sources/{id}` | Оновити джерело |
| `DELETE /api/sources/{id}` | Видалити джерело |
| `POST /api/keywords/` | Додати ключове слово для фільтрації |
| `GET /api/keywords/` | Список ключових слів |
| `GET /api/posts/` | Історія згенерованих/опублікованих постів |

Приклад додавання джерела-сайту:
```bash
curl -X POST http://localhost:8000/api/sources/ \
  -H "Content-Type: application/json" \
  -d '{"type": "site", "name": "Ukrainska Pravda", "url": "https://www.pravda.com.ua/rus/news/", "enabled": true}'
```

## Ручний запуск пайплайну

Поза розкладом `celery_beat` пайплайн можна запустити вручну:
```bash
docker compose exec celery_worker uv run python -c "
from app.workers.tasks.pipeline import run_pipeline
run_pipeline.delay()
"
```

## Моніторинг

Flower (стан Celery-задач): `http://localhost:5555`
