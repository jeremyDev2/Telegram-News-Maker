from telethon import TelegramClient
from app.config import settings
from app.db.models import Source

async def get_messages(source: Source, limit: int = 20) -> list[dict]:

    async with TelegramClient(settings.TELEGRAM_SESSION, 
                              settings.TELEGRAM_API_ID, 
                              settings.TELEGRAM_API_HASH) as client:
        messages = await client.get_messages(source.url, limit=limit)
        return [_message_to_dict(message, source) for message in messages if message.text]

def _message_to_dict(message, source: Source) -> dict:

    return {
        "title": message.text[:100],
        "url": None,
        "summary": message.text[:300],
        "source": source.name,
        "published_at": message.date,
        "raw_text": message.text,
    }
