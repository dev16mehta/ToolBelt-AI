"""
Model Serialization Script
===========================
Saves trained plumbing service prediction models and metadata for deployment.
"""

import json
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


def save_plumbing_models(
    cost_model,
    time_model,
    scaler_time,
    X_encoded,
    ordinal_mappings,
    remaining_categorical,
    categorical_cols,
    numerical_cols,
    cost_metrics,
    time_metrics,
    cost_cv_scores,
    time_cv_scores,
    version="1.0.0",
    output_dir="models/production",
):
    """
    Save trained models and all preprocessing components needed for predictions.

    Parameters:
    -----------
    cost_model : XGBoost model
        Trained model for cost prediction
    time_model : Ridge model
        Trained model for time prediction
    scaler_time : StandardScaler
        Fitted scaler for time prediction features
    X_encoded : DataFrame
        Encoded features (to extract column names)
    ordinal_mappings : dict
        Mappings for ordinal encoding
    remaining_categorical : list
        List of categorical columns that were one-hot encoded
    categorical_cols : list
        All categorical column names
    numerical_cols : list
        All numerical column names
    cost_metrics : dict
        Performance metrics for cost model (R2, RMSE, MAE)
    time_metrics : dict
        Performance metrics for time model (R2, RMSE, MAE)
    cost_cv_scores : array
        Cross-validation scores for cost model
    time_cv_scores : array
        Cross-validation scores for time model
    version : str
        Model version (semantic versioning)
    output_dir : str
        Directory to save models
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Create version-specific filenames
    model_file = output_path / f"plumbing_model_v{version}.joblib"
    metadata_file = output_path / f"metadata_v{version}.json"

    print("\n" + "=" * 80)
    print("SAVING MODELS FOR DEPLOYMENT")
    print("=" * 80)

    # Package all components together
    model_package = {
        "cost_model": cost_model,
        "time_model": time_model,
        "scaler_time": scaler_time,
        "feature_names": list(X_encoded.columns),
        "ordinal_mappings": ordinal_mappings,
        "one_hot_columns": remaining_categorical,
        "categorical_columns": categorical_cols,
        "numerical_columns": numerical_cols,
    }

    # Save model package
    print(f"\nSaving model package to: {model_file}")
    joblib.dump(model_package, model_file, compress=3)
    print(f"✓ Model package saved ({model_file.stat().st_size / 1024:.2f} KB)")

    # Create metadata
    metadata = {
        "model_info": {
            "version": version,
            "created_date": datetime.now().isoformat(),
            "model_type": "plumbing_cost_time_predictor",
            "description": "Regression models for predicting plumbing service cost and time",
        },
        "preprocessing": {
            "ordinal_mappings": ordinal_mappings,
            "categorical_columns": categorical_cols,
            "numerical_columns": numerical_cols,
            "one_hot_encoded_columns": remaining_categorical,
            "feature_names": list(X_encoded.columns),
            "total_features_after_encoding": len(X_encoded.columns),
        },
        "transformations": {
            "cost_target": "log1p (np.log1p)",
            "time_target": "none",
            "feature_scaling": "StandardScaler (for Ridge time model only)",
        },
        "models": {
            "cost_predictor": {
                "algorithm": "XGBoost",
                "model_class": str(type(cost_model).__name__),
                "hyperparameters": {
                    "n_estimators": int(cost_model.n_estimators),
                    "max_depth": int(cost_model.max_depth),
                    "learning_rate": float(cost_model.learning_rate),
                },
                "performance": {
                    "r2_score": float(cost_metrics["R²"]),
                    "rmse": float(cost_metrics["RMSE"]),
                    "mae": float(cost_metrics["MAE"]),
                    "cv_mean": float(cost_cv_scores.mean()),
                    "cv_std": float(cost_cv_scores.std()),
                },
            },
            "time_predictor": {
                "algorithm": "Ridge",
                "model_class": str(type(time_model).__name__),
                "uses_scaler": True,
                "hyperparameters": {
                    "alpha": float(time_model.alpha),
                },
                "performance": {
                    "r2_score": float(time_metrics["R²"]),
                    "rmse": float(time_metrics["RMSE"]),
                    "mae": float(time_metrics["MAE"]),
                    "cv_mean": float(time_cv_scores.mean()),
                    "cv_std": float(time_cv_scores.std()),
                },
            },
        },
        "training_config": {
            "random_state": 42,
            "test_size": 0.2,
            "cv_folds": 5,
        },
    }

    # Save metadata
    print(f"Saving metadata to: {metadata_file}")
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✓ Metadata saved ({metadata_file.stat().st_size / 1024:.2f} KB)")

    # Print summary
    print("\n" + "-" * 80)
    print("SAVED COMPONENTS:")
    print("-" * 80)
    print(f"✓ Cost Model (XGBoost):  R² = {cost_metrics['R²']:.4f}")
    print(f"✓ Time Model (Ridge):    R² = {time_metrics['R²']:.4f}")
    print(f"✓ Time Scaler (StandardScaler)")
    print(f"✓ Feature Names:         {len(X_encoded.columns)} features")
    print(f"✓ Encoding Metadata:     Ordinal + One-Hot mappings")
    print("\n" + "-" * 80)
    print(f"Models ready for deployment at: {output_path.absolute()}")
    print("=" * 80 + "\n")

    return {
        "model_file": str(model_file.absolute()),
        "metadata_file": str(metadata_file.absolute()),
        "version": version,
    }


def load_plumbing_models(model_file):
    """
    Load saved model package.

    Parameters:
    -----------
    model_file : str
        Path to the saved model file

    Returns:
    --------
    dict : Dictionary containing all model components
    """
    print(f"Loading model package from: {model_file}")
    model_package = joblib.load(model_file)
    print("✓ Model package loaded successfully")
    return model_package


if __name__ == "__main__":
    print("This script provides model saving/loading utilities.")
    print("Import and use save_plumbing_models() from your training script.")
