import asyncio
from openai import AsyncOpenAI, APIError, RateLimitError

from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def complete(prompt: str) -> str:
    last_error = None
    for attempt in range(settings.OPENAI_MAX_RETRIES):
        try:
            response = await client.chat.completions.create(
                model = settings.OPENAI_MODEL,
                messages= [{"role":"user", "content":prompt}],
            )
            return response.choices[0].message.content
        except (RateLimitError, APIError) as e:
            last_error = e
            if attempt < settings.OPENAI_MAX_RETRIES - 1:
                await asyncio.sleep(2 ** attempt)
    raise last_error
