# Plumbing Cost Estimator API - Usage Guide

## Quick Start

### 1. Install Dependencies

```bash
cd models
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
uvicorn api:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### POST /estimate

Get cost and time estimates for a plumbing job.

**Request:**
```json
{
  "job_description": "I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink"
}
```

**Response:**
```json
{
  "success": true,
  "job_description": "I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink",
  "cost_dzd": 450000.00,
  "cost_gbp": 2520.00,
  "time_days": 12.5,
  "features": {
    "boilerSize": "medium",
    "radiator": 5,
    "radiatorType": "Primavera_H500",
    "toilet": 1,
    "toileType": "Wall-Hung",
    "washbasin": 1,
    "washbasinType": "Pedestal",
    "bathhub": 0,
    "bathhubType": "Standard",
    "showerCabin": 1,
    "showerCabinType": "Luxury_Enclosure",
    "Bidet": 0,
    "BidetType": "Bidet-Mixer-Tap",
    "waterHeater": 1,
    "waterHeaterType": "Electric-50liters",
    "sinkTypeQuality": "high",
    "sinkCategorie": "single"
  }
}
```

### GET /health

Check if the API and its services are healthy.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "feature_extractor": "ready",
    "predictor": "ready"
  }
}
```

### GET /

Get API information and available endpoints.

### GET /docs

Interactive API documentation (Swagger UI) - Visit in browser

### GET /redoc

Alternative API documentation (ReDoc) - Visit in browser

## Example Usage

### Using cURL

```bash
curl -X POST "http://localhost:8000/estimate" \
  -H "Content-Type: application/json" \
  -d '{"job_description": "Complete plumbing for a 3-bedroom house: 3 bathrooms, kitchen with double sink, big boiler, 8 radiators"}'
```

### Using Python requests

```python
import requests

# Make prediction
response = requests.post(
    "http://localhost:8000/estimate",
    json={
        "job_description": "Budget bathroom renovation: basic fixtures, 1 toilet, 1 shower, 1 sink"
    }
)

result = response.json()
print(f"Cost: {result['cost_dzd']:,.2f} DZD (£{result['cost_gbp']:,.2f})")
print(f"Time: {result['time_days']} days")
```

### Using JavaScript (Fetch API)

```javascript
fetch('http://localhost:8000/estimate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    job_description: 'Install a master bathroom with bathtub, separate shower cabin, 2 washbasins'
  })
})
  .then(response => response.json())
  .then(data => {
    console.log(`Cost: ${data.cost_dzd.toLocaleString()} DZD (£${data.cost_gbp.toLocaleString()})`);
    console.log(`Time: ${data.time_days} days`);
  });
```

### Using React (with axios)

```javascript
import axios from 'axios';

const getEstimate = async (jobDescription) => {
  try {
    const response = await axios.post('http://localhost:8000/estimate', {
      job_description: jobDescription
    });

    return {
      costDZD: response.data.cost_dzd,
      costGBP: response.data.cost_gbp,
      timeDays: response.data.time_days,
      features: response.data.features
    };
  } catch (error) {
    console.error('Estimation failed:', error.response?.data);
    throw error;
  }
};

// Usage in component
const estimate = await getEstimate('Add a half bath with one toilet and wall-mounted sink');
console.log(`Estimated cost: £${estimate.costGBP}`);
```

## Error Handling

### 400 Bad Request
Invalid input (e.g., job description too short or empty)

```json
{
  "detail": {
    "success": false,
    "error": "Invalid input",
    "detail": "Job description cannot be empty"
  }
}
```

### 500 Internal Server Error
Service error (e.g., API key issue, model not found)

```json
{
  "detail": {
    "success": false,
    "error": "Estimation failed",
    "detail": "ChatGPT API call failed: ..."
  }
}
```

## Configuration

### Environment Variables

Create a `.env` file in the `models/` directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### Currency Exchange Rate

The default DZD to GBP exchange rate is set to 0.0056 in `api.py`. To update it, modify the `DZD_TO_GBP_RATE` constant.

### CORS Settings

By default, the API allows requests from all origins (`allow_origins=["*"]`). For production, update this in `api.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Production Deployment

### Using Docker

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t plumbing-api .
docker run -p 8000:8000 --env-file .env plumbing-api
```

### Using Gunicorn (for production)

```bash
pip install gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Monitoring and Logging

Access logs are automatically generated by Uvicorn. For custom logging:

```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## Troubleshooting

### API won't start
- Ensure model file exists: `models/production/plumbing_model_v1.0.0.joblib`
- Run `python model.py` to train the model if missing

### Authentication errors
- Check `.env` file has valid `OPENAI_API_KEY`
- Verify API key has access to the specified model

### CORS issues
- Update `allow_origins` in `api.py` to include your frontend URL
- Ensure frontend sends correct headers

### Port already in use
```bash
uvicorn api:app --reload --port 8001  # Use different port
```

## Support

For issues or questions, refer to:
- API documentation: http://localhost:8000/docs
- Project README: ../README.md
