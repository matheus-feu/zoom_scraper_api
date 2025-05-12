import httpx



async def fetch_url(base_url: str) -> str:
    """
    Constrói a URL completa a partir do base_url e detail_url_bytes e realiza a requisição HTTP.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(url=base_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()
        return response.text
