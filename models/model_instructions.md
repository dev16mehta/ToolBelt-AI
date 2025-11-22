# Plumbing Service Prediction Model - User Guide

## What This Model Does

This model helps you predict **two important things** about plumbing jobs:

1. **Cost** - How much a plumbing service will cost (in dollars)
2. **Time** - How long the job will take to complete (in days)

The model analyzes information about the plumbing equipment needed (boilers, radiators, toilets, sinks, etc.) and predicts both the cost and time required.

---

## How to Use the Model

### Step 1: Install Required Software

Before running the model, you need to have Python installed on your computer along with some data science libraries.

**Install the required libraries by running:**

```bash
pip install pandas numpy scikit-learn xgboost
```

### Step 2: Prepare Your Data

Make sure you have the plumbing service data file (`plumbing_service_data.csv`) in the same folder as the model script.

The data should already be loaded into a variable called `df` as mentioned in the model file.

### Step 3: Run the Model

Simply run the Python script from your terminal or command prompt:

```bash
python model.py
```

That's it! The model will automatically:
- Load your data
- Process and prepare it
- Train multiple prediction models
- Show you the results

---

## What You'll See When It Runs

The model goes through **7 main steps** and shows progress along the way:

### [1/7] Loading data
Shows how many rows and columns are in your dataset.

### [2/7] Preprocessing data
Converts text categories (like "small", "medium", "big") into numbers the model can understand.

### [3/7] Splitting data
Divides your data into training (80%) and testing (20%) sets.

### [4/7] Training models for COST prediction
Trains three different prediction models and shows their accuracy scores.

### [5/7] Training models for TIME prediction
Trains three different prediction models for time estimation.

### [6/7] Evaluating models
Tests each model and shows how well they perform using:
- **R² Score**: How well the model fits (closer to 1.0 is better)
- **RMSE**: Average prediction error (lower is better)
- **MAE**: Another measure of error (lower is better)

### [7/7] Analyzing feature importance
Shows which factors (boiler size, number of radiators, etc.) have the biggest impact on cost and time.

---

## Understanding the Results

### Model Performance Metrics

**R² Score (R-squared)**
- Ranges from 0 to 1
- Higher is better (1.0 = perfect predictions)
- Example: 0.85 means the model explains 85% of the variation

**RMSE (Root Mean Squared Error)**
- Shows average prediction error
- For cost: measured in dollars
- For time: measured in days
- Lower numbers = more accurate predictions

**MAE (Mean Absolute Error)**
- Similar to RMSE but easier to interpret
- Average difference between predicted and actual values
- Lower is better

### Which Model is Best?

The script automatically identifies the best-performing model for each prediction target. Typically:

- **XGBoost** performs best (most accurate)
- **Random Forest** is a close second
- **Ridge Regression** serves as a simpler baseline

### Feature Importance

The model shows the **Top 10 features** that most influence predictions. For example:

- **For Cost**: Boiler size, radiator type, and number of fixtures
- **For Time**: Project complexity (total number of items to install)

---

## Three Models Explained

### 1. Random Forest
- Uses many decision trees working together
- Very reliable and handles different types of data well
- Good at finding patterns in complex data

### 2. XGBoost
- Advanced machine learning technique
- Usually the most accurate
- Great at learning from data and making precise predictions

### 3. Ridge Regression
- Traditional statistical approach
- Simpler and faster than the others
- Good baseline for comparison

---

## What Happens Behind the Scenes

### Data Preparation
The model automatically:
- Converts categories like "small/medium/big" into numbers (0/1/2)
- Handles different types of equipment (toilets, sinks, radiators, etc.)
- Transforms the cost values using logarithms (makes predictions more stable)
- Standardizes all numbers to the same scale

### Training Process
- Uses 80% of data to learn patterns
- Tests on the remaining 20% to verify accuracy
- Performs 5-fold cross-validation for reliability
- Compares three different approaches to find the best

### Validation
- Ensures models work on data they haven't seen before
- Prevents overfitting (memorizing instead of learning)
- Provides confidence that predictions will work on new jobs

---

## Tips for Best Results

### When to Re-run the Model
- When you get new plumbing job data
- If costs or equipment types change significantly
- Periodically (every few months) to keep predictions current

### Interpreting Predictions
- Check the R² score - above 0.80 is generally good
- Look at RMSE/MAE in context of your typical job costs
- Review feature importance to understand what drives costs

### Common Questions

**Q: Why three different models?**
A: Different models have different strengths. Comparing them helps us find the most accurate one and builds confidence in the results.

**Q: What if my predictions seem off?**
A: Check that your input data matches the format of the training data. The model works best with jobs similar to those in the training set.

**Q: Can I use this for jobs not in the training data?**
A: Yes, but predictions are most reliable for jobs similar to what the model learned from. Very unusual jobs may have less accurate predictions.

**Q: How accurate are the predictions?**
A: Check the R² score and RMSE values in the output. These tell you exactly how accurate the model is on your specific dataset.

---

## Summary Output

At the end, you'll see a comprehensive summary including:

- **Best model for cost prediction** with performance metrics
- **Best model for time prediction** with performance metrics
- **Key findings** about what influences cost and time
- **Recommendations** for improving the model further

---

## Need Help?

If you encounter any issues:

1. Make sure all required libraries are installed
2. Check that your data file path is correct
3. Verify your CSV file has the expected columns
4. Ensure Python 3.7 or later is installed

For further improvements or questions, refer to the "IMPROVEMENT RECOMMENDATIONS" section in the model output.

---

## Using Saved Models for Predictions

After training, the models are **automatically saved** for deployment and can be used to make predictions on new plumbing jobs.

### Saved Model Files

The trained models are saved in the `models/production/` directory:

- **`plumbing_model_v1.0.0.joblib`** - Complete model package (all components in one file)
- **`metadata_v1.0.0.json`** - Model performance metrics and configuration

### Making Predictions

#### Option 1: Quick Example Prediction

Run a prediction on example data:

```bash
python predict.py --example
```

This will show you:
- Example input features
- Predicted cost (in dollars)
- Predicted time (in days)

#### Option 2: Predict from a JSON File

Create a JSON file with your job specifications (e.g., `my_job.json`):

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

Then run:

```bash
python predict.py --input-file my_job.json
```

The results will be displayed on screen and saved to `my_job.output.json`.

#### Option 3: Batch Predictions

If you have multiple jobs in a CSV file:

```bash
python predict.py --batch jobs.csv
```

Results will be saved to `jobs.predictions.csv` with cost and time for each job.

#### Option 4: Use in Python Code

```python
from predict import PlumbingPredictor

# Load the trained model
predictor = PlumbingPredictor("models/production/plumbing_model_v1.0.0.joblib")

# Define your job specifications
job = {
    "boilerSize": "big",
    "radiator": 8,
    "radiatorType": "GLOBAL_ISEO_350",
    # ... include all 17 features
}

# Get prediction
result = predictor.predict(job)

print(f"Estimated Cost: {result['cost_formatted']}")
print(f"Estimated Time: {result['time_formatted']}")
```

### Model Performance Summary

Based on the actual test results:

**Cost Prediction (XGBoost Model):**
- Accuracy (R²): **97.67%** - Extremely accurate!
- Average error: **$40,628** (on jobs ranging from $21K to $2.2M)
- Most accurate model among the three tested

**Time Prediction (Ridge Regression Model):**
- Accuracy (R²): **85.61%** - Very good!
- Average error: **5 days** (on jobs ranging from 2 to 91 days)
- Performed best for time estimation

These results mean the model is highly reliable for estimating both cost and duration of plumbing projects.

### What Features Matter Most?

**For Cost Prediction:**
1. Type of radiator (premium models cost significantly more)
2. Number of radiators
3. Number of shower cabins
4. Bathtub count
5. Water heater count

**For Time Prediction:**
1. Number of radiators (biggest factor)
2. Number of shower cabins
3. Bathtub count
4. Water heater count
5. Toilet count

The more fixtures, especially radiators and luxury items, the higher the cost and longer the timeline.

### Detailed Documentation

For comprehensive model documentation including:
- Complete performance metrics
- Feature importance rankings
- API integration examples
- Model architecture details

See: **[models/README.md](models/README.md)**

---

**Last Updated**: 2025-11-22
**Model Version**: 1.0.0
**Author**: Regression Model for Plumbing Services
