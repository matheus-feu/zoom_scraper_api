from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.api import api_router
from app.core.cache import cache_manager
from app.core.config import settings
from app.core.logs import logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("starting lifespan")
    await cache_manager.init_cache()
    yield
    await cache_manager.close_cache()


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    app_version=settings.app_version,
    lifespan=lifespan
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
