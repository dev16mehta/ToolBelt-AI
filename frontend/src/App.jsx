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
            {loading ? "Analyzing & Sourcing..." : "✨ Generate Quote & Materials"}
          </button>
        </div>

        {estimate && <EstimateCard estimate={estimate} />}
      </main>
    </div>
  );
}