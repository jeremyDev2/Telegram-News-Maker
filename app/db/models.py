from app.db import Base
from app.db.enums import PostStatus, SourceType

from sqlalchemy import ForeignKey, Enum
import uuid
import datetime

from sqlalchemy.orm import mapped_column, Mapped


class NewsItem(Base):

    __tablename__ = "news_item"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    url: Mapped[str | None] = mapped_column(default=None)
    summary: Mapped[str] = mapped_column()
    source: Mapped[str] = mapped_column()
    published_at: Mapped[datetime.datetime] = mapped_column()
    raw_text: Mapped[str] = mapped_column()

class Post(Base):
    
    __tablename__ = "posts"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    news_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("news_item.id"))
    generated_text: Mapped[str] = mapped_column()
    published_at: Mapped[datetime.datetime | None] = mapped_column(default=None)
    status: Mapped[PostStatus] = mapped_column(Enum(PostStatus), default=PostStatus.NEW)

class Source(Base):

    __tablename__ = "sources"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    type: Mapped[SourceType] = mapped_column(Enum(SourceType))
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    enabled: Mapped[bool] = mapped_column(default=True)


class Keyword(Base):

    __tablename__ = "keywords"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    word: Mapped[str] = mapped_column(unique=True)
