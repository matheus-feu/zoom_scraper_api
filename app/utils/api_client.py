from typing import Optional, Dict, Any

import requests


class APIClient:
    """Classe responsável por interagir com a API"""

    def __init__(self, base_url: str):
        self.base_url = base_url

    def get(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """Realiza uma requisição GET para a API"""
        try:
            response = requests.get(f"{self.base_url}/{endpoint}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return None

    def fetch_all_products(self, term: str) -> Optional[Dict[str, Any]]:
        """Fetch all products from the API"""
        return self.get(f"api/v1/search?term={term}")

    def fetch_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a product by ID from the API"""
        return self.get(f"api/v1/product/{product_id}")

    def fetch_product_by_id_stores(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a product by ID and its prices in other stores from the API"""
        return self.get(f"api/v1/product/{product_id}/stores")
