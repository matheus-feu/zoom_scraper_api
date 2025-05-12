from abc import ABC, abstractmethod

from app.scrapers.parser import SearchParser, ProductOffersParser, ProductDetailsParser


class Scraper(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        """Executa a lógica de scraping."""
        pass


class SearchProductScraper(Scraper):
    async def execute(self, base_url: str, query: str, cache_manager, fetch_url):
        products = []
        page = 1
        total_pages = 0

        while True:
            url = f"{base_url}/search?q={query}&hitsPerPage=48&page={page}&sortBy=default&isDealsPage=false&enableRefinementsSuggestions=true"
            response_text = await fetch_url(url)
            search_parser = SearchParser(response_text)
            page_products = search_parser.parser()

            if not page_products:
                break

            for product in page_products:
                cached_url = await cache_manager.get_cache_value(product["id"])
                if not cached_url:
                    await cache_manager.set_cache_value(product["id"], product["detail_url"], expire=900)

            products.extend(page_products)
            page += 1
            total_pages += 1

        return {"products": products, "total_pages": total_pages, "total_products": len(products)}


class ProductDetailsScraper(Scraper):
    async def execute(self, base_url: str, product_id: int, cache_manager, fetch_url):
        detail_url_bytes = await cache_manager.get_cache_value(product_id)
        if not detail_url_bytes:
            return None

        detail_url = detail_url_bytes.decode("utf-8")
        full_url = f"{base_url}{detail_url}"
        response_text = await fetch_url(full_url)

        details_parser = ProductDetailsParser(response_text)
        return details_parser.parser()


class ProductOffersScraper(Scraper):
    async def execute(self, base_url: str, product_id: int, cache_manager, fetch_url):
        detail_url_bytes = await cache_manager.get_cache_value(product_id)
        if not detail_url_bytes:
            return []

        detail_url = detail_url_bytes.decode("utf-8")
        full_url = f"{base_url}{detail_url}"
        response_text = await fetch_url(full_url)

        offers_parser = ProductOffersParser(response_text)
        return offers_parser.parser()
