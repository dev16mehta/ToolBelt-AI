/* App.jsx */
import React, { useState } from "react";
import CameraCapture from "./components/CameraCapture";
import VoiceRecorder from "./components/VoiceRecorder";
import EstimateCard from "./components/EstimateCard";

export default function App() {
  const [images, setImages] = useState([]);
  const [transcript, setTranscript] = useState("");
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleEstimate() {
    if(images.length === 0 && !transcript) {
        alert("Please upload a photo or describe the job first.");
        return;
    }
    setLoading(true);
    // Placeholder logic simulation
    const result = generateEstimate(images, transcript);
    await new Promise((r) => setTimeout(r, 1500)); // Longer delay for effect
    setEstimate(result);
    setLoading(false);
  }

  // (Keep your existing generateEstimate logic here exactly as it was)
  function generateEstimate(images, transcript) {
    const baseLabor = 75; 
    const imageFactor = Math.min(4, Math.max(1, images.length));
    let tasks = [];
    let materials = [];

    const text = transcript.toLowerCase();
    if (text.includes("leak") || text.includes("pipe")) {
      tasks.push({ title: "Diagnose leak", hours: 1 });
      tasks.push({ title: "Replace pipe section", hours: 2 });
      materials.push({ name: "1/2\" PVC pipe (2ft)", qty: 1, unitPrice: 12 });
      materials.push({ name: "Pipe coupler", qty: 1, unitPrice: 4 });
    } else if (text.includes("landscap") || text.includes("sod") || text.includes("mulch")) {
      tasks.push({ title: "Site prep", hours: 2 });
      tasks.push({ title: "Install mulch/sod", hours: 3 * imageFactor });
      materials.push({ name: "Mulch (cu ft)", qty: 12 * imageFactor, unitPrice: 4 });
      materials.push({ name: "Sod (sq ft)", qty: 50 * imageFactor, unitPrice: 0.8 });
    } else {
      tasks.push({ title: "General repair/inspection", hours: 1 * imageFactor });
      materials.push({ name: "Assorted fasteners", qty: 1, unitPrice: 8 });
    }

    const laborTotal = tasks.reduce((s, t) => s + t.hours * baseLabor, 0);
    const materialsTotal = materials.reduce((s, m) => s + m.qty * m.unitPrice, 0);
    const subtotal = Math.round((laborTotal + materialsTotal) * 100) / 100;
    const markup = Math.round(subtotal * 0.12 * 100) / 100;
    const total = Math.round((subtotal + markup) * 100) / 100;

    const materialsWithLinks = materials.map((m) => ({
      ...m,
      link: `https://www.homedepot.com/s/${encodeURIComponent(m.name)}`,
    }));

    return {
      tasks,
      materials: materialsWithLinks,
      breakdown: { laborTotal, materialsTotal, markup, total },
      note: "Instant on-site estimate. Final quote subject to inspection."
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
              <div className="icon-box cyan">jq</div>
              <div>
                <h2 className="card-title">Voice Description</h2>
                <p className="card-desc">Describe the job details</p>
              </div>
            </div>
            <VoiceRecorder transcript={transcript} setTranscript={setTranscript} />
          </div>

        </div>

        <div className="action-area">
          <button className="cta-btn" onClick={handleEstimate} disabled={loading}>
            {loading ? "Analyzing Job Site..." : "✨ Generate Quote & Materials"}
          </button>
        </div>

        {estimate && <EstimateCard estimate={estimate} />}
      </main>
    </div>
  );
}