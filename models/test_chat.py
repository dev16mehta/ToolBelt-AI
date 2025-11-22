"""
Test script for the new /chat endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_chat_endpoint():
    """Test the /chat endpoint with various inputs"""
    
    print("=" * 80)
    print("Testing /chat Endpoint")
    print("=" * 80)
    
    test_cases = [
        {
            "name": "Job Description - Leak Repair",
            "message": "I have a leaking pipe under my kitchen sink that needs to be fixed"
        },
        {
            "name": "Job Description - Bathroom Installation",
            "message": "Install a luxury bathroom with wall-hung toilet and premium shower cabin"
        },
        {
            "name": "Greeting",
            "message": "Hello, what can you help me with?"
        },
        {
            "name": "General Inquiry",
            "message": "How much does plumbing work typically cost?"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}: {test['name']}")
        print(f"{'=' * 80}")
        print(f"User Message: {test['message']}")
        print()
        
        try:
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": test["message"]},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: {response.status_code}")
                print(f"\nAI Response:")
                print("-" * 80)
                print(data.get('response', 'No response'))
                print("-" * 80)
                
                if data.get('estimate'):
                    print(f"\n💰 Estimate Generated:")
                    print(f"   Cost (GBP): £{data['estimate']['cost_gbp']:.2f}")
                    print(f"   Cost (DZD): {data['estimate']['cost_dzd']:.2f}")
                    print(f"   Time: {data['estimate']['time_days']} days")
                    
                if data.get('features'):
                    print(f"\n🔧 Features Detected:")
                    for key, value in data['features'].items():
                        print(f"   {key}: {value}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Connection Error: Make sure the API is running!")
            print("   Start it with: uvicorn api:app --reload")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'=' * 80}")
    print("Testing Complete!")
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    print("\n🧪 Testing Plumbing Chat API\n")
    print("Make sure the API is running first:")
    print("  cd models")
    print("  uvicorn api:app --reload\n")
    
    input("Press Enter to start tests...")
    test_chat_endpoint()
