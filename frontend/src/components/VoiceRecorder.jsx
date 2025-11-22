import React, { useState, useEffect } from "react";

export default function VoiceRecorder({ transcript, setTranscript }) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onresult = (e) => {
      const text = Array.from(e.results).map((r) => r[0].transcript).join("");
      setTranscript(text);
    };
    recognition.onend = () => setListening(false);

    window._toolbelt_recognition = recognition;
    return () => {
      if (window._toolbelt_recognition) {
        window._toolbelt_recognition.onresult = null;
        window._toolbelt_recognition.onend = null;
      }
    };
  }, [setTranscript]);

  function toggleListen() {
    const r = window._toolbelt_recognition;
    if (!r) return;
    if (!listening) {
      r.start();
      setListening(true);
    } else {
      r.stop();
      setListening(false);
    }
  }

  return (
    <div className="mic-wrapper">
      <button 
        className={`mic-btn ${listening ? "recording" : ""}`} 
        onClick={toggleListen}
        disabled={!supported}
      >
        {listening ? "II" : "🎙️"}
      </button>
      
      <div style={{marginBottom: '15px', textAlign: 'center'}}>
         <span style={{fontSize: '0.9rem', color: listening ? '#ef4444' : 'var(--text-muted)', fontWeight: 600}}>
            {listening ? "Listening..." : "Tap to Describe Job"}
         </span>
      </div>

      <textarea
        className="glass-input"
        rows={3}
        placeholder="Or type details here (e.g., 'Leaking pipe under kitchen sink...')"
        value={transcript}
        onChange={(e) => setTranscript(e.target.value)}
      />
    </div>
  );
}