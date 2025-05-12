from app.core.logs import logger
from app.scrapers.backend import ScraperBackend


class ProductSearchService:
    @classmethod
    async def get_product_details(cls, product_id: int):
        """
        Get product details from the scraper.
        :param product_id:
        :return:
        """
        logger.info(f"Getting product details for product id: {product_id}")

        scraper = ScraperBackend("details")
        product_details = await scraper.execute(product_id)
        if not product_details:
            logger.warning(f"No details found for product id: {product_id}")
            return None
        return product_details

    @classmethod
    async def get_product_offers(cls, product_id: int) -> list[dict]:
        """
        Get product offers from the scraper.
        :param product_id:
        :return:
        """
        logger.info(f"Getting product offers for product id: {product_id}")

        scraper = ScraperBackend("offers")
        product_offers = await scraper.execute(product_id)
        if not product_offers:
            logger.warning(f"No stores found for product id: {product_id}")
            return []
        return product_offers
