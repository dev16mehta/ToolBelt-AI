# Plumbing Service Prediction Models

This directory contains trained machine learning models for predicting plumbing service **cost** and **time** based on equipment specifications.

---

## Model Performance (v1.0.0)

### Cost Prediction Model (XGBoost)

| Metric | Value | Description |
|--------|-------|-------------|
| **R² Score** | **0.9767** | Explains 97.67% of cost variation (excellent) |
| **RMSE** | **$52,653** | Root mean squared error |
| **MAE** | **$40,628** | Average prediction error |
| **CV Mean** | **0.9405** | Cross-validation R² (5-fold) |
| **CV Std** | **±0.0095** | Cross-validation standard deviation |

**Key Features Influencing Cost:**
1. `radiatorType_GLOBAL_ISEO_350` (59.06% importance)
2. `radiator` count (14.34%)
3. `showerCabin` count (11.52%)
4. `bathhub` count (3.29%)
5. `waterHeater` count (1.62%)

### Time Prediction Model (Ridge Regression)

| Metric | Value | Description |
|--------|-------|-------------|
| **R² Score** | **0.8561** | Explains 85.61% of time variation (very good) |
| **RMSE** | **6.00 days** | Root mean squared error |
| **MAE** | **4.99 days** | Average prediction error |
| **CV Mean** | **0.8684** | Cross-validation R² (5-fold) |
| **CV Std** | **±0.0070** | Cross-validation standard deviation |

**Key Features Influencing Time:**
1. `radiator` count (36.90% importance)
2. `showerCabin` count (19.76%)
3. `bathhub` count (6.80%)
4. `waterHeater` count (4.04%)
5. `toilet` count (2.87%)

---

## Model Architecture

### Cost Prediction Pipeline
```
Raw Input → Ordinal Encoding → One-Hot Encoding → XGBoost → log1p inverse → Cost ($)
```

**Algorithm:** XGBoost Regressor
- n_estimators: 100
- max_depth: 8
- learning_rate: 0.1
- random_state: 42

**Target Transformation:** Log1p (handles wide cost range: $21K - $2.2M)

### Time Prediction Pipeline
```
Raw Input → Ordinal Encoding → One-Hot Encoding → StandardScaler → Ridge → Time (days)
```

**Algorithm:** Ridge Regression
- alpha: 1.0
- random_state: 42

**Feature Scaling:** StandardScaler (applied to all features)

---

## Files in This Directory

### Production Models
- `plumbing_model_v1.0.0.joblib` - Complete model package including:
  - XGBoost cost predictor
  - Ridge time predictor
  - StandardScaler for time model
  - Feature encoding mappings
  - Feature names and order

- `metadata_v1.0.0.json` - Model metadata including:
  - Hyperparameters
  - Performance metrics
  - Feature information
  - Training configuration
  - Creation timestamp

### Archived Models
- Previous versions moved to `archived/` directory
- Naming convention: `plumbing_model_v{MAJOR}.{MINOR}.{PATCH}.joblib`

---

## Usage

### Using the Prediction Script

**Example prediction:**
```bash
python predict.py --example
```

**Predict from JSON file:**
```bash
python predict.py --input-file my_job.json
```

Example `my_job.json`:
```json
{
  "boilerSize": "medium",
  "radiator": 5,
  "radiatorType": "GLOBAL_ISEO_350",
  "toilet": 2,
  "toileType": "Wall-Hung",
  "washbasin": 2,
  "washbasinType": "Integrated",
  "bathhub": 1,
  "bathhubType": "Standard",
  "showerCabin": 1,
  "showerCabinType": "Standard_Enclosure",
  "Bidet": 1,
  "BidetType": "Bidet-Mixer-Tap",
  "waterHeater": 1,
  "waterHeaterType": "Electric-On-Demand",
  "sinkTypeQuality": "high",
  "sinkCategorie": "Kitchen"
}
```

**Batch prediction from CSV:**
```bash
python predict.py --batch jobs.csv
```

### Using in Python Code

```python
from predict import PlumbingPredictor

# Load the model
predictor = PlumbingPredictor("models/production/plumbing_model_v1.0.0.joblib")

# Make a prediction
input_data = {
    "boilerSize": "medium",
    "radiator": 5,
    "radiatorType": "GLOBAL_ISEO_350",
    # ... other features
}

result = predictor.predict(input_data)
print(f"Cost: {result['cost_formatted']}")
print(f"Time: {result['time_formatted']}")
```

---

## Model Versioning

**Current Version:** v1.0.0

### Version History

#### v1.0.0 (2025-11-22)
- Initial production release
- Trained on 3,000 plumbing service records
- Features: 17 input features → 27 after encoding
- Train/test split: 80/20 (2,400 / 600 samples)
- Cost model R²: 0.9767 (XGBoost)
- Time model R²: 0.8561 (Ridge)

### Versioning Policy

**Semantic Versioning:** `MAJOR.MINOR.PATCH`

- **MAJOR:** Breaking changes (different features, incompatible API)
- **MINOR:** New features, model retraining, performance improvements
- **PATCH:** Bug fixes, minor adjustments

---

## Input Features

### Required Features (17 total)

**Ordinal Features:**
- `boilerSize`: `"small"`, `"medium"`, or `"big"`
- `sinkTypeQuality`: `"poor"` or `"high"`

**Categorical Features (one-hot encoded):**
- `radiatorType`: Type/model of radiator
- `toileType`: Type of toilet installation
- `washbasinType`: Washbasin category
- `bathhubType`: Bathtub type
- `showerCabinType`: Shower cabin category
- `BidetType`: Bidet fixture type
- `waterHeaterType`: Water heater category
- `sinkCategorie`: Sink category (Kitchen/Bathroom)

**Numerical Features:**
- `radiator`: Number of radiators (integer, 0-20)
- `toilet`: Number of toilets (integer, 0-10)
- `washbasin`: Number of washbasins (integer, 0-10)
- `bathhub`: Number of bathtubs (integer, 0-5)
- `showerCabin`: Number of shower cabins (integer, 0-5)
- `Bidet`: Number of bidets (integer, 0-5)
- `waterHeater`: Number of water heaters (integer, 0-5)

---

## Model Interpretation

### What Makes Jobs More Expensive?

1. **High-end radiator types** (especially GLOBAL_ISEO_350) dramatically increase cost
2. **More radiators** correlate with larger projects and higher costs
3. **Luxury shower cabins** add significant cost
4. **Multiple fixtures** (bathtubs, water heaters) compound costs

### What Makes Jobs Take Longer?

1. **Number of radiators** is the primary driver of project duration
2. **Multiple shower cabins** require significant installation time
3. **Total fixture count** (more items = more time)
4. **Complex installations** (wall-hung toilets, luxury enclosures)

---

## Model Limitations

1. **Training data range:** Predictions are most accurate for jobs similar to the training set
   - Cost range: $21,000 - $2,200,000
   - Time range: 2 - 91 days

2. **Feature dependencies:** Model assumes standard installation complexity. Unusual site conditions (difficult access, structural issues) are not captured.

3. **Temporal validity:** Costs are based on historical data. Inflation, supply chain changes, or market shifts may require model retraining.

4. **Categorical coverage:** Predictions for equipment types not seen during training may be less accurate.

---

## Retraining the Model

To retrain with new data:

```bash
# 1. Update the CSV file with new records
# 2. Run the training script
python model.py

# 3. Models will be automatically saved to models/production/
# 4. Previous version moved to models/archived/
```

**Recommended retraining frequency:** Quarterly, or when:
- Significant market changes occur
- New equipment types are introduced
- Model performance degrades (monitor in production)
- Additional training data becomes available (>500 new records)

---

## Model Deployment Options

### 1. Standalone Script (Current)
```bash
python predict.py --input-file job.json
```

### 2. REST API (Recommended for Production)
Deploy with FastAPI or Flask:
```python
# Example FastAPI endpoint
@app.post("/predict")
def predict(job: JobInput):
    predictor = PlumbingPredictor("models/production/plumbing_model_v1.0.0.joblib")
    return predictor.predict(job.dict())
```

### 3. Embedded in Application
Import `PlumbingPredictor` class directly into your application code.

---

## Performance Benchmarks

**Training Time:** ~2-3 minutes on standard hardware (MacBook)
**Inference Time:** <10ms per prediction
**Model Size:** ~500 KB (compressed with joblib)
**Memory Usage:** ~50 MB when loaded

---

## Support & Contact

For questions about the models:
1. Review the main [model_instructions.md](../model_instructions.md) guide
2. Check the metadata JSON for detailed model configuration
3. Review the training script [model.py](../model.py) for implementation details

---

**Last Updated:** 2025-11-22
**Model Version:** 1.0.0
**Trained By:** Regression Model Pipeline
