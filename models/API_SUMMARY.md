# Plumbing Cost Estimator API - Summary

## 🎯 What It Does

The API accepts natural language descriptions of plumbing jobs and returns:
- **Cost estimate** in Algerian Dinar (DZD) and British Pounds (GBP)
- **Time estimate** in days
- **Extracted features** showing what was detected from the description

## 🏗️ Architecture

```
User Input (Natural Language)
    ↓
Feature Extractor (ChatGPT)
    ↓
Extracted Features (JSON)
    ↓
ML Models (XGBoost + Ridge)
    ↓
Cost & Time Predictions
    ↓
Currency Conversion (DZD → GBP)
    ↓
JSON Response
```

## 📁 Files Created

### Core API Files
- **`api.py`** - FastAPI application with `/estimate` endpoint
- **`test_api.py`** - Test client for the API
- **`requirements.txt`** - Updated with FastAPI dependencies

### Documentation
- **`QUICK_START_API.md`** - Quick start guide
- **`API_USAGE.md`** - Comprehensive API documentation
- **`API_SUMMARY.md`** - This file

### Supporting Files (Already Existed)
- **`services/feature_extractor.py`** - ChatGPT feature extraction
- **`predict.py`** - Prediction logic
- **`models/production/plumbing_model_v1.0.0.joblib`** - Trained models
- **`.env`** - OpenAI API configuration

## 🚀 How to Use

### Start the Server
```bash
cd models
uvicorn api:app --reload
```

### Make a Request
```bash
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Install luxury bathroom with toilet and shower"}'
```

### Response Example
```json
{
  "success": true,
  "job_description": "Install luxury bathroom with toilet and shower",
  "cost_dzd": 336430.41,
  "cost_gbp": 1884.01,
  "time_days": 26.6,
  "features": {
    "toilet": 1,
    "toileType": "Wall-Hung",
    "showerCabin": 1,
    "showerCabinType": "Luxury_Enclosure",
    ...
  }
}
```

## 🎨 Frontend Integration

### Basic Fetch Example
```javascript
async function getEstimate(jobDescription) {
  const response = await fetch('http://localhost:8000/estimate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ job_description: jobDescription })
  });
  return await response.json();
}

// Usage
const result = await getEstimate('Install luxury bathroom');
console.log(`Cost: £${result.cost_gbp}, Time: ${result.time_days} days`);
```

### React Component Example
```jsx
import { useState } from 'react';
import axios from 'axios';

function PlumbingEstimator() {
  const [description, setDescription] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const getEstimate = async () => {
    setLoading(true);
    try {
      const { data } = await axios.post('http://localhost:8000/estimate', {
        job_description: description
      });
      setResult(data);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Describe your plumbing job..."
      />
      <button onClick={getEstimate} disabled={loading}>
        {loading ? 'Estimating...' : 'Get Estimate'}
      </button>

      {result && (
        <div>
          <h3>Estimate</h3>
          <p>Cost: {result.cost_dzd.toLocaleString()} DZD (£{result.cost_gbp.toLocaleString()})</p>
          <p>Time: {result.time_days} days</p>
        </div>
      )}
    </div>
  );
}
```

## 🔧 Key Features

### 1. Natural Language Processing
- Uses ChatGPT (gpt-4o-mini) to extract structured features
- Understands context: "luxury", "budget", "master bathroom", etc.
- Handles various formats and descriptions

### 2. Machine Learning Prediction
- **Cost Model**: XGBoost (R² = 0.9+)
- **Time Model**: Ridge Regression
- Trained on plumbing service data

### 3. Dual Currency Support
- Primary: Algerian Dinar (DZD)
- Secondary: British Pounds (GBP)
- Exchange rate: 1 DZD ≈ £0.0056

### 4. CORS Enabled
- Ready for cross-origin requests
- Works with any frontend framework
- Configurable allowed origins

### 5. Auto Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Interactive testing interface

## 📊 Performance

- **Average Response Time**: 2-3 seconds
- **Accuracy**: High (R² > 0.9 on test data)
- **Uptime**: Depends on hosting
- **Rate Limits**: Based on OpenAI API limits

## 🔐 Security Considerations

### Current Setup (Development)
- CORS allows all origins (`allow_origins=["*"]`)
- API key stored in `.env` file
- No authentication required

### Production Recommendations
1. **Restrict CORS** to specific frontend domains
2. **Add API authentication** (API keys, JWT, etc.)
3. **Rate limiting** to prevent abuse
4. **Environment variables** for sensitive data
5. **HTTPS only** in production
6. **Input validation** and sanitization
7. **Error logging** and monitoring

## 💰 Cost Estimate

Using the API incurs costs from:
- **OpenAI API**: ~$0.15-$0.60 per 1M input tokens (gpt-4o-mini)
- **Server hosting**: Depends on provider

Estimated cost per request: ~$0.001-$0.005

## 🚧 Limitations

1. **OpenAI API dependency**: Requires valid API key
2. **English language**: Best results with English descriptions
3. **Domain specific**: Trained for plumbing jobs only
4. **Model assumptions**: Based on training data patterns

## 🔮 Future Enhancements

Potential improvements:
1. **Caching**: Cache similar descriptions to reduce API calls
2. **Batch processing**: Handle multiple jobs at once
3. **User authentication**: Track usage per user
4. **History**: Store past estimates
5. **PDF generation**: Generate detailed quotes
6. **Multi-language**: Support other languages
7. **Real-time updates**: WebSocket support for live estimates

## 📞 Support

- **API Docs**: http://localhost:8000/docs
- **Test Suite**: Run `python test_api.py`
- **Health Check**: http://localhost:8000/health

## 📄 License

Part of the ToolBelt-AI project.

---

**Ready to integrate?** See [QUICK_START_API.md](QUICK_START_API.md) for a quick start guide!
