import React from "react";

export default function EstimateCard({ estimate = {}, images = [], transcript = "" }) {
  const { tasks = [], materials = [], breakdown = {}, note = "" } = estimate;
  return (
    <section className="card result">
      <h2>Instant Estimate</h2>
      <p className="small">{note}</p>

      <div className="row">
        <div>
          <h3>Tasks</h3>
          <ul>
            {tasks.map((t, i) => (
              <li key={i}>{t.title} — {t.hours} hr</li>
            ))}
          </ul>
        </div>
        <div>
          <h3>Photos</h3>
          <div className="mini-thumbs">
            {images.slice(0,4).map((img, i) => <img key={i} src={img.url} alt={`p${i}`} />)}
          </div>
        </div>
      </div>

      <h3>Materials</h3>
      <ul className="materials">
        {materials.map((m, i) => (
          <li key={i}>
            <div>
              <strong>{m.name}</strong> ×{m.qty} — ${Math.round(m.qty * m.unitPrice * 100)/100}
            </div>
            <div className="links">
              <a href={m.link} target="_blank" rel="noreferrer">Buy</a>
              <a href={`https://www.google.com/search?q=${encodeURIComponent(m.name)}`} target="_blank" rel="noreferrer">Compare</a>
            </div>
          </li>
        ))}
      </ul>

      <div className="totals">
        <div>Materials: ${Math.round((breakdown.materialsTotal || 0)*100)/100}</div>
        <div>Labor: ${Math.round((breakdown.laborTotal || 0)*100)/100}</div>
        <div>Markup: ${breakdown.markup}</div>
        <div className="grand">Total: ${breakdown.total}</div>
      </div>

      <div className="actions">
        <a className="primary" href={`mailto:office@you.com?subject=Materials%20Request&body=${encodeURIComponent(JSON.stringify({materials, transcript}, null, 2))}`}>
          Request Materials
        </a>
      </div>
    </section>
  );
}
