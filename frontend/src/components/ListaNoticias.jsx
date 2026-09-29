import { useState } from "react";

function formatarDia(dia) {
  const d = new Date(dia + "T12:00:00");
  return isNaN(d) ? dia : d.toLocaleDateString("pt-BR", { day: "2-digit", month: "long" });
}

export default function ListaNoticias({ noticias }) {
  const [fonte, setFonte] = useState("todas");

  const contagem = {};
  noticias.forEach((n) => { if (n.fonte) contagem[n.fonte] = (contagem[n.fonte] || 0) + 1; });
  const topFontes = Object.entries(contagem).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([f]) => f);

  const filtradas = fonte === "todas" ? noticias : noticias.filter((n) => n.fonte === fonte);

  const porDia = {};
  filtradas.forEach((n) => {
    const dia = (n.data || "").slice(0, 10);
    (porDia[dia] = porDia[dia] || []).push(n);
  });

  return (
    <section className="cartao">
      <h2>Manchetes</h2>

      <div className="filtros">
        {["todas", ...topFontes].map((f) => (
          <button key={f} className={`chip ${fonte === f ? "ativo" : ""}`}
                  onClick={() => setFonte(f)}>{f}</button>
        ))}
      </div>

      {Object.entries(porDia).sort().reverse().map(([dia, lista]) => (
        <div className="dia" key={dia}>
          <h3>{formatarDia(dia)} · {lista.length}</h3>
          {lista.map((n) => (
            <a className="noticia" key={n.url} href={n.url} target="_blank" rel="noreferrer">
              <b>{n.titulo}</b>
              <small>{n.fonte}</small>
            </a>
          ))}
        </div>
      ))}
    </section>
  );
}