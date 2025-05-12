from fastapi import APIRouter

from app.api.v1.product import router as product_router
from app.api.v1.search import router as search_router

api_router = APIRouter()
api_router.include_router(search_router, prefix="/api/v1", tags=["search"])
api_router.include_router(product_router, prefix="/api/v1", tags=["product"])
