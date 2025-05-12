from fastapi import APIRouter, HTTPException, Query, Depends

from app.schemas.product import ProductSearchResponse, ProductSummary
from app.services.search_service import SearchService

router = APIRouter()


@router.get("/search", response_model=ProductSearchResponse)
async def search_products(q: str = Query(..., alias="term"), service: SearchService = Depends()):
    try:
        products = await service.search_products(query=q)
        return {
            "total_pages": products["total_pages"],
            "total_products": products["total_products"],
            "products": [ProductSummary(**p) for p in products["products"]],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
