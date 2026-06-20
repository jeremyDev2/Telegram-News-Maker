from pydantic import BaseModel, ConfigDict
import datetime
import uuid

from app.db.enums import PostStatus, SourceType

class SourceCreate(BaseModel):

    type: SourceType
    name: str
    url: str
    enabled: bool = True

class SourceRead(BaseModel):
    # if at the input we have - object(not dict), deliver properties using "getattr(obj, field_name)"
    # instead of using "obj[filed_name]"
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    type: SourceType
    name: str
    url: str
    enabled: bool

#----------------------------------------------------

class PostRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    news_id: uuid.UUID
    generated_text: str
    published_at: datetime.datetime | None
    status: PostStatus

#----------------------------------------------------

class NewsItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    url: str | None
    summary: str
    source: str
    published_at: datetime.datetime
    raw_text: str

#----------------------------------------------------

class KeywordCreate(BaseModel):

    word: str

class KeywordRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    word: str

#----------------------------------------------------

class GenerateRequest(BaseModel):

    text: str

class GenerateResponse(BaseModel):

    generated_text: str
