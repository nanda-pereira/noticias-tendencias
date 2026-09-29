from flask import Flask, jsonify, request
from flask_cors import CORS

from noticias.cliente import buscar_noticias, buscar_por_pais
from noticias.analise import contar_palavras, montar_ranking

app = Flask(__name__)
CORS(app)


def resposta(rotulo, artigos, idioma, extras=()):
    if not artigos:
        return jsonify({"erro": "Nenhuma notícia encontrada"}), 404

    contagem = contar_palavras(artigos, idioma, extras)
    return jsonify({
        "tema": rotulo,
        "total": len(artigos),
        "ranking": montar_ranking(contagem, 30),
        "noticias": [{
            "titulo": a.get("title"),
            "fonte": (a.get("source") or {}).get("name"),
            "data": a.get("publishedAt"),
            "url": a.get("url"),
        } for a in artigos],
    })


@app.route("/api/tendencias")
def tendencias():
    tema = request.args.get("tema", "inteligência artificial")
    idioma = request.args.get("idioma", "pt")
    artigos = buscar_noticias(tema, idioma=idioma)
    return resposta(tema, artigos, idioma, extras=tema.split())


@app.route("/api/regiao")
def regiao():
    pais = request.args.get("pais", "br")
    categoria = request.args.get("categoria", "technology")
    idioma = "pt" if pais in ("br", "pt") else "en"
    artigos = buscar_por_pais(pais, categoria)
    return resposta(f"{categoria} ({pais.upper()})", artigos, idioma)


if __name__ == "__main__":
    app.run(debug=True, port=5000)