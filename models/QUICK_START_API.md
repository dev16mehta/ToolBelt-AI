# Quick Start - Plumbing Cost Estimator API

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
cd models
pip install -r requirements.txt
```

### Step 2: Start the API

```bash
uvicorn api:app --reload
```

The API will start at `http://localhost:8000`

### Step 3: Test the API

Open a new terminal and run:

```bash
python test_api.py
```

Or visit the interactive documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📡 API Endpoint

### POST /estimate

Send a job description, get cost and time estimate.

**Example Request:**
```bash
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Install luxury bathroom with wall-hung toilet and shower"}'
```

**Example Response:**
```json
{
  "success": true,
  "job_description": "Install luxury bathroom with wall-hung toilet and shower",
  "cost_dzd": 336430.41,
  "cost_gbp": 1884.01,
  "time_days": 26.6,
  "features": {
    "toilet": 1,
    "toileType": "Wall-Hung",
    "showerCabin": 1,
    "showerCabinType": "Luxury_Enclosure"
  }
}
```

## 🎨 Frontend Integration

### JavaScript (Fetch)

```javascript
const response = await fetch('http://localhost:8000/estimate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    job_description: 'Install luxury bathroom with wall-hung toilet and shower'
  })
});

const data = await response.json();
console.log(`Cost: £${data.cost_gbp}`);
console.log(`Time: ${data.time_days} days`);
```

### React (axios)

```javascript
import axios from 'axios';

const getEstimate = async (description) => {
  const { data } = await axios.post('http://localhost:8000/estimate', {
    job_description: description
  });
  return data;
};
```

## 📝 Key Features

- ✅ **Natural Language Input**: Just describe the job in plain English
- ✅ **Dual Currency**: Returns costs in both DZD and GBP
- ✅ **Feature Extraction**: Shows what features were detected
- ✅ **Fast Response**: Typically responds in 2-3 seconds
- ✅ **CORS Enabled**: Ready for frontend integration
- ✅ **Auto Documentation**: Interactive API docs included

## 🔧 Configuration

Create a `.env` file in the `models/` directory:

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
```

## 📚 More Information

- **Full API Documentation**: [API_USAGE.md](API_USAGE.md)
- **Interactive Docs**: http://localhost:8000/docs (when server is running)

## ⚡ Quick Test

```bash
# Health check
curl http://localhost:8000/health

# Get estimate
curl -X POST http://localhost:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Budget bathroom: 1 toilet, 1 shower, 1 sink"}'
```

## 🛠️ Troubleshooting

**API won't start?**
- Ensure model exists: `models/production/plumbing_model_v1.0.0.joblib`
- If missing, run: `python model.py`

**Authentication errors?**
- Check `.env` file has valid `OPENAI_API_KEY`

**Different port?**
```bash
uvicorn api:app --reload --port 8001
```

---

That's it! Your API is ready to use. For detailed documentation, see [API_USAGE.md](API_USAGE.md).
