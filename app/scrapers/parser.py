import re
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class Parser(ABC):
    def __init__(self, html: str):
        self.soup = BeautifulSoup(html, "html.parser")

    @abstractmethod
    def parser(self):
        """Parse the HTML content and return the relevant data."""
        pass

    def get_text(self, selector: str, scope=None):
        """Get the text content of the first matching element."""
        element = (scope or self.soup).select_one(selector)
        return element.get_text(strip=True) if element else None

    def get_attribute(self, selector: str, attribute: str, scope=None):
        """Get the value of the specified attribute from the first matching element."""
        element = (scope or self.soup).select_one(selector)
        return element[attribute] if element and attribute in element.attrs else None


class SearchParser(Parser):
    """
    Parse the search results from the HTML content.
    Localiza a sessão de resultados da busca e extrai as informações relevantes.
    """

    def parser(self):
        products = []

        product_cards = self.soup.select(".Hits_ProductCard__Bonl_")
        for item in product_cards:

            name_element = item.select_one("h2.ProductCard_ProductCard_Name__U_mUQ")
            if name_element:
                id_product = name_element.get("id", "").split("::")[0].replace(
                    "product-card-", "") if name_element else None
                name_product = name_element.text.strip().replace("\\", "") if name_element else None

                price_source = item.select_one("h3.ProductCard_ProductCard_BestMerchant__JQo_V")
                price_source_text = price_source.text.strip() if price_source else None

                price_element = item.select_one("p[data-testid='product-card::price']")
                price_text = price_element.text.strip() if price_element else None
                price_value = (
                    float(price_text.replace("R$", "").replace(".", "").replace(",", ".").strip())
                    if price_text else None
                )

                installment_element = item.select_one("span.ProductCard_ProductCard_Installment__XZEnD")
                installment_text = installment_element.text.strip() if installment_element else None

                ratings_element = item.select_one("div[data-testid='product-card::rating']")
                ratings_text = ratings_element.text.strip() if ratings_element else None

                products.append({
                    "id": id_product,
                    "name": name_product,
                    "description": price_source_text,
                    "price": price_value,
                    "installments": installment_text,
                    "ratings": ratings_text,
                    "image_url": item.select_one("img")["src"] if item.select_one("img") else None,
                    "detail_url": item.select_one("a")["href"] if item.select_one("a") else None
                })

        return products


class ProductDetailsParser(Parser):
    """
    Parse the product details from the HTML content.
    Localiza a sessão de detalhes técnicos do produto e extrai as informações relevantes.
    Obtém os detalhes técnicos do produto de acordo com a estrutura HTML da página.
    :param html:
    :return:"
   """

    def parser(self):
        details = {}

        content_section = self.soup.select_one("div[data-testid='detailsSection-masonry']")
        if content_section:
            attribute_blocks = content_section.select("div.DetailsContent_AttributeBlock__lGim_")
            for block in attribute_blocks:
                group_title = block.select_one("h3.AttributeBlock_GroupTitle__XIqmq")
                group_name = group_title.text.strip() if group_title else "Outros"

                if group_name not in details:
                    details[group_name] = {}

                if group_name == "Descrição":
                    description_content = block.select_one("div.AttributeBlock_GroupContent__rKxrs p")
                    if description_content:
                        details[group_name] = description_content.text.strip()

                rows = block.select("tr.Row_Row__kKYw6")
                for row in rows:
                    attribute_name = row.select_one("th.AttributeName_Key__JJU2r span")
                    attribute_value = row.select_one("td.AttributeValues_Value__iqjHN span")

                    if attribute_name and attribute_value:
                        name = attribute_name.text.strip()
                        value = attribute_value.text.strip()
                        details[group_name][name] = value

        else:
            description_section = self.soup.select_one("section.DetailsSection_DetailsSection__4RLSH")
            if description_section:
                description_element = description_section.select_one(
                    "div.DetailsContentSimplified_ContentSimplified__2Rszi p")
                if description_element:
                    details["Descrição"] = description_element.text.strip()

        return details if details else None


class ProductOffersParser(Parser):
    """
    Parse the product offers from the HTML content.

    Localiza a sessão de ofertas do produto e extrai as informações relevantes.
    Obtém as ofertas do produto de acordo com a estrutura HTML da página.
    :param html:
    :return:
    """

    def parser(self):
        offers = []
        offer_cards = self.soup.select("div[data-testid='offer-card-wrapper']")
        for card in offer_cards:
            price_text = self.get_text("a[data-testid='offer-price'] .OfferPrice_InCash___m2LM", card)
            if price_text:
                match = re.search(r"[\d.,]+", price_text)
                cleaned_price = match.group(0).replace(".", "").replace(",", ".") if match else None
                price_value = float(cleaned_price) if cleaned_price else None

            offers.append({
                "price": price_value,
                "store_name": self.get_text("a[data-testid='offer-merchant'] h3", card),
                "purchase_link": self.get_attribute("a[data-testid='offer-price']", "href", card)
            })
        return offers if offers else None
