from telethon import TelegramClient

from app.config import settings
from app.db.enums import PostStatus
from app.db.models import Post

async def publish_post(post: Post) -> bool:

    client = TelegramClient(
        "bot_session",
        settings.TELEGRAM_API_ID,
        settings.TELEGRAM_API_HASH,
    )
    # connect manually instead of "async with client" - that calls start()
    # with no args and prompts interactively for a phone number
    await client.connect()
    try:
        await client.start(bot_token=settings.TELEGRAM_BOT_TOKEN)
        await client.send_message(settings.TELEGRAM_PUBLISH_CHANNEL, post.generated_text)
        return True
    except Exception:
        return False
    finally:
        await client.disconnect()
