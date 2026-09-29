import { useState } from "react";
import Busca from "./components/Busca";
import Nuvem from "./components/Nuvem";
import Ranking from "./components/Ranking";
import ListaNoticias from "./components/ListaNoticias";
import "./App.css";

const API = "http://localhost:5000/api/tendencias";

export default function App() {
  const [dados, setDados] = useState(null);
  const [carregando, setCarregando] = useState(false);
  const [erro, setErro] = useState("");

  async function buscar(tema, idioma) {
    setCarregando(true);
    setErro("");
    try {
      const url = `${API}?tema=${encodeURIComponent(tema)}&idioma=${idioma}`;
      const resp = await fetch(url);
      const json = await resp.json();
      if (!resp.ok) throw new Error(json.erro || "Erro ao buscar");
      setDados(json);
    } catch (e) {
      setErro(e.message);
      setDados(null);
    } finally {
      setCarregando(false);
    }
  }

  const fontes = dados ? new Set(dados.noticias.map((n) => n.fonte)).size : 0;

  return (
    <div className="pagina">
      <header className="hero">
        <p className="selo">Análise de notícias</p>
        <h1>O que está em <em>alta</em> nas manchetes</h1>
        <p className="sub">Escolha um tema e descubra quais palavras dominam a conversa.</p>
        <Busca onBuscar={buscar} carregando={carregando} />
      </header>

      {erro && <p className="erro">{erro}</p>}
      {carregando && <p className="carregando">Lendo as manchetes…</p>}

      {dados && !carregando && (
        <main>
          <div className="stats">
            <div className="stat"><small>Notícias</small><strong>{dados.total}</strong></div>
            <div className="stat"><small>Palavra líder</small><strong>{dados.ranking[0]?.palavra}</strong></div>
            <div className="stat"><small>Fontes</small><strong>{fontes}</strong></div>
          </div>
          <Nuvem ranking={dados.ranking} />
          <Ranking ranking={dados.ranking.slice(0, 15)} />
          <ListaNoticias noticias={dados.noticias} />
        </main>
      )}

      <footer className="rodape">React + Flask + NewsAPI
        <p>
            Fernanda Pereira · 2026
        </p>
      </footer>
    </div>
  );
}