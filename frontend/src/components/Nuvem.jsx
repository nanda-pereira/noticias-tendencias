const CORES = ["#4f46e5", "#14b8a6", "#0f766e", "#6366f1", "#0d9488", "#312e81"];
export default function Nuvem({ ranking }) {
  const max = ranking[0].frequencia;
  const min = ranking[ranking.length - 1].frequencia;

  const tamanho = (f) =>
    max === min ? 32 : 16 + Math.sqrt((f - min) / (max - min)) * 48;

  // maiores no centro: alterna entre o fim e o começo da lista
  const ordenado = [];
  ranking.forEach((r, i) => {
    const item = { ...r, i };
    if (i % 2 === 0) ordenado.push(item);
    else ordenado.unshift(item);
  });

  return (
    <section className="cartao">
      <h2>Nuvem de palavras</h2>
      <div className="nuvem">
        {ordenado.map((r) => (
          <span key={r.palavra}
                title={`${r.frequencia} ocorrências`}
                style={{ fontSize: tamanho(r.frequencia), color: CORES[r.i % CORES.length] }}>
            {r.palavra}
          </span>
        ))}
      </div>
    </section>
  );
}