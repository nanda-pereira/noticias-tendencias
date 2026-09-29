export default function Ranking({ ranking }) {
  const max = ranking[0].frequencia;

  return (
    <section className="cartao">
      <h2>Ranking de palavras</h2>
      {ranking.map((r, i) => (
        <div className="linha-rank" key={r.palavra}>
          <span className="pos">{i + 1}</span>
          <span className="palavra">{r.palavra}</span>
          <div className="barra"><i style={{ width: `${(r.frequencia / max) * 100}%` }} /></div>
          <span className="num">{r.frequencia}</span>
        </div>
      ))}
    </section>
  );
}