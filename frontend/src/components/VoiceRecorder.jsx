import React, { useState, useEffect } from "react";

export default function VoiceRecorder({ transcript, setTranscript }) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);
  let recognition = null;

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = true;
    recognition.continuous = false;

    recognition.onresult = (e) => {
      const text = Array.from(e.results).map((r) => r[0].transcript).join("");
      setTranscript(text);
    };
    recognition.onend = () => setListening(false);

    // store to window to use in handlers
    window._toolbelt_recognition = recognition;
    // cleanup
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
    <section className="card">
      <h2>Describe the job</h2>
      {!supported ? (
        <p className="hint">Voice not supported — enter a short description below.</p>
      ) : (
        <p className="hint">Tap record and speak: e.g., "Leaking sink, pipe behind cabinet, small puddle on floor."</p>
      )}

      <div className="voice-row">
        <button className={`mic ${listening ? "on" : ""}`} onClick={toggleListen} disabled={!supported}>
          {listening ? "● Recording" : "● Record"}
        </button>
        <textarea
          className="desc"
          placeholder="Or type a short description..."
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
        />
      </div>
    </section>
  );
}
