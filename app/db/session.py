from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(

    str(settings.DATABASE_URL),
    pool_size = 5,
    max_overflow = 5,
    pool_pre_ping = True,
    pool_timeout = 5,
    pool_recycle = 1800

)

session_factory = async_sessionmaker(
    
    engine,
    ## after ended session(async session),we can't make query's to DB, so we mark this False
    expire_on_commit=False

)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_factory() as session: 
        yield session
