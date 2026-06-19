from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    #Database
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost:5432/newsbot"

    #Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"

    #OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_RETRIES: int = 3

    #Telethon (user account for reading channels)
    TELEGRAM_API_ID: int = 0
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_SESSION: str = "sessions/bot_session"

    #Bot token for publishing (can also use Telethon user session)
    TELEGRAM_BOT_TOKEN: str = ""

    #Target channel to publish posts (e.g. "@mychannel" or numeric id)
    TELEGRAM_PUBLISH_CHANNEL: str = ""

    #App
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    DEBUG: bool = False

    #News collection interval (minutes)
    COLLECT_INTERVAL_MINUTES: int = 30


settings = Settings()
