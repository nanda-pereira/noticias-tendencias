from noticias.cliente import buscar_noticias, buscar_por_pais
from noticias.analise import contar_palavras, agrupar_por_data
from noticias.visual import gerar_nuvem, ranking_tabela


def main():
    tema = "inteligência artificial"

    artigos = buscar_noticias(tema)
    print(len(artigos), "notícias coletadas")
    if not artigos:
        return

    contagem = contar_palavras(artigos, "pt", extras=tema.split())

    print("\n=== RANKING ===")
    print(ranking_tabela(contagem))

    print("\n=== POR DATA ===")
    for dia, lista in agrupar_por_data(artigos).items():
        print(f"\n{dia} ({len(lista)} notícias)")
        for a in lista[:3]:
            print("  -", a["title"])

    print("\n=== POR REGIÃO ===")
    for pais in ["br", "us", "gb"]:
        arts = buscar_por_pais(pais)
        print(f"\n[{pais.upper()}] {len(arts)} notícias")
        for a in arts[:3]:
            print("  -", a["title"])

    gerar_nuvem(contagem, f"Tendências: {tema}", "nuvem.png")


if __name__ == "__main__":
    main()