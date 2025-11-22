"""
Test Script for Model Prediction Pipeline
==========================================
This script verifies the prediction pipeline works correctly.

NOTE: Run this AFTER training the model with: python model.py
"""

import sys
from pathlib import Path

# Check if model exists
model_path = Path("models/production/plumbing_model_v1.0.0.joblib")
metadata_path = Path("models/production/metadata_v1.0.0.json")

print("=" * 80)
print("TESTING MODEL PREDICTION PIPELINE")
print("=" * 80)

if not model_path.exists():
    print("\n❌ ERROR: Model file not found!")
    print(f"   Expected: {model_path.absolute()}")
    print("\n   Please run the training script first:")
    print("   $ python model.py")
    print("\n   This will train the models and save them to models/production/")
    sys.exit(1)

if not metadata_path.exists():
    print("\n⚠️  WARNING: Metadata file not found!")
    print(f"   Expected: {metadata_path.absolute()}")
    print("   Continuing with model testing...")

print(f"\n✓ Found model file: {model_path}")
print(f"✓ Model size: {model_path.stat().st_size / 1024:.2f} KB")

if metadata_path.exists():
    print(f"✓ Found metadata: {metadata_path}")
    print(f"✓ Metadata size: {metadata_path.stat().st_size / 1024:.2f} KB")

# Import the predictor
try:
    from predict import PlumbingPredictor
    print("\n✓ Successfully imported PlumbingPredictor")
except ImportError as e:
    print(f"\n❌ ERROR: Failed to import PlumbingPredictor: {e}")
    sys.exit(1)

# Load the model
print("\n" + "-" * 80)
print("LOADING MODEL...")
print("-" * 80)

try:
    predictor = PlumbingPredictor(str(model_path))
    print("✓ Model loaded successfully!")
except Exception as e:
    print(f"❌ ERROR: Failed to load model: {e}")
    sys.exit(1)

# Test prediction with example data
print("\n" + "-" * 80)
print("TESTING PREDICTION...")
print("-" * 80)

test_input = {
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
    "sinkCategorie": "Kitchen",
}

print("\nInput features:")
for key, value in test_input.items():
    print(f"  {key:20s}: {value}")

try:
    result = predictor.predict(test_input)
    print("\n✓ Prediction successful!")
    print("\n" + "=" * 80)
    print("PREDICTION RESULTS")
    print("=" * 80)
    print(f"\n  Estimated Cost: {result['cost_formatted']}")
    print(f"  Estimated Time: {result['time_formatted']}")
    print("\n  (Raw values)")
    print(f"  Cost: ${result['cost']:.2f}")
    print(f"  Time: {result['time']:.2f} days")
    print("\n" + "=" * 80)
except Exception as e:
    print(f"\n❌ ERROR: Prediction failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test with a different configuration
print("\n" + "-" * 80)
print("TESTING WITH DIFFERENT CONFIGURATION (Large Project)...")
print("-" * 80)

large_project = {
    "boilerSize": "big",
    "radiator": 10,
    "radiatorType": "GLOBAL_ISEO_350",
    "toilet": 4,
    "toileType": "Wall-Hung",
    "washbasin": 4,
    "washbasinType": "Integrated",
    "bathhub": 2,
    "bathhubType": "Standard",
    "showerCabin": 2,
    "showerCabinType": "Luxury_Enclosure",
    "Bidet": 2,
    "BidetType": "Bidet-Mixer-Tap",
    "waterHeater": 2,
    "waterHeaterType": "Electric-On-Demand",
    "sinkTypeQuality": "high",
    "sinkCategorie": "Kitchen",
}

try:
    result2 = predictor.predict(large_project)
    print(f"\n  Large Project Cost: {result2['cost_formatted']}")
    print(f"  Large Project Time: {result2['time_formatted']}")
except Exception as e:
    print(f"\n❌ ERROR: Second prediction failed: {e}")
    sys.exit(1)

# Compare results
print("\n" + "-" * 80)
print("COMPARISON")
print("-" * 80)
print(f"\n  Standard Project: {result['cost_formatted']} / {result['time_formatted']}")
print(f"  Large Project:    {result2['cost_formatted']} / {result2['time_formatted']}")
print(f"\n  Cost Difference:  ${result2['cost'] - result['cost']:,.2f}")
print(f"  Time Difference:  {result2['time'] - result['time']:.1f} days")

# Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print("\n✅ All tests passed!")
print("\n   Model loading:     SUCCESS")
print("   Prediction:        SUCCESS")
print("   Multiple inputs:   SUCCESS")
print("   Result formatting: SUCCESS")

print("\n" + "-" * 80)
print("The prediction pipeline is working correctly!")
print("-" * 80)
print("\nYou can now use the model for predictions:")
print("  • python predict.py --example")
print("  • python predict.py --input-file my_job.json")
print("  • python predict.py --batch jobs.csv")
print("\n" + "=" * 80 + "\n")
