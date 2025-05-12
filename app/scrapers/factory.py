from app.scrapers.zoom_scraper import ProductDetailsScraper, ProductOffersScraper, SearchProductScraper


class ScraperFactory:
    _scraper_map = {
        "search": SearchProductScraper,
        "details": ProductDetailsScraper,
        "offers": ProductOffersScraper,
    }

    @staticmethod
    def create_scraper(scraper_type: str):
        try:
            return ScraperFactory._scraper_map[scraper_type]()
        except KeyError:
            raise ValueError(f"Scraper type '{scraper_type}' is not recognized.")
