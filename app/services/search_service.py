from app.core.logs import logger
from app.schemas.product import ProductSummary
from app.scrapers.backend import ScraperBackend


class SearchService:
    @classmethod
    async def search_products(cls, query: str) -> list[ProductSummary]:
        """Search all products in Zoom using the provided query."""
        logger.info(f"Searching for products with query: {query}")

        scraper = ScraperBackend("search")
        raw_products = await scraper.execute(query)
        if not raw_products:
            logger.warning(f"No products found for query: {query}")
            return []
        return raw_products
