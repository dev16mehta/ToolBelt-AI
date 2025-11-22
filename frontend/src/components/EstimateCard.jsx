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
            <div style={{width: '100%'}}>
              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <div className="item-name">
                  {m.name} <span className="item-sub">x{m.qty}</span>
                </div>
                {/* Price removed, only the link remains */}
                <a href={m.link} target="_blank" rel="noreferrer" className="buy-link">
                  Select Item & Buy ↗
                </a>
              </div>
            </div>
          </div>
        ))}

        {/* TOTALS SECTION (UPDATED TO GBP) */}
        <div className="total-section">
          <div style={{textAlign: 'right'}}>
            <span className="total-label">ESTIMATED TOTAL</span>
            {/* Changed $ to £ */}
            <span className="total-price">£{breakdown.total}</span>
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