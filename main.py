from fastapi import FastAPI
from app.api.endpoints import (sources_router, 
                              keywords_router,
                              posts_router, 
                              generate_router)

app = FastAPI()

app.include_router(sources_router)
app.include_router(keywords_router)
app.include_router(posts_router)
app.include_router(generate_router)

