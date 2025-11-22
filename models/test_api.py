"""
Simple API Test Client
======================
Test the Plumbing Cost Estimator API with example requests.

Usage:
    1. Start the API: uvicorn api:app --reload
    2. Run this script: python test_api.py
"""

import requests
import json
import time


API_BASE_URL = "http://localhost:8000"


def print_separator(title=""):
    """Print a formatted separator."""
    print("\n" + "=" * 80)
    if title:
        print(f"{title:^80}")
        print("=" * 80)


def test_health_check():
    """Test the health check endpoint."""
    print_separator("HEALTH CHECK")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        response.raise_for_status()
        result = response.json()
        print(json.dumps(result, indent=2))
        return result.get("status") == "healthy"
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_estimate(job_description):
    """Test the estimate endpoint."""
    print_separator("ESTIMATE REQUEST")
    print(f"\nJob Description:\n{job_description}\n")

    try:
        # Send request
        start_time = time.time()
        response = requests.post(
            f"{API_BASE_URL}/estimate",
            json={"job_description": job_description}
        )
        elapsed_time = time.time() - start_time

        response.raise_for_status()
        result = response.json()

        # Print results
        print("-" * 80)
        print("RESPONSE:")
        print("-" * 80)
        print(f"✓ Success: {result['success']}")
        print(f"\n💰 Cost Estimate:")
        print(f"   Algerian Dinar: {result['cost_dzd']:,.2f} DZD")
        print(f"   British Pounds: £{result['cost_gbp']:,.2f}")
        print(f"\n⏱️  Time Estimate: {result['time_days']:.1f} days")
        print(f"\n🔧 Extracted Features:")
        for key, value in result['features'].items():
            print(f"   {key:20s}: {value}")
        print(f"\n⚡ Response time: {elapsed_time:.2f}s")
        print("-" * 80)

        return result

    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP Error: {e}")
        if e.response is not None:
            print(f"Response: {e.response.text}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_root():
    """Test the root endpoint."""
    print_separator("API INFO")
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        result = response.json()
        print(json.dumps(result, indent=2))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Run all tests."""
    print("\n" + "#" * 80)
    print("#" + " " * 78 + "#")
    print("#" + "PLUMBING COST ESTIMATOR API - TEST SUITE".center(78) + "#")
    print("#" + " " * 78 + "#")
    print("#" * 80)

    # Check if API is running
    print("\nChecking if API is running at", API_BASE_URL, "...")
    try:
        response = requests.get(API_BASE_URL, timeout=2)
        response.raise_for_status()
        print("✓ API is running!\n")
    except Exception as e:
        print(f"\n❌ Cannot connect to API at {API_BASE_URL}")
        print("\nPlease start the API first:")
        print("  cd models")
        print("  uvicorn api:app --reload")
        print("\nThen run this test again.\n")
        return

    # Test API info
    test_root()

    # Test health check
    if not test_health_check():
        print("\n⚠️  API is not healthy. Some services may not be working.")
        print("Please check:")
        print("  1. Model file exists at models/production/plumbing_model_v1.0.0.joblib")
        print("  2. OPENAI_API_KEY is set in .env file")
        return

    # Test examples
    examples = [
        "I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink",
        "Complete plumbing for a 3-bedroom house: 3 bathrooms, kitchen with double sink, big boiler, 8 radiators",
        "Budget bathroom renovation: basic fixtures, 1 toilet, 1 shower, 1 sink, small electric water heater",
        "Install a master bathroom with bathtub, separate shower cabin, 2 washbasins, and premium fixtures",
        "Add a half bath with one toilet and wall-mounted sink"
    ]

    print("\n" + "#" * 80)
    print(f"# Running {len(examples)} test cases")
    print("#" * 80)

    results = []
    for i, example in enumerate(examples, 1):
        print(f"\n\n{'#' * 80}")
        print(f"# TEST CASE {i}/{len(examples)}")
        print(f"{'#' * 80}")

        result = test_estimate(example)
        if result:
            results.append(result)

        # Small delay between requests
        if i < len(examples):
            time.sleep(1)

    # Summary
    print_separator("TEST SUMMARY")
    print(f"\nTotal tests: {len(examples)}")
    print(f"Successful: {len(results)}")
    print(f"Failed: {len(examples) - len(results)}")

    if results:
        print("\n" + "-" * 80)
        print("COST RANGE:")
        costs_dzd = [r['cost_dzd'] for r in results]
        costs_gbp = [r['cost_gbp'] for r in results]
        times = [r['time_days'] for r in results]

        print(f"  DZD: {min(costs_dzd):,.2f} - {max(costs_dzd):,.2f}")
        print(f"  GBP: £{min(costs_gbp):,.2f} - £{max(costs_gbp):,.2f}")
        print(f"  Time: {min(times):.1f} - {max(times):.1f} days")

    print("\n" + "#" * 80)
    print("#" + "TESTS COMPLETE!".center(78) + "#")
    print("#" * 80)
    print("\n📚 For more information, see:")
    print("  - API docs: http://localhost:8000/docs")
    print("  - Usage guide: API_USAGE.md")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user\n")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
