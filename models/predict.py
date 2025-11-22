"""
Plumbing Service Prediction Script
===================================
Standalone script to make cost and time predictions using saved models.
"""

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from save_models import load_plumbing_models


class PlumbingPredictor:
    """
    Prediction class for plumbing service cost and time estimation.
    """

    def __init__(self, model_path):
        """
        Initialize predictor by loading saved model package.

        Parameters:
        -----------
        model_path : str
            Path to the saved model file (.joblib)
        """
        self.model_package = load_plumbing_models(model_path)
        self.cost_model = self.model_package["cost_model"]
        self.time_model = self.model_package["time_model"]
        self.scaler_time = self.model_package["scaler_time"]
        self.feature_names = self.model_package["feature_names"]
        self.ordinal_mappings = self.model_package["ordinal_mappings"]
        self.one_hot_columns = self.model_package["one_hot_columns"]
        self.categorical_columns = self.model_package["categorical_columns"]
        self.numerical_columns = self.model_package["numerical_columns"]

        print(f"✓ Loaded model with {len(self.feature_names)} features")

    def preprocess_input(self, input_data):
        """
        Preprocess input data to match the training format.

        Parameters:
        -----------
        input_data : dict
            Dictionary containing feature values

        Returns:
        --------
        DataFrame : Preprocessed features ready for prediction
        """
        # Create DataFrame from input
        df = pd.DataFrame([input_data])

        # Apply ordinal encoding
        for col, mapping in self.ordinal_mappings.items():
            if col in df.columns:
                df[col] = df[col].map(mapping)
                if df[col].isnull().any():
                    valid_values = list(mapping.keys())
                    raise ValueError(
                        f"Invalid value for {col}. Must be one of: {valid_values}"
                    )

        # One-hot encode remaining categorical features
        df_encoded = pd.get_dummies(df, columns=self.one_hot_columns, drop_first=True)

        # Ensure all expected features are present (add missing columns with 0)
        for feature in self.feature_names:
            if feature not in df_encoded.columns:
                df_encoded[feature] = 0

        # Select features in the correct order
        df_encoded = df_encoded[self.feature_names]

        return df_encoded

    def predict(self, input_data):
        """
        Make cost and time predictions for a plumbing job.

        Parameters:
        -----------
        input_data : dict
            Dictionary containing feature values (e.g., boilerSize, radiator count, etc.)

        Returns:
        --------
        dict : Predictions containing cost (in dollars) and time (in days)
        """
        # Preprocess input
        X = self.preprocess_input(input_data)

        # Predict cost (remember to inverse log transformation)
        cost_pred_log = self.cost_model.predict(X)[0]
        cost_pred = np.expm1(cost_pred_log)  # Inverse of log1p

        # Predict time (requires scaling for Ridge model)
        X_scaled = self.scaler_time.transform(X)
        time_pred = self.time_model.predict(X_scaled)[0]

        return {
            "cost": float(cost_pred),
            "time": float(time_pred),
            "cost_formatted": f"${cost_pred:,.2f}",
            "time_formatted": f"{time_pred:.1f} days",
        }


def create_example_input():
    """Create an example input for testing."""
    return {
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


def main():
    parser = argparse.ArgumentParser(
        description="Predict plumbing service cost and time"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="models/production/plumbing_model_v1.0.0.joblib",
        help="Path to saved model file",
    )
    parser.add_argument(
        "--input-file",
        type=str,
        help="Path to JSON file with input features",
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run prediction on example input",
    )
    parser.add_argument(
        "--batch",
        type=str,
        help="Path to CSV file with multiple inputs for batch prediction",
    )

    args = parser.parse_args()

    # Check if model file exists
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}")
        print("Please train the model first by running: python model.py")
        sys.exit(1)

    # Initialize predictor
    print("=" * 80)
    print("PLUMBING SERVICE PREDICTOR")
    print("=" * 80)
    predictor = PlumbingPredictor(args.model)

    # Handle different input modes
    if args.example:
        print("\n--- EXAMPLE PREDICTION ---\n")
        input_data = create_example_input()
        print("Input features:")
        for key, value in input_data.items():
            print(f"  {key:20s}: {value}")

        result = predictor.predict(input_data)
        print("\n" + "-" * 80)
        print("PREDICTION RESULTS:")
        print("-" * 80)
        print(f"Estimated Cost: {result['cost_formatted']}")
        print(f"Estimated Time: {result['time_formatted']}")
        print("-" * 80 + "\n")

    elif args.input_file:
        print(f"\n--- PREDICTING FROM FILE: {args.input_file} ---\n")
        with open(args.input_file, "r") as f:
            input_data = json.load(f)

        result = predictor.predict(input_data)
        print("\n" + "-" * 80)
        print("PREDICTION RESULTS:")
        print("-" * 80)
        print(f"Estimated Cost: {result['cost_formatted']}")
        print(f"Estimated Time: {result['time_formatted']}")
        print("-" * 80)

        # Save output
        output_file = Path(args.input_file).with_suffix(".output.json")
        with open(output_file, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Results saved to: {output_file}\n")

    elif args.batch:
        print(f"\n--- BATCH PREDICTION FROM: {args.batch} ---\n")
        df = pd.read_csv(args.batch)
        print(f"Processing {len(df)} records...")

        results = []
        for idx, row in df.iterrows():
            input_data = row.to_dict()
            try:
                result = predictor.predict(input_data)
                results.append(
                    {
                        "index": idx,
                        "cost": result["cost"],
                        "time": result["time"],
                        "status": "success",
                    }
                )
            except Exception as e:
                results.append({"index": idx, "status": "error", "error": str(e)})

        # Save batch results
        output_file = Path(args.batch).with_suffix(".predictions.csv")
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_file, index=False)
        print(f"✓ Batch predictions saved to: {output_file}\n")

    else:
        print("\nNo input provided. Use one of the following options:")
        print("  --example                Run prediction on example input")
        print("  --input-file <file>      Predict from JSON file")
        print("  --batch <file>           Batch prediction from CSV file")
        print("\nFor more help: python predict.py --help\n")


if __name__ == "__main__":
    main()
