from collections import Counter
from .texto import extrair_textos, limpar_e_tokenizar, stopwords_do_idioma


def contar_palavras(artigos, idioma="pt", extras=()):
    stop = stopwords_do_idioma(idioma) | {e.lower() for e in extras}
    palavras = limpar_e_tokenizar(extrair_textos(artigos), stop)
    return Counter(palavras)


def montar_ranking(contagem, n=15):
    return [{"palavra": p, "frequencia": f} for p, f in contagem.most_common(n)]


def agrupar_por_data(artigos):
    grupos = {}
    for a in artigos:
        dia = (a.get("publishedAt") or "")[:10]
        grupos.setdefault(dia, []).append(a)
    return dict(sorted(grupos.items(), reverse=True))