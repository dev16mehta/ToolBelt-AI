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
    setLoading(true);
    // Placeholder client-side estimator. Replace with API call to your agent.
    const result = generateEstimate(images, transcript);
    // Simulate small delay
    await new Promise((r) => setTimeout(r, 600));
    setEstimate(result);
    setLoading(false);
  }

  function generateEstimate(images, transcript) {
    // Simple heuristic-based sample estimator
    const baseLabor = 75; // per hour
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

    // Generate supplier links (search URLs)
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
    <div className="app">
      <header className="topbar">
        <h1>Toolbelt AI</h1>
        <p className="sub">Instant Job Estimator & Materials Requisition</p>
      </header>

      <main className="panel">
        <CameraCapture images={images} setImages={setImages} />
        <VoiceRecorder transcript={transcript} setTranscript={setTranscript} />

        <div className="actions">
          <button className="primary" onClick={handleEstimate} disabled={loading}>
            {loading ? "Estimating…" : "Estimate Now"}
          </button>
        </div>

        {estimate && <EstimateCard estimate={estimate} images={images} transcript={transcript} />}
      </main>

      <footer className="footer">
        <small>Mobile-first — voice + photo workflow for contractors</small>
      </footer>
    </div>
  );
}
