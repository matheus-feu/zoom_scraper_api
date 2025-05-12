from app.core.cache import cache_manager
from app.core.config import settings
from app.scrapers.factory import ScraperFactory
from app.utils.http_client import fetch_url


class ScraperBackend:
    BASE_URL = settings.base_url

    def __init__(self, scraper_type: str):
        self.instance = ScraperFactory.create_scraper(scraper_type)

    async def execute(self, *args, **kwargs):
        return await self.instance.execute(self.BASE_URL, *args, cache_manager=cache_manager, fetch_url=fetch_url)
