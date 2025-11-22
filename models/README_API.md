# Plumbing Cost Estimator API 🔧

A FastAPI-based REST API that provides instant cost and time estimates for plumbing jobs using natural language descriptions.

## ✨ Features

- 🤖 **AI-Powered**: Uses ChatGPT to extract features from natural language
- 📊 **ML Predictions**: XGBoost and Ridge Regression models for accurate estimates
- 💰 **Dual Currency**: Returns costs in both DZD and GBP
- ⚡ **Fast**: Typically responds in 2-3 seconds
- 📚 **Auto Documentation**: Built-in Swagger UI and ReDoc
- 🌐 **CORS Enabled**: Ready for frontend integration

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
OPENAI_MODEL=gpt-4o-mini
```

### 3. Start the Server

```bash
uvicorn api:app --reload
```

Server starts at `http://localhost:8000`

### 4. Test the API

```bash
python test_api.py
```

Or visit `http://localhost:8000/docs` for interactive documentation.

## 📡 API Endpoints

### POST /estimate

Get cost and time estimate from job description.

**Request:**
```json
{
  "job_description": "Install luxury bathroom with wall-hung toilet and shower"
}
```

**Response:**
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

### GET /health

Health check endpoint.

### GET /docs

Interactive API documentation (Swagger UI).

### GET /redoc

Alternative API documentation (ReDoc).

## 🎨 Frontend Integration

### Simple HTML Example

Open `example_frontend.html` in a browser (requires API running):

```bash
# Start API first
uvicorn api:app --reload

# Then open example_frontend.html in your browser
```

### JavaScript Fetch

```javascript
const response = await fetch('http://localhost:8000/estimate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    job_description: 'Install luxury bathroom'
  })
});

const data = await response.json();
console.log(`Cost: £${data.cost_gbp}, Time: ${data.time_days} days`);
```

### React with Axios

```javascript
import axios from 'axios';

const { data } = await axios.post('http://localhost:8000/estimate', {
  job_description: 'Install luxury bathroom'
});

console.log(data.cost_gbp, data.time_days);
```

## 📁 Project Structure

```
models/
├── api.py                      # FastAPI application
├── test_api.py                 # API test client
├── example_frontend.html       # Example HTML frontend
├── services/
│   └── feature_extractor.py   # ChatGPT feature extraction
├── predict.py                  # Prediction logic
├── models/production/
│   └── plumbing_model_v1.0.0.joblib  # Trained models
├── .env                        # Environment configuration
└── requirements.txt            # Python dependencies
```

## 📚 Documentation

- **Quick Start**: [QUICK_START_API.md](QUICK_START_API.md)
- **Full API Documentation**: [API_USAGE.md](API_USAGE.md)
- **Summary**: [API_SUMMARY.md](API_SUMMARY.md)
- **Interactive Docs**: http://localhost:8000/docs (when running)

## 🔧 How It Works

1. **User Input**: Natural language job description
2. **Feature Extraction**: ChatGPT extracts 17 structured features
3. **Prediction**: ML models predict cost and time
4. **Currency Conversion**: DZD to GBP conversion
5. **Response**: JSON with estimates and features

## 🧪 Testing

Run the test suite:

```bash
python test_api.py
```

This will:
- Check API health
- Test 5 example job descriptions
- Display results and performance metrics

## 🔒 Security

**Development Setup:**
- CORS allows all origins
- No authentication required
- API key stored in `.env`

**Production Recommendations:**
1. Restrict CORS to specific domains
2. Add API authentication (JWT, API keys)
3. Implement rate limiting
4. Use HTTPS only
5. Add request validation
6. Enable logging and monitoring

## 📊 Performance

- **Response Time**: 2-3 seconds average
- **Accuracy**: R² > 0.9 on test data
- **Cost per Request**: ~$0.001-$0.005 (OpenAI API)

## 🛠️ Troubleshooting

**API won't start:**
```bash
# Check if model exists
ls models/production/plumbing_model_v1.0.0.joblib

# If missing, train the model
python model.py
```

**OpenAI API errors:**
- Verify `.env` has valid `OPENAI_API_KEY`
- Check API key has access to `gpt-4o-mini`

**Port already in use:**
```bash
uvicorn api:app --reload --port 8001
```

**CORS errors:**
- Update `allow_origins` in `api.py`
- Ensure frontend sends correct headers

## 💡 Example Use Cases

1. **Budget Bathroom**: "Basic bathroom with 1 toilet, 1 shower, 1 sink"
   - Result: ~100,000 DZD (£560), 15 days

2. **Luxury Bathroom**: "Luxury bathroom with wall-hung toilet, premium shower, marble sink"
   - Result: ~350,000 DZD (£1,960), 25 days

3. **Complete House**: "3-bedroom house with 3 bathrooms, big boiler, 8 radiators"
   - Result: ~800,000 DZD (£4,480), 45 days

## 🚧 Known Limitations

- Requires OpenAI API access
- English language works best
- Domain-specific (plumbing only)
- Based on training data patterns

## 🔮 Future Enhancements

- [ ] Request caching to reduce API costs
- [ ] Batch processing support
- [ ] User authentication and tracking
- [ ] Estimate history storage
- [ ] PDF quote generation
- [ ] Multi-language support
- [ ] WebSocket for real-time updates

## 📞 Support

- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Test Suite**: `python test_api.py`

## 📄 License

Part of the ToolBelt-AI project.

---

**Ready to integrate?** Check out [QUICK_START_API.md](QUICK_START_API.md) or the [example frontend](example_frontend.html)!
