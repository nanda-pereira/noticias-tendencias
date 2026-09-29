# Notícias em Tendência

Aplicação que coleta manchetes sobre um tema, conta quais palavras mais aparecem e mostra o resultado em uma interface web com nuvem de palavras, ranking e lista de notícias organizada por data e fonte.

O projeto tem duas partes que conversam entre si:

- **Back-end em Python (Flask):** busca as notícias na NewsAPI, limpa o texto e faz a contagem de palavras.
- **Front-end em React (Vite):** o usuário digita um tema e vê os resultados na tela.

Também é possível rodar só a parte Python pelo terminal, sem o front-end.

---

## Índice

1. [O que o projeto faz](#o-que-o-projeto-faz)
2. [Como funciona por dentro](#como-funciona-por-dentro)
3. [Tecnologias](#tecnologias)
4. [Estrutura de pastas](#estrutura-de-pastas)
5. [Pré-requisitos](#pré-requisitos)
6. [Instalação](#instalação)
7. [Como executar](#como-executar)
8. [Rotas da API](#rotas-da-api)
9. [Limites da NewsAPI](#limites-da-newsapi)
10. [Segurança da chave](#segurança-da-chave)
11. [Problemas comuns](#problemas-comuns)
12. [Ideias para evoluir](#ideias-para-evoluir)
13. [Autora](#autora)

---

## O que o projeto faz

1. Recebe um tema digitado pelo usuário (por exemplo, "economia" ou "inteligência artificial").
2. Busca até 100 notícias recentes sobre esse tema na NewsAPI.
3. Junta título e descrição de cada notícia e limpa o texto: converte para minúsculas, remove pontuação, números e palavras sem significado (as chamadas *stopwords*, como "de", "que" e "para").
4. Conta quantas vezes cada palavra aparece.
5. Exibe o resultado de três formas:
   - **Nuvem de palavras:** quanto mais frequente a palavra, maior ela aparece.
   - **Ranking:** as 15 palavras mais frequentes em formato de tabela com barras.
   - **Manchetes:** lista de notícias agrupada por dia, com filtro por fonte.

Além disso, o painel mostra três números de resumo: total de notícias analisadas, a palavra líder e a quantidade de fontes diferentes.

---

## Como funciona por dentro

O fluxo de dados segue um pipeline:

```
NewsAPI  ->  texto bruto  ->  limpeza  ->  contagem  ->  visualização
```

E a comunicação entre as partes acontece assim:

```
Navegador (React)  ->  API Flask (Python)  ->  NewsAPI
   telas e gráficos       lógica e chave          fonte dos dados
```

O React nunca fala diretamente com a NewsAPI. Isso é intencional por dois motivos:

- **A chave da API fica protegida.** Tudo o que roda no navegador pode ser visto por qualquer pessoa, então a chave precisa ficar no servidor.
- **A lógica de análise já está em Python**, com bibliotecas próprias para processamento de texto, então faz sentido reaproveitá-la em vez de reescrevê-la em JavaScript.

O código Python é dividido em módulos, cada um com uma responsabilidade:

| Módulo | Responsabilidade |
|---|---|
| `config.py` | Carrega a chave do arquivo `.env` e define a URL base da API |
| `cliente.py` | Faz as requisições HTTP à NewsAPI e trata erros de conexão |
| `texto.py` | Extrai título e descrição, define as stopwords e limpa o texto |
| `analise.py` | Conta palavras, monta o ranking e agrupa notícias por data |
| `visual.py` | Gera a nuvem em imagem e a tabela (usado apenas no modo terminal) |

---

## Tecnologias

**Back-end**

- Python 3
- Flask e Flask-CORS (servidor e liberação de acesso para o front-end)
- requests (chamadas HTTP)
- NLTK (lista de stopwords)
- collections.Counter (contagem de palavras)
- python-dotenv (leitura do arquivo `.env`)
- pandas, matplotlib e wordcloud (apenas no modo terminal)

**Front-end**

- React
- Vite
- CSS puro, sem bibliotecas de componentes

---

## Estrutura de pastas

```
noticias-tendencias/
├── noticias/                 pacote com a lógica do projeto
│   ├── __init__.py
│   ├── config.py
│   ├── cliente.py
│   ├── texto.py
│   ├── analise.py
│   └── visual.py
├── frontend/                 aplicação React
│   ├── src/
│   │   ├── components/
│   │   │   ├── Busca.jsx
│   │   │   ├── Nuvem.jsx
│   │   │   ├── Ranking.jsx
│   │   │   └── ListaNoticias.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
├── api.py                    servidor Flask
├── main.py                   versão de terminal
├── requirements.txt          dependências do Python
├── .env.example              modelo do arquivo de configuração
├── .gitignore
└── README.md
```

---

## Pré-requisitos

Antes de começar, instale:

- **Python 3.10 ou superior**. Ao instalar no Windows, marque a opção "Add python.exe to PATH".
- **Node.js (versão LTS)**, que já inclui o npm.
- **Git**.
- Uma **chave gratuita da NewsAPI**, obtida em [newsapi.org](https://newsapi.org): clique em "Get API Key", crie a conta e copie a chave.

Para conferir se tudo está instalado:

```
python --version
node --version
npm --version
git --version
```

---

## Instalação

### 1. Baixar o projeto

```
git clone https://github.com/nanda-pereira/noticias-tendencias.git
cd noticias-tendencias
```

### 2. Configurar a chave da API

Crie um arquivo chamado `.env` na raiz do projeto (ao lado do `api.py`) com uma única linha:

```
NEWS_API_KEY=cole_sua_chave_aqui
```

Não use aspas nem espaços em volta do sinal de igual. O repositório inclui um arquivo `.env.example` como modelo.

### 3. Instalar as dependências do Python

Recomenda-se usar um ambiente virtual, que isola as bibliotecas do projeto do resto do computador:

```
python -m venv venv
```

Ative o ambiente:

```
# Windows (Prompt de Comando)
venv\Scripts\activate.bat

# Windows (PowerShell)
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

No PowerShell, se aparecer um erro dizendo que a execução de scripts está desabilitada, rode uma vez:

```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Com o ambiente ativo (o terminal mostra `(venv)` no começo da linha), instale as bibliotecas:

```
pip install -r requirements.txt
```

Se preferir não usar o ambiente virtual, o comando `pip install -r requirements.txt` também funciona direto, mas instalará os pacotes no Python geral do computador.

### 4. Instalar as dependências do front-end

```
cd frontend
npm install
cd ..
```

---

## Como executar

### Opção A: aplicação completa (recomendada)

São necessários **dois terminais abertos ao mesmo tempo**.

**Terminal 1, na raiz do projeto (com o ambiente virtual ativo):**

```
python api.py
```

O servidor sobe em `http://localhost:5000`.

**Terminal 2, dentro da pasta `frontend`:**

```
npm run dev
```

O Vite mostra o endereço da aplicação, normalmente `http://localhost:5173`. Abra no navegador, digite um tema e clique em **Analisar**.

### Opção B: apenas pelo terminal

Na raiz do projeto, com o ambiente ativo:

```
python main.py
```

O programa imprime no terminal o ranking, as notícias agrupadas por data e por região, e salva a nuvem de palavras no arquivo `nuvem.png`. Uma janela com a nuvem também é aberta e o programa só termina depois que ela for fechada.

Importante: execute sempre os comandos Python a partir da **raiz do projeto**, senão o Python não encontra o pacote `noticias`.

---

## Rotas da API

### `GET /api/tendencias`

Busca notícias por tema.

| Parâmetro | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `tema` | não | `inteligência artificial` | Assunto pesquisado |
| `idioma` | não | `pt` | Idioma das notícias (`pt`, `en`, `es`) |

Exemplo:

```
http://localhost:5000/api/tendencias?tema=economia&idioma=pt
```

Resposta (resumida):

```json
{
  "tema": "economia",
  "total": 100,
  "ranking": [
    { "palavra": "governo", "frequencia": 34 },
    { "palavra": "mercado", "frequencia": 29 }
  ],
  "noticias": [
    {
      "titulo": "Título da notícia",
      "fonte": "Nome do veículo",
      "data": "2026-09-27T14:30:00Z",
      "url": "https://..."
    }
  ]
}
```

### `GET /api/regiao`

Busca as principais manchetes de um país.

| Parâmetro | Obrigatório | Padrão | Descrição |
|---|---|---|---|
| `pais` | não | `br` | Código do país (`br`, `us`, `gb`, `pt`...) |
| `categoria` | não | `technology` | `business`, `entertainment`, `general`, `health`, `science`, `sports` ou `technology` |

Exemplo:

```
http://localhost:5000/api/regiao?pais=us&categoria=business
```

O formato da resposta é o mesmo da rota anterior. Notícias de países de língua inglesa são processadas com as stopwords em inglês.

Em caso de erro ou de nenhum resultado, as duas rotas respondem com status 404 e uma mensagem no campo `erro`.

---

## Limites da NewsAPI

O plano gratuito tem restrições que afetam o uso do projeto (confira os valores atuais no site da NewsAPI, pois eles podem mudar):

- Há um limite diário de requisições. Cada busca feita na aplicação consome uma.
- As notícias do plano gratuito chegam com atraso de cerca de 24 horas.
- A rota `top-headlines`, usada na busca por região, tem cobertura irregular por país e categoria, então pode retornar poucas notícias ou nenhuma.
- O plano gratuito não permite chamadas feitas diretamente de navegadores fora do `localhost`, o que reforça a escolha de passar pelo servidor Flask.

Durante o desenvolvimento, evite repetir buscas sem necessidade para não gastar o limite do dia.

---

## Segurança da chave

- A chave fica no arquivo `.env`, que está listado no `.gitignore` e nunca deve ser enviado ao GitHub.
- O front-end não contém a chave em nenhum momento.
- Não exiba o conteúdo do `.env` em capturas de tela, vídeos ou apresentações.
- Se a chave for exposta por engano, apagar o arquivo depois não resolve, porque ela permanece no histórico do Git. Gere uma chave nova no painel da NewsAPI e desative a antiga.

---

## Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `Chave não encontrada` | Arquivo `.env` ausente, com nome errado ou sem salvar | Confira o nome (`.env`, com o ponto), o conteúdo e salve o arquivo |
| `ModuleNotFoundError: requests` (ou outra biblioteca) | Ambiente virtual não ativado ou dependências não instaladas | Ative o `venv` e rode `pip install -r requirements.txt` |
| `ModuleNotFoundError: noticias` | Comando executado fora da raiz, ou falta o `__init__.py` | Rode a partir da raiz e confira se `noticias/__init__.py` existe |
| Erro de execução de scripts ao ativar o `venv` no PowerShell | Política de execução do Windows | Rode o `Set-ExecutionPolicy` indicado na seção de instalação, ou use o Prompt de Comando |
| `Failed to fetch` no navegador | Servidor Flask desligado | Confira se o `python api.py` está rodando no outro terminal |
| Erro de CORS no console do navegador | Falta o `flask-cors` ou a linha `CORS(app)` | Instale o pacote e confira o `api.py` |
| `apiKeyInvalid` | Chave copiada errada | Copie novamente a chave do painel da NewsAPI |
| `rateLimited` | Limite diário atingido | Aguarde e tente novamente no dia seguinte |
| Nenhuma notícia encontrada | Tema muito específico ou idioma incompatível | Teste um tema mais comum ou troque o idioma |
| Tela em branco no front-end e erro sobre `main.jsx` | Arquivo `src/main.jsx` ausente | Crie o arquivo conforme o modelo do Vite para React |

---

## Ideias para evoluir

- Seletor de país e categoria na interface, usando a rota `/api/regiao`.
- Comparação entre dois temas lado a lado.
- Análise da evolução das palavras ao longo dos dias.
- Cache das respostas para economizar requisições da NewsAPI.
- Análise de sentimento das manchetes.
- Publicação online, com o front-end na Vercel ou Netlify e o back-end no Render ou Railway.
- Suporte a GNews como fonte alternativa de notícias.

---

## Autora

Desenvolvido por **Fernanda Pereira**, estudante de Análise e Desenvolvimento de Sistemas, como atividade prática de consumo de APIs externas com Python.
