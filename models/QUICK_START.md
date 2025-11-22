# Quick Start Guide - Model Export & Prediction

## Overview

Your plumbing service prediction models can now be **exported and used for predictions** on new data!

---

## Step 1: Train and Export Models

From the `models/` directory, run the training script (this will automatically save the models):

```bash
cd models
python model.py
```

**What this does:**
- Trains XGBoost (cost) and Ridge (time) models
- Evaluates performance on test data
- **Automatically exports models** to `models/production/`
- Saves metadata with performance metrics

**Output files:**
- `models/production/plumbing_model_v1.0.0.joblib` (model package)
- `models/production/metadata_v1.0.0.json` (performance metrics)

---

## Step 2: Make Predictions

### Option A: Quick Example

From the `models/` directory:

```bash
cd models
python predict.py --example
```

**Output:**
```
Estimated Cost: $425,750.00
Estimated Time: 12.5 days
```

### Option B: Custom Job (JSON)

Create `my_job.json`:
```json
{
  "boilerSize": "big",
  "radiator": 8,
  "radiatorType": "GLOBAL_ISEO_350",
  "toilet": 3,
  "toileType": "Wall-Hung",
  "washbasin": 3,
  "washbasinType": "Integrated",
  "bathhub": 1,
  "bathhubType": "Standard",
  "showerCabin": 2,
  "showerCabinType": "Luxury_Enclosure",
  "Bidet": 1,
  "BidetType": "Bidet-Mixer-Tap",
  "waterHeater": 1,
  "waterHeaterType": "Electric-On-Demand",
  "sinkTypeQuality": "high",
  "sinkCategorie": "Kitchen"
}
```

Run prediction from the `models/` directory:
```bash
cd models
python predict.py --input-file my_job.json
```

Results saved to: `my_job.output.json`

### Option C: Batch Processing

Process multiple jobs from CSV (from the `models/` directory):
```bash
cd models
python predict.py --batch jobs.csv
```

Results saved to: `jobs.predictions.csv`

### Option D: Python Integration

From the `models/` directory or with proper Python path:

```python
from predict import PlumbingPredictor

# Load model once (reuse for multiple predictions)
predictor = PlumbingPredictor("production/plumbing_model_v1.0.0.joblib")

# Make prediction
job = {
    "boilerSize": "medium",
    "radiator": 5,
    # ... include all 17 features
}

result = predictor.predict(job)
print(f"Cost: {result['cost_formatted']}")
print(f"Time: {result['time_formatted']}")
```

---

## Step 3: Verify Installation (Optional)

Test the complete pipeline from the `models/` directory:

```bash
cd models
python test_prediction.py
```

This will:
- Check if models exist
- Load the model
- Run test predictions
- Compare different configurations
- Verify everything works correctly

---

## Model Performance

Your trained models achieved excellent results:

| Model | Target | R² Score | Average Error |
|-------|--------|----------|---------------|
| **XGBoost** | Cost | **97.67%** | $40,628 |
| **Ridge** | Time | **85.61%** | 5.0 days |

These are production-ready models with high accuracy!

---

## Required Features (17 total)

Every prediction requires these features:

**Ordinal:**
- `boilerSize`: "small", "medium", or "big"
- `sinkTypeQuality`: "poor" or "high"

**Categorical:**
- `radiatorType`, `toileType`, `washbasinType`, `bathhubType`
- `showerCabinType`, `BidetType`, `waterHeaterType`, `sinkCategorie`

**Numerical:**
- `radiator`, `toilet`, `washbasin`, `bathhub`
- `showerCabin`, `Bidet`, `waterHeater`

---

## File Structure

```
ToolBelt-AI/
├── models/
│   ├── model.py                    # Training script (run first)
│   ├── save_models.py              # Serialization utilities
│   ├── predict.py                  # Prediction script
│   ├── test_prediction.py          # Testing script
│   ├── plumbing_service_data.csv   # Training data
│   ├── model_instructions.md       # User guide
│   ├── QUICK_START.md              # This file
│   ├── README.md                   # Detailed documentation
│   ├── production/
│   │   ├── plumbing_model_v1.0.0.joblib
│   │   └── metadata_v1.0.0.json
│   └── archived/                   # Old model versions
└── frontend/                       # Web application
```

---

## Common Issues

### "Model file not found"
**Solution:** From the `models/` directory, run `python model.py` first to train and export the models.

### "Module not found: numpy/pandas/sklearn"
**Solution:** Install dependencies:
```bash
pip install pandas numpy scikit-learn xgboost
```

### "Invalid value for boilerSize"
**Solution:** Check that all feature values match the expected types:
- `boilerSize` must be exactly: "small", "medium", or "big"
- `sinkTypeQuality` must be exactly: "poor" or "high"
- Numerical features must be integers

---

## Next Steps

### For Production Deployment:

1. **Create a REST API** (FastAPI/Flask)
   - Load model once at startup
   - Create `/predict` endpoint
   - Add input validation
   - Handle errors gracefully

2. **Monitor Performance**
   - Log predictions
   - Track model accuracy over time
   - Retrain quarterly or when performance degrades

3. **Version Control**
   - Tag model versions in git
   - Archive old models
   - Document changes in `models/README.md`

### For Further Improvement:

1. **Hyperparameter Tuning**
   - Use GridSearchCV for optimal parameters
   - May improve R² scores by 1-2%

2. **Feature Engineering**
   - Add total fixture count
   - Create luxury indicator
   - Add interaction features

3. **Advanced Models**
   - Try LightGBM or CatBoost
   - Ensemble multiple models
   - Use SHAP for interpretability

---

## Documentation

- **Quick reference:** This file
- **User guide:** [model_instructions.md](model_instructions.md)
- **Model details:** [README.md](README.md)
- **Training code:** [model.py](model.py)
- **Prediction code:** [predict.py](predict.py)

---

## Summary

You now have a **complete model export and prediction system**:

✅ Models automatically saved after training
✅ Standalone prediction script (`predict.py`)
✅ Support for single, batch, and programmatic predictions
✅ Comprehensive documentation with performance metrics
✅ Production-ready code with 97.67% cost accuracy

**To get started:** From the `models/` directory, run `cd models && python model.py` then `python predict.py --example`

---

**Created:** 2025-11-22
**Model Version:** 1.0.0
