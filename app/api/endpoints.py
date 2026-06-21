from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.session import get_session
from app.db.models import Keyword, Post, Source
from app.api.schemas import GenerateRequest, GenerateResponse, KeywordCreate, KeywordRead, SourceCreate, SourceRead, PostRead

sources_router = APIRouter(prefix="/api/sources", tags=["sources"])
keywords_router = APIRouter(prefix="/api/keywords", tags=["keywords"])
posts_router = APIRouter(prefix="/api/posts", tags=["posts"])
generate_router = APIRouter(prefix="/api/generate", tags=["generate"])

@sources_router.post("/", response_model=SourceRead)
async def create_source(data: SourceCreate, 
                        session: AsyncSession = Depends(get_session)
                        ):
    source = Source(**data.model_dump())
    session.add(source)
    await session.commit()
    await session.refresh(source)
    return source

@sources_router.get("/", response_model=list[SourceRead])
async def list_sources(session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(Source))
    return result.scalars().all()

@sources_router.get("/{source_id}", response_model = SourceRead)
async def get_source(source_id: uuid.UUID, 
                     session: AsyncSession = Depends(get_session)):

    source  = await session.get(Source, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found!")
    return source

@sources_router.put("/{source_id}", response_model=SourceRead)
async def update_source(source_id: uuid.UUID, 
                        data: SourceCreate, 
                        session: AsyncSession = Depends(get_session)):

    source = await session.get(Source, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found!")
    # pydantic-scheme date transpile in dict and we can get items
    for field, value in data.model_dump().items():
        setattr(source, field, value)
    await session.commit()
    #needs for take "id" what DB generated
    await session.refresh(source)
    return source


@sources_router.delete("/{source_id}", status_code=204)
async def delete_source(source_id: uuid.UUID, session: AsyncSession = Depends(get_session)):

    source = await session.get(Source, source_id)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found!")
    await session.delete(source)
    await session.commit()

@keywords_router.post("/", response_model=KeywordRead)
async def create_keyword(data: KeywordCreate, 
                         session:AsyncSession = Depends(get_session)):

    keyword = Keyword(**data.model_dump())
    session.add(keyword)
    await session.commit()
    await session.refresh(keyword)
    return keyword

@keywords_router.get("/{keyword_id}", response_model=KeywordRead)
async def get_keyword(keyword_id: uuid.UUID, session: AsyncSession = Depends(get_session)):

    keyword = await session.get(Keyword, keyword_id)
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found!")
    return keyword

@keywords_router.get("/", response_model=list[KeywordRead])
async def list_keywords(session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(Keyword))
    return result.scalars().all()

@keywords_router.delete("/{keyword_id}", status_code=204)
async def delete_keyword(keyword_id: uuid.UUID, session: AsyncSession = Depends(get_session)):

    keyword = await session.get(Keyword, keyword_id)
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found!")
    await session.delete(keyword)
    await session.commit()


@posts_router.get("/{post_id}", response_model=PostRead)
async def get_post(post_id: uuid.UUID, session: AsyncSession = Depends(get_session)):

    post = await session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post is not found!")
    return post

@posts_router.get("/", response_model=list[PostRead])
async def list_posts(session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(Post))
    return result.scalars().all()

@generate_router.post("/", response_model=GenerateResponse)
async def generate_post(data: GenerateRequest):

    return GenerateResponse(generated_text=data.text)
