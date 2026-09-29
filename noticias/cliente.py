import requests
from .config import API_KEY, BASE_URL


def _get(endpoint, params):
    params = {**params, "apiKey": API_KEY}
    try:
        resposta = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=10)
        dados = resposta.json()
    except requests.RequestException as e:
        print("Erro de conexão:", e)
        return []

    if resposta.status_code == 200 and dados.get("status") == "ok":
        return dados["articles"]

    print("Erro da API:", dados.get("message"))
    return []


def buscar_noticias(tema, idioma="pt", qtd=100):
    return _get("everything", {
        "q": tema,
        "language": idioma,
        "sortBy": "publishedAt",
        "pageSize": qtd,
    })


def buscar_por_pais(pais, categoria="technology"):
    return _get("top-headlines", {"country": pais, "category": categoria})