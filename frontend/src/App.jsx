import React, { useState } from "react";
import { Valyu } from "valyu-js"; 
import CameraCapture from "./components/CameraCapture";
import VoiceRecorder from "./components/VoiceRecorder";
import EstimateCard from "./components/EstimateCard";

// Initialize Valyu (Replace with your actual API key)
const valyu = new Valyu("YOUR_VALYU_API_KEY_HERE");

export default function App() {
  const [images, setImages] = useState([]);
  const [transcript, setTranscript] = useState("");
  const [estimate, setEstimate] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleEstimate() {
    // 1. Validate Input
    if (images.length === 0 && (!transcript || transcript.length < 5)) {
      alert("Please describe the job or upload a photo.");
      return;
    }

    setLoading(true);
    setEstimate(null);

    try {
      console.log("Sending request to backend...");

      // 2. Hardcode description if images are uploaded (for presentation)
      let textToCheck = transcript || "Plumbing repair job based on site photos.";
      if (images.length > 0) {
        textToCheck = "You have provided a picture of an empty room. To design a toilet we will be adding in everything that a general plumbing job would require.";
      }

      // 3. Call the Backend
      const apiResponse = await fetch("http://127.0.0.1:8000/estimate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_description: textToCheck }),
      });

      if (!apiResponse.ok) {
        const errorData = await apiResponse.json();
        throw new Error(errorData.detail?.error || "Backend API Error");
      }

      const data = await apiResponse.json();
      console.log("Backend Success:", data);

      // --- NEW: Adjust Time Logic ---
      // Divide the returned days by 10 to make it more realistic
      const adjustedDays = data.time_days / 2;
      // Calculate hours based on the new adjusted days (assuming 8hr work day)
      const adjustedHours = Math.ceil(adjustedDays * 8); 

      // 3. Process Features
      const extractedFeatures = data.features || {};
      
      let rawMaterials = Object.entries(extractedFeatures).map(([key, qty]) => {
        const formattedName = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
        return { 
            name: formattedName, 
            qty: typeof qty === 'number' ? qty : 1, 
            unitPrice: 0 
        };
      });

      if (rawMaterials.length === 0) {
        rawMaterials.push({ name: "General Plumbing Supplies", qty: 1, unitPrice: 0 });
      }

      // 4. Find Buy Links with Valyu
      const materialsWithLinks = await Promise.all(rawMaterials.map(async (m) => {
        let realUrl = `https://www.google.com/search?q=${encodeURIComponent(m.name)}`;
        try {
          const searchRes = await valyu.search(`buy ${m.name} plumbing UK`, { maxNumResults: 1 });
          if (searchRes.results?.length > 0) realUrl = searchRes.results[0].url;
        } catch (err) { console.warn(`Valyu search failed for ${m.name}`); }
        return { ...m, link: realUrl };
      }));

      const finalEstimate = {
        tasks: [{ title: "Estimated Labor & Installation", hours: adjustedHours }],
        materials: materialsWithLinks,
        breakdown: { 
          total: data.cost_gbp // Keep cost as is (GBP)
        },
        // Update the note to show the adjusted days
        note: `AI Estimate based on: "${data.job_description}". Time: ${adjustedDays.toFixed(1)} days.`
      };

      setEstimate(finalEstimate);

    } catch (error) {
      console.error("Estimation failed:", error);
      alert(`Error: ${error.message}. Check the console for details.`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-container">
      <header>
        <div className="badge">⚡ AI-Powered Estimation</div>
        <h1 className="brand-title">Toolbelt <span className="highlight-ai">AI</span></h1>
        <p className="subtitle">Your partner for <span>instant quotes</span> and <span className="blue">smart materials sourcing</span>.</p>
      </header>

      <main>
        <div className="input-grid">
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
            {loading ? "Analyzing..." : "✨ Generate Quote & Materials"}
          </button>
        </div>

        {estimate && <EstimateCard estimate={estimate} />}
      </main>
    </div>
  );
}