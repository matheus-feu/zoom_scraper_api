## Comparador de Preços e Produtos

### Introdução

O projeto é um **comparador de preços e produtos** que simula buscas no site **Zoom (zoom.com.br)**, transformando os
resultados encontrados em dados estruturados no formato **JSON**. Essa estrutura pode ser consumida por meio de APIs
REST (utilizando **FastAPI**) ou via interface gráfica de usuário disponibilizada por **Streamlit**.

O principal objetivo é ajudar os usuários a encontrar os melhores preços e detalhes dos produtos de forma prática, sem
depender de APIs oficiais do Zoom. Todo o processo envolve um _crawler_ que navega pela página, coleta informações
relevantes e fornece esses dados de maneira estruturada.

### Descrição Resumida

O serviço é baseado em um _crawler_ configurado para:

- Simular buscas no site **Zoom**.
- Coletar informações como **nome do produto**, **imagem**, **preço**, **loja** e **detalhes do produto**.
- Um mecanismo de cache incorporado através do pacote `fastapi-cache` para melhorar o desempenho das requisições repetidas.
- Estruturar e disponibilizar as informações para consumo via **API FastAPI** ou **interface Streamlit**.

--- 

### Endpoints Disponíveis

#### FastAPI

Os seguintes endpoints REST estão disponíveis para interagir com o serviço:

1. **Lista de Produtos**:

### **Exemplo de Requisição:**

Requisição:

``` bash
GET api/v1/search?term=notebook
```

### **Parâmetros da Query:**

- **`term` (obrigatório):**
    - Descrição: O termo utilizado para pesquisar os produtos no catálogo.
    - Tipo: `string`
    - Exemplo: `term=notebook`.

### **Resposta:**

A resposta será um JSON com os seguintes campos:

- **(int):`total_pages`** Total de páginas disponíveis na pesquisa.
- **(int):`total_products`** Total de produtos encontrados.
- **(array):`products`** Uma lista de produtos encontrados na pesquisa, onde cada produto contém:
    - **(int):`id`** Identificador único do produto.
    - **(string):`name`** Nome do produto.
    - **(float):`price`** Preço do produto no Zoom.
    - **`image` (string):** URL para a imagem do produto.
    - **`link internal` (string):** Link interno para detalhes do produto.

### **Exemplo de Resposta:**

Sucesso (código HTTP **200**):

``` json
{
    "total_pages": 5,
    "total_products": 120,
    "products": [
        {
            "id": 1,
            "name": "Notebook Acer Aspire 5",
            "price": 3500.00,
            "image": "https://zoom.com.br/static/images/notebook.png",
            "link_internal": "/product/1"
        },
        {
            "id": 2,
            "name": "Notebook Dell Inspiron 15",
            "price": 4200.50,
            "image": "https://zoom.com.br/static/images/dell.png",
            "link_internal": "/product/2"
        }
    ]
}
```

2. **Detalhes do Produto**:

### **Exemplo de Requisição:**

Requisição:

``` bash
GET /api/v1/product/12345156
```

### **Parâmetros da URL:**

- **`product_id` (obrigatório):**
    - Descrição: O ID do produto para o qual você deseja obter detalhes.
    - Tipo: `int`
    - Exemplo: `product_id=12345156`.

### **Resposta:**

A resposta será um JSON contendo os detalhes do produto, incluindo ficha técnica, avaliações e comentários, descrição,
complementos e entre outros.

3. **Busca por Produtos em outras Lojas**:

### **Exemplo de Requisição:**

Requisição:

``` bash
GET /api/v1/product/12345156/stores
```

### **Parâmetros da URL:**

- **`product_id` (obrigatório):**
    - Descrição: O ID do produto para o qual você deseja obter detalhes.
    - Tipo: `int`
    - Exemplo: `product_id=12345156`.

### **Resposta:**

A resposta será um JSON contendo os detalhes do produto, incluindo ficha técnica, avaliações e comentários, descrição,
complementos e entre outros.

- **(float):`price`** Preço do produto na loja.
- **(string):`store_name`** Nome da loja onde o produto está disponível.
- **(string):`purchase_link`** Link para compra do produto na loja.

``` json
[
  {
    "price": 452.09,
    "store_name": "Casas Bahia",
    "purchase_link": "https://www.casasbahia.com.br/12345156",
  }
]
```

---

# Funcionalidades

### API REST

- Fornece endereços REST para busca, detalhamento de produtos e listagem de lojas, permitindo integrações com sistemas
  externos.

### Streamlit Interface (UI)

- Uma **interface gráfica intuitiva** para realizar buscas e visualizar informações em tempo real.

Funcionalidades disponíveis:

- **Busca de Produtos**: Insira o termo desejado e veja uma lista de produtos relacionados.
- **Produto por ID**: Insira o ID de um produto para visualizar seus detalhes.
- **Ofertas por Produto**: Insira o ID de um produto para encontrar preços em diferentes lojas.

---

# Uso prático

### Executando localmente

1. Após clonar o projeto, instale as dependências necessárias:

```bash
pip install -r requirements.txt
```

2. Execute o servidor FastAPI:

```bash
python app/main.py
```

3. Execute a interface Streamlit:

```bash
streamlit run frontend/streamlit_app.py
```

4. Acesse os endpoints:

- FastAPI Docs: `http://localhost:8000/docs`
- Streamlit UI: `http://localhost:8502`

### Executando em Docker

```bash
docker-compose up
```

### Logs

Os logs são configurados para registrar eventos importantes da aplicação, como:

- Inicialização.
- Requisições recebidas na API.
- Erros durante o processo.

Os logs são gravados em e exibidos no console. `app.log`

### Caching

A aplicação utiliza o **FastAPI Cache**, que permite:

- Evitar processamento redundante em requisições repetitivas.
- Gerenciar respostas com controle de expiração utilizando um backend de cache (como Redis ou outros).

As funções podem ser decoradas com o decorador `@cache` para habilitar o armazenamento em cache.

#### Exemplo:

``` python
from fastapi_cache.decorator import cache

@cache(expire=60)  # Cache expira em 60 segundos
async def get_data(param: str):
    # Lógica que será armazenada em cache
    return {"result": f"Dados para {param}"}
```

### Estrutura do Projeto

```bash
.
├── app/main.py                  # Arquivo principal do FastAPI
├── frontend/streamlit_app.py      # Interface gráfica (Streamlit)
├── http_client.py           # Cliente HTTP para simulação de requisições
├── app/scrapers/zoom_scraper.py      # Crawler para coleta de dados do Zoom
├── requirements.txt         # Arquivo de dependências
├── Dockerfile               # Para contêiner Docker
└── app.log                  # Arquivo de logs
```

