import React from "react";

export default function EstimateCard({ estimate = {} }) {
  const { tasks = [], materials = [], breakdown = {}, note = "", modelPrediction, features } = estimate;

  return (
    <div className="estimate-container">
      <div className="est-header">
        <span className="est-title">⚡ Instant Estimate</span>
        <span className="est-badge">AI GENERATED</span>
      </div>

      <div className="est-body">
        {note && (
          <p style={{ color: '#94a3b8', marginBottom: '20px', fontSize: '0.95rem' }}>
            {note}
          </p>
        )}

        {/* Model Prediction Highlight */}
        {modelPrediction && (
          <div style={{
            marginBottom: '25px',
            padding: '15px',
            background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.05))',
            borderRadius: '10px',
            border: '1px solid rgba(34, 197, 94, 0.3)'
          }}>
            <div style={{ 
              fontSize: '0.85rem', 
              fontWeight: 'bold',
              color: '#22c55e',
              marginBottom: '10px'
            }}>
              🤖 ML Model Prediction:
            </div>
            <div style={{ 
              display: 'flex', 
              gap: '20px',
              fontSize: '0.9rem',
              color: '#e5e7eb'
            }}>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>Cost: </span>
                <strong style={{ color: '#22c55e' }}>£{modelPrediction.cost.toFixed(2)}</strong>
              </div>
              <div>
                <span style={{ color: 'var(--text-muted)' }}>Time: </span>
                <strong style={{ color: '#22c55e' }}>{modelPrediction.time} days</strong>
              </div>
            </div>
          </div>
        )}

        {/* Detected Features */}
        {features && Object.keys(features).length > 0 && (
          <div style={{ marginBottom: '25px' }}>
            <span className="section-title">Detected Features</span>
            <div style={{
              display: 'flex',
              flexWrap: 'wrap',
              gap: '8px',
              marginTop: '10px'
            }}>
              {Object.entries(features).map(([key, value]) => {
                // Only show non-zero and meaningful values
                if (value === 0 || value === '0' || value === 'none' || value === '') return null;
                
                return (
                  <span key={key} style={{
                    padding: '6px 12px',
                    backgroundColor: 'rgba(96, 165, 250, 0.15)',
                    borderRadius: '6px',
                    fontSize: '0.8rem',
                    color: '#60a5fa',
                    border: '1px solid rgba(96, 165, 250, 0.3)'
                  }}>
                    {key.replace(/([A-Z])/g, ' $1').trim()}: {typeof value === 'boolean' ? (value ? '✓' : '✗') : value}
                  </span>
                );
              })}
            </div>
          </div>
        )}

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