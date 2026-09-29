import re
import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

STOP_PT = set(stopwords.words("portuguese")) | {
    "diz", "após", "sobre", "novo", "nova", "ser", "ano", "anos",
    "pode", "veja", "como", "mais", "vai",
}
STOP_EN = set(stopwords.words("english"))


def stopwords_do_idioma(idioma):
    return STOP_PT if idioma == "pt" else STOP_EN


def extrair_textos(artigos):
    return [f"{a.get('title') or ''} {a.get('description') or ''}" for a in artigos]


def limpar_e_tokenizar(textos, stop):
    palavras = []
    for texto in textos:
        texto = re.sub(r"[^a-záàâãéêíóôõúç\s]", " ", texto.lower())
        palavras += [p for p in texto.split() if p not in stop and len(p) > 2]
    return palavras