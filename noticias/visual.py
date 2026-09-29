import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


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