import React from "react";

export default function CameraCapture({ images, setImages }) {
  
  function handleFiles(e) {
    const files = Array.from(e.target.files || []);
    if (files.length === 0) return;
    
    const urls = files.map((f) => ({ 
      file: f, 
      url: URL.createObjectURL(f) 
    }));
    setImages((prev) => [...prev, ...urls]);
  }

  function removeImage(idx) {
    setImages((prev) => prev.filter((_, i) => i !== idx));
  }

  return (
    <div style={{display: 'flex', flexDirection: 'column', height: '100%'}}>
      {/* Hidden Input wrapped in Styled Label */}
      <label className="dropzone-area">
        <input 
          type="file" 
          accept="image/*" 
          capture="environment" 
          onChange={handleFiles} 
          multiple 
          style={{ display: "none" }} 
        />
        <div className="dropzone-icon">📸</div>
        <span className="dropzone-text">Click to Snap or Upload</span>
        <span className="dropzone-sub">Supports JPG, PNG (Max 10MB)</span>
      </label>

      {/* Preview Grid */}
      {images.length > 0 && (
        <div className="preview-grid">
          {images.map((img, i) => (
            <div className="thumb-wrapper" key={i}>
              <img src={img.url} alt="thumb" className="thumb-img" />
              <button className="remove-btn" onClick={() => removeImage(i)}>✕</button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}