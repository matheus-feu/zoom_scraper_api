from typing import List

from fastapi import APIRouter, Depends, HTTPException

from app.schemas.product import StoreDetails
from app.services.product_service import ProductSearchService

router = APIRouter()


@router.get("/product/{product_id}")
async def get_product(product_id: int, service: ProductSearchService = Depends()):
    """
    Endpoint para buscar os detalhes de um produto.
    Primeiro verifica o cache, caso não encontre, faz o scraping.
    """
    product_info = await service.get_product_details(product_id)
    if not product_info:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product_info

@router.get("/product/{product_id}/stores", response_model=List[StoreDetails])
async def get_product_stores(product_id: int, service: ProductSearchService = Depends()):
    """
    Endpoint para buscar as demais comparações de preço do produto em outras lojas.
    """
    product_offers = await service.get_product_offers(product_id)
    if not product_offers:
        raise HTTPException(status_code=404, detail="Comparações dos produtos não encontrados")
    return [StoreDetails(**offer) for offer in product_offers]
