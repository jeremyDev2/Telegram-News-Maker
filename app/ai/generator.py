from app.ai.openai_client import complete

PROMPT =  """\
Напиши короткий, цікавий пост для Telegram-каналу на основі цієї новини.
Додай 1-2 емодзі та заклик до дії в кінці (наприклад, підписатись на канал).

Новина:
{raw_text}
"""

async def generate_post(raw_text:str) -> str:

    prompt = PROMPT.format(raw_text=raw_text)
    return await complete(prompt)
