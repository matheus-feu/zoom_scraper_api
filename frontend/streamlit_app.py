from typing import Dict, Any, List

import streamlit as st

from app.utils.api_client import APIClient

BASE_URL = "http://api:8000"


class StreamLitApp:
    """Classe responsável pela interface do usuário no Streamlit."""

    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.store_url = "https://www.zoom.com.br"
        self.title = "Scraping Zoom API"
        self.description = "Aplicação para pesquisa de produtos e suas ofertas. \n\n Selecione uma das opções abaixo para começar a pesquisa."

    def display_products(self, products: List[Any]):
        """Exibe a lista de produtos encontrados após a pesquisa."""
        if not products:
            st.write("### Nenhum produto encontrado ou formato inválido.")
            return

        st.write("### Lista de Produtos encontrados")
        for product in products:
            with st.container():
                st.write(f"**ID:** {product['id']}")
                st.write(f"**Nome:** {product['name']}")
                st.write(f"**Preço:** {product['price']}")
                st.write(f"**Parcelas:** {product['installments']}")
                st.write(f"**Avaliações:** {product['ratings']}")

                detail_url = f"{self.store_url}{product['detail_url']}"
                st.markdown(f"[Clique aqui para mais detalhes]({detail_url})", unsafe_allow_html=True)
                st.write(f"**Descrição:** {product['description']}")
                st.image(product['image_url'], caption="Imagem do Produto", use_container_width=True, width=50)
                st.divider()

    @classmethod
    def display_product_details(cls, product: Dict[str, Any]):
        """Exibe os detalhes de um produto específico."""
        if not product:
            st.write("### Nenhum dado encontrado.")
            return

        for key, value in product.items():
            if isinstance(value, dict):
                st.write(f"### {key}")
                st.table([value])
            elif isinstance(value, list):
                st.write(f"### {key}")
                for item in value:
                    st.write(item)
            else:
                st.write(f"### {key}")
                st.write(value)

    def display_product_offers(self, product_offers: Dict[str, Any]):
        """Aba que exibe as ofertas de um produto específico."""
        if not product_offers:
            st.write("### Nenhum dado encontrado.")
            return

        st.write("### Ofertas do Produto")
        for product in product_offers:
            with st.container():
                st.write(f"**Preço:** {product['price']}")
                st.write(f"**Nome Loja:** {product['store_name']}")
                purchase_link = f"{self.store_url}{product['purchase_link']}"
                st.markdown(f"[Clique aqui para mais detalhes]({purchase_link})", unsafe_allow_html=True)
                st.divider()

    def search_products_tab(self):
        """Aba para pesquisa de produtos."""
        st.write("### Pesquisar Produtos")
        st.write("Retorna lista de produtos encontrados com base no termo de pesquisa.")

        search_query = st.text_input(
            "Digite o nome do produto que deseja pesquisar:",
            placeholder="Ex: Smartphone, Notebook, etc.",
            key="search_query_input"
        )
        if st.button("Consultar", key="search_products_button"):
            if not search_query:
                st.error("Por favor, insira um termo de pesquisa.")
                return
            products = self.api_client.fetch_all_products(search_query)
            if products is None:
                st.error("Erro ao buscar produtos. Verifique a conexão com a API.")
                return

            st.session_state["products"] = products.get("products", [])
        else:
            st.session_state.setdefault("products", [])

        self.display_products(st.session_state["products"])

    def search_product_by_id_tab(self):
        """Aba para pesquisa de produto por ID."""
        st.write("### Pesquisar Produto por ID")
        st.write("O resultado retornará os detalhes do produto com base no ID fornecido. \n\n"
                 "Para obter o ID do produto, você pode usar a aba de pesquisa de produtos acima e copiar o ID do produto desejado.")

        product_id = st.number_input(
            "Digite o ID do produto para buscar os detalhes de um produto específico:",
            step=1,
            value=0,
            key="product_id_input"
        )
        if st.button("Consultar", key="search_product_by_id_button"):
            if product_id == 0 or not isinstance(product_id, int):
                st.error("Por favor, insira um ID de produto válido.")
                return
            product = self.api_client.fetch_product_by_id(product_id)
            st.session_state["product_details"] = product
        else:
            st.session_state.setdefault("product_details", None)

        self.display_product_details(st.session_state["product_details"])

    def search_product_by_id_offers_tab(self):
        """Pesquisa de produto por ID e localizar ofertas em outras lojas."""
        st.write("### Pesquisar Ofertas e Preços do Produto em Outras Lojas")
        st.write("Retorna lista de ofertas do produto com base no ID fornecido. \n\n"
                 "Para obter o ID do produto, você pode usar a aba de pesquisa de produtos acima e copiar o ID do produto desejado.")

        product_id_stores = st.number_input(
            "Digite o ID do produto para buscar as ofertas disponíveis em diferentes lojas:",
            step=1,
            value=0,
            key="product_id_stores_input"
        )
        if st.button("Consultar", key="search_product_by_id_stores_button"):
            if product_id_stores == 0 or not isinstance(product_id_stores, int):
                st.error("Por favor, insira um ID de produto válido.")
                return
            product_offers = self.api_client.fetch_product_by_id_stores(product_id_stores)
            st.session_state["product_offers"] = product_offers
        else:
            st.session_state.setdefault("product_offers", None)

        self.display_product_offers(st.session_state["product_offers"])

    def run(self):
        """Executa a aplicação Streamlit."""
        st.title(self.title)
        st.write(self.description)

        if "products" not in st.session_state:
            st.session_state["products"] = []
        if "product_details" not in st.session_state:
            st.session_state["product_details"] = None
        if "product_offers" not in st.session_state:
            st.session_state["product_offers"] = None

        tabs = st.tabs(["Pesquisa", "Detalhes", "Ofertas"])

        with tabs[0]:
            self.search_products_tab()

        with tabs[1]:
            self.search_product_by_id_tab()

        with tabs[2]:
            self.search_product_by_id_offers_tab()


if __name__ == "__main__":
    api_client = APIClient(BASE_URL)
    app = StreamLitApp(api_client)
    app.run()
