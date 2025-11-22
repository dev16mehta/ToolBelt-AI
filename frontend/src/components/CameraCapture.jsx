import React from "react";

export default function CameraCapture({ images, setImages }) {
  function handleFiles(e) {
    const files = Array.from(e.target.files || []);
    const urls = files.map((f) => ({ file: f, url: URL.createObjectURL(f) }));
    setImages((prev) => [...prev, ...urls]);
  }

  function removeImage(idx) {
    setImages((prev) => {
      const copy = [...prev];
      copy.splice(idx, 1);
      return copy;
    });
  }

  return (
    <section className="card">
      <h2>Photos</h2>
      <p className="hint">Take a few photos of the job area. Use the camera button for mobile.</p>
      <div className="controls">
        <label className="camera-btn">
          📷 Take Photo
          <input accept="image/*" capture="environment" type="file" onChange={handleFiles} multiple />
        </label>
      </div>

      <div className="thumbs">
        {images.map((img, i) => (
          <div className="thumb" key={i}>
            <img src={img.url} alt={`capture-${i}`} />
            <button className="remove" onClick={() => removeImage(i)}>✕</button>
          </div>
        ))}
      </div>
    </section>
  );
}
