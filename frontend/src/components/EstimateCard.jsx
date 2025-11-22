import React from "react";

export default function EstimateCard({ estimate = {} }) {
  const { tasks = [], materials = [], breakdown = {}, note = "" } = estimate;

  return (
    <div className="estimate-container">
      <div className="est-header">
        <span className="est-title">⚡ Instant Estimate</span>
        <span className="est-badge">AI GENERATED</span>
      </div>

      <div className="est-body">
        <p style={{ color: '#94a3b8', marginBottom: '30px', fontSize: '0.95rem' }}>
          {note}
        </p>

        {/* LABOR SECTION */}
        <span className="section-title">Labor Breakdown</span>
        {tasks.map((t, i) => (
          <div className="item-row" key={i}>
            <span className="item-name">{t.title}</span>
            <span className="item-price">{t.hours} hrs</span>
          </div>
        ))}

        {/* MATERIALS SECTION */}
        <span className="section-title" style={{marginTop: '30px'}}>Materials Required</span>
        {materials.map((m, i) => (
          <div className="item-row" key={i}>
            <div>
              <div className="item-name">
                {m.name} <span className="item-sub">x{m.qty}</span>
              </div>
              <div>
                <a href={m.link} target="_blank" rel="noreferrer" className="buy-link">Buy Now ↗</a>
              </div>
            </div>
            <span className="item-price">${(m.qty * m.unitPrice).toFixed(2)}</span>
          </div>
        ))}

        {/* TOTALS SECTION */}
        <div className="total-section">
          <div style={{display:'flex', justifyContent:'flex-end', gap: '20px', marginBottom: '10px', color: '#94a3b8', fontSize: '0.9rem'}}>
             <span>Labor: ${breakdown.laborTotal}</span>
             <span>Materials: ${breakdown.materialsTotal}</span>
             <span>Markup: ${breakdown.markup}</span>
          </div>
          <div>
            <span className="total-label">ESTIMATED TOTAL</span>
            <span className="total-price">${breakdown.total}</span>
          </div>
        </div>
        
        <div style={{marginTop: '30px', textAlign: 'center'}}>
          <a 
            href={`mailto:?subject=Estimate&body=${encodeURIComponent(JSON.stringify(breakdown))}`}
            style={{color: 'var(--orange)', textDecoration: 'none', fontSize: '0.9rem', fontWeight: 600}}
          >
            📩 Email this Quote
          </a>
        </div>
      </div>
    </div>
  );
}