import React, { useState, useEffect, useRef } from "react";

export default function VoiceRecorder({ transcript, setTranscript, onEstimateReceived }) {
  const [listening, setListening] = useState(false);
  const [supported, setSupported] = useState(true);
  const [conversationLog, setConversationLog] = useState([]);
  const [processing, setProcessing] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [conversationLog, processing]);

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return;
    }
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = async (e) => {
      const text = Array.from(e.results).map((r) => r[0].transcript).join("");
      await sendMessage(text, true); // true = from voice
    };
    
    recognition.onend = () => setListening(false);

    window._toolbelt_recognition = recognition;
    return () => {
      if (window._toolbelt_recognition) {
        window._toolbelt_recognition.onresult = null;
        window._toolbelt_recognition.onend = null;
      }
    };
  }, []);

  const sendMessage = async (messageText, fromVoice = false) => {
    if (!messageText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: messageText,
      sender: "user",
      timestamp: new Date(),
      fromVoice
    };

    setConversationLog(prev => [...prev, userMessage]);
    
    if (!fromVoice) {
      setTranscript(""); // Clear text input only if typed
    }
    
    setProcessing(true);

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText })
      });
      const data = await response.json();
      
      const aiMessage = {
        id: Date.now() + 1,
        text: data.response,
        sender: "assistant",
        timestamp: new Date(),
        estimate: data.estimate, // Include estimate data if present
        features: data.features  // Include extracted features if present
      };

      setConversationLog(prev => [...prev, aiMessage]);
      
      // If an estimate was generated, notify the parent component
      if (data.estimate && onEstimateReceived) {
        onEstimateReceived(data.estimate, data.features);
      }
      
      // Speak the response if it was a voice interaction
      if (fromVoice && window.speechSynthesis) {
        const utterance = new SpeechSynthesisUtterance(data.response);
        window.speechSynthesis.speak(utterance);
      }
    } catch (error) {
      console.error('Error communicating with AI:', error);
      setConversationLog(prev => [...prev, { 
        id: Date.now() + 1,
        sender: 'assistant', 
        text: 'Sorry, I had trouble processing that. Please try again.',
        timestamp: new Date(),
      }]);
    }
    setProcessing(false);
  };

  function toggleListen() {
    const r = window._toolbelt_recognition;
    if (!r) return;
    if (!listening && !processing) {
      r.start();
      setListening(true);
    } else {
      r.stop();
      setListening(false);
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage(transcript, false);
    }
  };

  const handleSendClick = () => {
    sendMessage(transcript, false);
  };

  return (
    <div className="mic-wrapper">
      <button 
        className={`mic-btn ${listening ? "recording" : ""}`} 
        onClick={toggleListen}
        disabled={!supported || processing}
      >
        {listening ? "II" : processing ? "⏳" : "🎙️"}
      </button>
      
      <div style={{marginBottom: '15px', textAlign: 'center'}}>
         <span style={{fontSize: '0.9rem', color: listening ? '#ef4444' : processing ? '#f59e0b' : 'var(--text-muted)', fontWeight: 600}}>
            {listening ? "Listening..." : processing ? "Processing..." : "Tap to Describe Job"}
         </span>
      </div>

      {/* Conversation History Box */}
      {conversationLog.length > 0 && (
        <div style={{
          marginBottom: '15px',
          maxHeight: '300px',
          overflowY: 'auto',
          padding: '12px',
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '8px',
          border: '1px solid rgba(255, 255, 255, 0.1)'
        }}>
          <div style={{ 
            marginBottom: '10px', 
            fontSize: '0.85rem', 
            color: 'var(--text-muted)',
            fontWeight: 600,
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
            paddingBottom: '8px'
          }}>
            Conversation:
          </div>
          {conversationLog.map((message) => (
            <div 
              key={message.id} 
              style={{ 
                marginBottom: '12px', 
                padding: '10px',
                backgroundColor: message.sender === 'user' ? 'rgba(96, 165, 250, 0.1)' : 'rgba(52, 211, 153, 0.1)',
                borderRadius: '8px',
                borderLeft: `3px solid ${message.sender === 'user' ? '#60a5fa' : '#34d399'}`
              }}
            >
              <div style={{ 
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '4px'
              }}>
                <strong style={{ 
                  color: message.sender === 'user' ? '#60a5fa' : '#34d399',
                  fontSize: '0.85rem'
                }}>
                  {message.sender === 'user' ? 'You' : 'AI Assistant'}
                </strong>
                {message.fromVoice && (
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    🎤 voice
                  </span>
                )}
              </div>
              <div style={{ color: '#e5e7eb', lineHeight: '1.5', fontSize: '0.9rem' }}>
                {message.text}
              </div>
              {message.estimate && (
                <div style={{ 
                  marginTop: '10px',
                  padding: '10px',
                  backgroundColor: 'rgba(34, 197, 94, 0.15)',
                  borderRadius: '6px',
                  border: '1px solid rgba(34, 197, 94, 0.3)'
                }}>
                  <div style={{ 
                    fontWeight: 'bold', 
                    color: '#22c55e',
                    marginBottom: '6px',
                    fontSize: '0.85rem'
                  }}>
                    💰 Estimate Generated:
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#e5e7eb' }}>
                    <div>Cost: £{message.estimate.cost_gbp} (DZD {message.estimate.cost_dzd})</div>
                    <div>Time: {message.estimate.time_days} days</div>
                  </div>
                </div>
              )}
            </div>
          ))}
          {processing && (
            <div style={{ 
              padding: '10px',
              backgroundColor: 'rgba(52, 211, 153, 0.1)',
              borderRadius: '8px',
              borderLeft: '3px solid #34d399'
            }}>
              <span style={{ color: '#34d399', fontSize: '0.85rem' }}>AI is thinking...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      )}

      {/* Text Input with Send Button */}
      <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
        <textarea
          className="glass-input"
          rows={3}
          placeholder="Or type details here (e.g., 'Leaking pipe under kitchen sink...')"
          value={transcript}
          onChange={(e) => setTranscript(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={processing}
          style={{ flex: 1 }}
        />
        <button
          onClick={handleSendClick}
          disabled={!transcript.trim() || processing}
          style={{
            padding: '10px 16px',
            backgroundColor: transcript.trim() && !processing ? '#60a5fa' : 'rgba(255, 255, 255, 0.1)',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            cursor: transcript.trim() && !processing ? 'pointer' : 'not-allowed',
            fontSize: '1.2rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            height: '48px',
            transition: 'all 0.3s ease'
          }}
        >
          ➤
        </button>
      </div>
    </div>
  );
}