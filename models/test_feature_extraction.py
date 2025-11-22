"""
Test script for ChatGPT feature extraction.

This script allows you to test the FeatureExtractor with sample job descriptions
and see the extracted features. It also validates the features can be used with
the PlumbingPredictor model.

Usage:
    python test_feature_extraction.py
"""

import json
import sys
from services.feature_extractor import FeatureExtractor
from predict import PlumbingPredictor


def dzd_to_gbp(dzd_amount, exchange_rate=0.0056):
    """
    Convert Algerian Dinar (DZD) to British Pounds (GBP).

    Parameters:
        dzd_amount (float): Amount in Algerian Dinar
        exchange_rate (float): DZD to GBP exchange rate (default: 0.0056)
                              As of 2024, 1 DZD ≈ 0.0056 GBP

    Returns:
        float: Amount in British Pounds
    """
    return dzd_amount * exchange_rate


def test_extraction(job_description: str):
    """
    Test feature extraction for a single job description.

    Parameters:
        job_description (str): Natural language job description
    """
    print("\n" + "="*80)
    print("JOB DESCRIPTION:")
    print("="*80)
    print(job_description)
    print("\n" + "="*80)
    print("EXTRACTED FEATURES:")
    print("="*80)

    try:
        # Initialize extractor
        extractor = FeatureExtractor()

        # Extract features
        features = extractor.extract_features(job_description)

        # Print features in readable format
        print(json.dumps(features, indent=2))

        print("\n" + "="*80)
        print("PREDICTION:")
        print("="*80)

        # Test with predictor
        model_path = "models/production/plumbing_model_v1.0.0.joblib"
        predictor = PlumbingPredictor(model_path)
        result = predictor.predict(features)
        cost_dzd = result['cost']
        cost_gbp = dzd_to_gbp(cost_dzd)
        time = result['time']

        print(f"Estimated Cost (DZD): {cost_dzd:,.2f} DZD")
        print(f"Estimated Cost (GBP): £{cost_gbp:,.2f}")
        print(f"Estimated Time: {time:.1f} days")

        return features, cost, time

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return None, None, None


def test_multiple_examples():
    """Test with multiple example job descriptions."""

    examples = [
        # Example 1: Luxury bathroom
        "I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink",

        # Example 2: Complete house plumbing
        "Complete plumbing for a 3-bedroom house: 3 bathrooms, kitchen with double sink, big boiler, 8 radiators",

        # Example 3: Budget renovation
        "Budget bathroom renovation: basic fixtures, 1 toilet, 1 shower, 1 sink, small electric water heater",

        # Example 4: Master bathroom
        "Install a master bathroom with bathtub, separate shower cabin, 2 washbasins, and premium fixtures",

        # Example 5: Simple half bath
        "Add a half bath with one toilet and wall-mounted sink"
    ]

    results = []

    for i, example in enumerate(examples, 1):
        print(f"\n\n{'#'*80}")
        print(f"EXAMPLE {i}/{len(examples)}")
        print(f"{'#'*80}")

        features, cost, time = test_extraction(example)

        if features:
            results.append({
                'description': example,
                'features': features,
                'cost': cost,
                'time': time
            })

    # Summary
    print("\n\n" + "="*80)
    print("SUMMARY OF ALL TESTS")
    print("="*80)

    if results:
        for i, result in enumerate(results, 1):
            cost_dzd = result['cost']
            cost_gbp = dzd_to_gbp(cost_dzd)
            print(f"\n{i}. {result['description'][:60]}...")
            print(f"   Cost: {cost_dzd:,.2f} DZD (£{cost_gbp:,.2f}) | Time: {result['time']:.1f} days")
    else:
        print("No successful extractions")

    return results


def test_custom_input():
    """Test with custom user input from command line."""

    print("\n" + "="*80)
    print("CUSTOM JOB DESCRIPTION TEST")
    print("="*80)
    print("\nEnter your plumbing job description (or press Enter to skip):")

    job_description = input("> ").strip()

    if job_description:
        test_extraction(job_description)
    else:
        print("Skipping custom input test")


def main():
    """Main test function."""

    print("\n" + "#"*80)
    print("# ChatGPT Feature Extraction Test Suite")
    print("#"*80)

    # Check if we should run all examples or custom input
    if len(sys.argv) > 1:
        # Custom job description provided as command line argument
        job_description = " ".join(sys.argv[1:])
        test_extraction(job_description)
    else:
        # Run predefined examples
        print("\nThis will test the feature extraction with 5 example job descriptions.")
        print("Each test will show:")
        print("  1. The original job description")
        print("  2. Extracted features (JSON)")
        print("  3. Cost and time predictions")

        input("\nPress Enter to start tests...")

        results = test_multiple_examples()

        # Offer custom input test
        print("\n" + "="*80)
        test_custom_input()

    print("\n" + "#"*80)
    print("# Tests Complete!")
    print("#"*80)
    print("\nTip: You can also test a custom description directly:")
    print('  python test_feature_extraction.py "your job description here"')
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
