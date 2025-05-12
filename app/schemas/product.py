from typing import Optional, List

from pydantic import BaseModel


class ProductSummary(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    installments: str
    ratings: Optional[str] = None
    image_url: str
    detail_url: str


class ProductSearchResponse(BaseModel):
    total_pages: int
    total_products: int
    products: List[ProductSummary]


class StoreDetails(BaseModel):
    price: Optional[float] = None
    store_name: Optional[str] = None
    purchase_link: str
