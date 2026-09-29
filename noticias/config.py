import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"

if not API_KEY:
    raise RuntimeError("Chave não encontrada. Verifique o arquivo .env")