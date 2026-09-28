import os
import re
import requests
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from collections import Counter
from dotenv import load_dotenv
from nltk.corpus import stopwords
from wordcloud import WordCloud

load_dotenv()                        # criei ele para ler o arquivo .env
API_KEY = os.getenv("NEWS_API_KEY")  # aqui é onde ele pega a chave da api dentro do .env

if not API_KEY:
    raise SystemExit("Chave não encontrada. Verifique o arquivo .env")

nltk.download("stopwords", quiet=True)

def buscar_noticias(tema, idioma="pt", qtd=100):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": tema,
        "language": idioma,
        "sortBy": "publishedAt",
        "pageSize": qtd,
        "apiKey": API_KEY,
    }
    try:
        resposta = requests.get(url, params=params, timeout=10)
        dados = resposta.json()
    except requests.RequestException as e:
        print("Erro de conexão:", e)
        return []

    if resposta.status_code == 200 and dados.get("status") == "ok":
        return dados["articles"]

    print("Erro da API:", dados.get("message"))
    return []

def extrair_textos(artigos):
    textos = []
    for a in artigos:
        titulo = a.get("title") or ""
        descricao = a.get("description") or ""
        textos.append(titulo + " " + descricao)
    return textos

STOP_PT = set(stopwords.words("portuguese"))
STOP_PT.update({"diz", "após", "sobre", "novo", "nova", "ser", "ano", "anos",
                "pode", "veja", "como", "mais", "vai"})

def limpar_e_tokenizar(textos, stop=STOP_PT):
    palavras = []
    for texto in textos:
        texto = texto.lower()
        texto = re.sub(r"[^a-záàâãéêíóôõúç\s]", " ", texto)
        for p in texto.split():
            if p not in stop and len(p) > 2:
                palavras.append(p)
    return palavras

def gerar_nuvem(contagem, titulo, arquivo):
    nuvem = WordCloud(width=1000, height=500, background_color="white",
                      colormap="viridis").generate_from_frequencies(contagem)
    plt.figure(figsize=(12, 6))
    plt.imshow(nuvem, interpolation="bilinear")
    plt.axis("off")
    plt.title(titulo)
    plt.savefig(arquivo, dpi=200, bbox_inches="tight")
    plt.show()

def ranking_tabela(contagem, n=15):
    df = pd.DataFrame(contagem.most_common(n), columns=["Palavra", "Frequência"])
    df.index = df.index + 1
    df.index.name = "Posição"
    return df

def buscar_por_pais(pais, categoria="technology"):
    url = "https://newsapi.org/v2/top-headlines"
    params = {"country": pais, "category": categoria, "apiKey": API_KEY}
    r = requests.get(url, params=params, timeout=10).json()
    return r.get("articles", [])

def agrupar_por_data(artigos):
    df = pd.DataFrame(artigos)
    df["data"] = pd.to_datetime(df["publishedAt"]).dt.date
    for data, grupo in df.groupby("data"):
        print(f"\n📅 {data} ({len(grupo)} notícias)")
        for titulo in grupo["title"].head(3):
            print("  -", titulo)

STOP_EN = set(stopwords.words("english"))

def mostrar_por_regiao(paises, categoria="technology"):
    for pais in paises:
        arts = buscar_por_pais(pais, categoria)
        print(f"\n[{pais.upper()}] {len(arts)} notícias")
        if not arts:
            print("  (nenhuma manchete retornada)")
            continue

        for a in arts[:3]:
            print("  -", a["title"])

        # palavras mais frequentes daquela região
        stop = STOP_EN if pais in ("us", "gb") else STOP_PT
        palavras = limpar_e_tokenizar(extrair_textos(arts), stop)
        print("  Top palavras:", Counter(palavras).most_common(5))

def mostrar_por_tema(temas):
    for tema in temas:
        arts = buscar_noticias(tema, qtd=30)
        palavras = limpar_e_tokenizar(extrair_textos(arts))
        print(f"\n[{tema.upper()}] {len(arts)} notícias")
        print("  Top palavras:", Counter(palavras).most_common(5))

def main():
    tema = "inteligência artificial"

    artigos = buscar_noticias(tema)
    print(len(artigos), "notícias coletadas")
    if not artigos:
        return

    # palavras do próprio tema não ajudam no ranking
    stop = STOP_PT | {"inteligência", "artificial"}
    palavras = limpar_e_tokenizar(extrair_textos(artigos), stop)
    contagem = Counter(palavras)

    print("\n=== RANKING ===")
    print(ranking_tabela(contagem))

    print("\n=== POR DATA ===")
    agrupar_por_data(artigos)

    print("\n=== POR REGIÃO ===")
    mostrar_por_regiao(["br", "us", "gb"])

    print("\n=== POR TEMA ===")
    mostrar_por_tema(["tecnologia", "economia", "esportes"])

    gerar_nuvem(contagem, f"Tendências: {tema}", "nuvem.png")

if __name__ == "__main__":
    main()