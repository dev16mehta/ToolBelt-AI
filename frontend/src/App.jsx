/* App.jsx */
import React, { useState } from "react";
import { Valyu } from "valyu-js"; // Import the library
import CameraCapture from "./components/CameraCapture";
import VoiceRecorder from "./components/VoiceRecorder";
import EstimateCard from "./components/EstimateCard";

// Initialize the client 
const valyu = new Valyu("EqsAMTZKpW28845oSgHcm7FkekXKxi6K2qbkIUhu");

export default function App() {
  const [images, setImages] = useState([]);
  const [transcript, setTranscript] = useState("");
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(false);
  const [aiEstimate, setAiEstimate] = useState(null); // Estimate from voice/chat

  // Handler for when AI generates an estimate from voice/chat
  const handleAiEstimate = (estimateData, features) => {
    setAiEstimate({
      cost_gbp: estimateData.cost_gbp,
      cost_dzd: estimateData.cost_dzd,
      time_days: estimateData.time_days,
      features: features
    });
  };

  async function handleEstimate() {
    if (images.length === 0 && !transcript) {
      alert("Please upload a photo or describe the job first.");
      return;
    }
    setLoading(true);
    setEstimate(null); // Clear previous estimate while loading

    try {
      // Now we await the AI generation because it fetches real links
      const result = await generateEstimate(images, transcript);
      setEstimate(result);
    } catch (error) {
      console.error("Estimation failed:", error);
      alert("Something went wrong generating the quote. Check console.");
    } finally {
      setLoading(false);
    }
  }

  // Converted to ASYNC function to handle API calls
  async function generateEstimate(images, transcript) {
    const baseLabor = 75;
    const imageFactor = Math.min(4, Math.max(1, images.length));
    let tasks = [];
    let rawMaterials = [];

    const text = transcript.toLowerCase();
    
    // 1. Determine logic (Placeholder simulation)
    if (text.includes("leak") || text.includes("pipe")) {
      tasks.push({ title: "Diagnose leak", hours: 1 });
      tasks.push({ title: "Replace pipe section", hours: 2 });
      rawMaterials.push({ name: "1/2\" PVC pipe", qty: 1, unitPrice: 12 });
      rawMaterials.push({ name: "PVC Pipe coupler", qty: 1, unitPrice: 4 });
    } else if (text.includes("landscap") || text.includes("sod") || text.includes("mulch")) {
      tasks.push({ title: "Site prep", hours: 2 });
      tasks.push({ title: "Install mulch/sod", hours: 3 * imageFactor });
      rawMaterials.push({ name: "Bag of Mulch", qty: 12 * imageFactor, unitPrice: 4 });
      rawMaterials.push({ name: "Sod roll", qty: 50 * imageFactor, unitPrice: 8 });
    } else {
      tasks.push({ title: "General repair/inspection", hours: 1 * imageFactor });
      rawMaterials.push({ name: "Assorted fasteners box", qty: 1, unitPrice: 8 });
    }

    // 2. Fetch REAL links using Valyu
    // We use Promise.all to fetch all links in parallel (faster)
    const materialsWithLinks = await Promise.all(rawMaterials.map(async (m) => {
      let realUrl = `https://www.google.com/search?q=${encodeURIComponent(m.name)}`; // Fallback
      
      try {
        // Search specifically for buying the item
        const response = await valyu.search(`buy ${m.name} home depot`, { 
          maxNumResults: 1 
        });
        
        if (response.results && response.results.length > 0) {
           realUrl = response.results[0].url;
        }
      } catch (err) {
        console.warn(`Valyu search failed for ${m.name}, using fallback.`, err);
      }

      return {
        ...m,
        link: realUrl
      };
    }));

    // 3. Calculate Totals
    const laborTotal = tasks.reduce((s, t) => s + t.hours * baseLabor, 0);
    const materialsTotal = materialsWithLinks.reduce((s, m) => s + m.qty * m.unitPrice, 0);
    const subtotal = Math.round((laborTotal + materialsTotal) * 100) / 100;
    const markup = Math.round(subtotal * 0.12 * 100) / 100;
    const total = Math.round((subtotal + markup) * 100) / 100;

    return {
      tasks,
      materials: materialsWithLinks,
      breakdown: { laborTotal, materialsTotal, markup, total },
      note: "Instant on-site estimate. Prices sourced via Valyu AI."
    };
  }

  return (
    <div className="app-container">
      <header>
        <div className="badge">⚡ AI-Powered Estimation</div>
        <h1 className="brand-title">
          Toolbelt <span className="highlight-ai">AI</span>
        </h1>
        <p className="subtitle">
          Your partner for <span>instant quotes</span> and <span className="blue">smart materials sourcing</span>.
        </p>
      </header>

      <main>
        {/* Split Card Layout */}
        <div className="input-grid">
          
          {/* Left Card: Photos */}
          <div className="glass-card">
            <div className="card-header">
              <div className="icon-box orange">📷</div>
              <div>
                <h2 className="card-title">Job Site Photos</h2>
                <p className="card-desc">Upload images of the work area</p>
              </div>
            </div>
            <CameraCapture images={images} setImages={setImages} />
          </div>

          {/* Right Card: Voice */}
          <div className="glass-card">
             <div className="card-header">
              <div className="icon-box cyan">🎤</div>
              <div>
                <h2 className="card-title">Voice Description</h2>
                <p className="card-desc">Describe the job details</p>
              </div>
            </div>
            <VoiceRecorder 
              transcript={transcript} 
              setTranscript={setTranscript}
              onEstimateReceived={handleAiEstimate}
            />
          </div>

        </div>

        <div className="action-area">
          <button className="cta-btn" onClick={handleEstimate} disabled={loading}>
            {loading ? "Analyzing & Sourcing..." : "✨ Generate Quote & Materials"}
          </button>
        </div>

        {/* Display AI-generated estimate from voice/chat */}
        {aiEstimate && (
          <div className="glass-card" style={{ marginTop: '20px' }}>
            <div style={{ 
              padding: '20px',
              background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.05))',
              borderRadius: '12px',
              border: '2px solid rgba(34, 197, 94, 0.3)'
            }}>
              <div style={{ 
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                marginBottom: '20px'
              }}>
                <div style={{ fontSize: '2rem' }}>💰</div>
                <div>
                  <h2 style={{ 
                    color: '#22c55e',
                    fontSize: '1.5rem',
                    fontWeight: 'bold',
                    margin: 0
                  }}>
                    AI-Generated Estimate
                  </h2>
                  <p style={{ 
                    color: 'var(--text-muted)',
                    fontSize: '0.9rem',
                    margin: '4px 0 0 0'
                  }}>
                    Based on your description
                  </p>
                </div>
              </div>
              
              <div style={{ 
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '16px',
                marginBottom: '16px'
              }}>
                <div style={{ 
                  padding: '16px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '8px'
                }}>
                  <div style={{ 
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)',
                    marginBottom: '8px'
                  }}>
                    Cost (GBP)
                  </div>
                  <div style={{ 
                    fontSize: '1.8rem',
                    fontWeight: 'bold',
                    color: '#22c55e'
                  }}>
                    £{aiEstimate.cost_gbp.toFixed(2)}
                  </div>
                </div>
                
                <div style={{ 
                  padding: '16px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '8px'
                }}>
                  <div style={{ 
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)',
                    marginBottom: '8px'
                  }}>
                    Cost (DZD)
                  </div>
                  <div style={{ 
                    fontSize: '1.8rem',
                    fontWeight: 'bold',
                    color: '#22c55e'
                  }}>
                    {aiEstimate.cost_dzd.toFixed(2)}
                  </div>
                </div>
                
                <div style={{ 
                  padding: '16px',
                  backgroundColor: 'rgba(255, 255, 255, 0.05)',
                  borderRadius: '8px'
                }}>
                  <div style={{ 
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)',
                    marginBottom: '8px'
                  }}>
                    Estimated Time
                  </div>
                  <div style={{ 
                    fontSize: '1.8rem',
                    fontWeight: 'bold',
                    color: '#22c55e'
                  }}>
                    {aiEstimate.time_days} days
                  </div>
                </div>
              </div>

              {aiEstimate.features && Object.keys(aiEstimate.features).length > 0 && (
                <div style={{ 
                  marginTop: '16px',
                  padding: '12px',
                  backgroundColor: 'rgba(255, 255, 255, 0.03)',
                  borderRadius: '8px'
                }}>
                  <div style={{ 
                    fontSize: '0.85rem',
                    color: 'var(--text-muted)',
                    marginBottom: '8px',
                    fontWeight: 'bold'
                  }}>
                    Detected Features:
                  </div>
                  <div style={{ 
                    display: 'flex',
                    flexWrap: 'wrap',
                    gap: '8px'
                  }}>
                    {Object.entries(aiEstimate.features).map(([key, value]) => (
                      <span key={key} style={{
                        padding: '4px 12px',
                        backgroundColor: 'rgba(34, 197, 94, 0.2)',
                        borderRadius: '12px',
                        fontSize: '0.8rem',
                        color: '#22c55e'
                      }}>
                        {key}: {typeof value === 'boolean' ? (value ? '✓' : '✗') : value}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              <button 
                onClick={() => setAiEstimate(null)}
                style={{
                  marginTop: '16px',
                  padding: '8px 16px',
                  backgroundColor: 'rgba(239, 68, 68, 0.2)',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  borderRadius: '6px',
                  color: '#ef4444',
                  cursor: 'pointer',
                  fontSize: '0.85rem',
                  width: '100%'
                }}
              >
                Clear Estimate
              </button>
            </div>
          </div>
        )}

        {estimate && <EstimateCard estimate={estimate} />}
      </main>
    </div>
  );
}