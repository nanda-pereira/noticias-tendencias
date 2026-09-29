import { useState } from "react";

const SUGESTOES = ["inteligência artificial", "economia", "esportes", "saúde", "clima"];

export default function Busca({ onBuscar, carregando }) {
  const [tema, setTema] = useState("");
  const [idioma, setIdioma] = useState("pt");

  function enviar(e) {
    e.preventDefault();
    if (tema.trim()) onBuscar(tema.trim(), idioma);
  }

  function escolher(s) {
    setTema(s);
    onBuscar(s, idioma);
  }

  return (
    <>
      <form onSubmit={enviar} className="busca">
        <input value={tema} onChange={(e) => setTema(e.target.value)}
               placeholder="Ex: economia, futebol, clima…" />
        <select value={idioma} onChange={(e) => setIdioma(e.target.value)}>
          <option value="pt">PT</option>
          <option value="en">EN</option>
          <option value="es">ES</option>
        </select>
        <button disabled={carregando}>{carregando ? "Buscando…" : "Analisar"}</button>
      </form>
      <div className="sugestoes">
        {SUGESTOES.map((s) => (
          <button key={s} type="button" className="chip"
                  onClick={() => escolher(s)} disabled={carregando}>{s}</button>
        ))}
      </div>
    </>
  );
}