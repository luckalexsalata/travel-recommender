import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")

def test_create_recommendation():
    """Test creating a recommendation"""
    data = {
        "text": "I want to visit Rome, I love history and pasta",
        "num_places": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/recommendations",
        json=data
    )
    
    print(f"Create recommendation: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Created recommendation ID: {result['id']}")
        print(f"Places: {[place['name'] for place in result['response_json']]}")
        return result['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_update_recommendation(request_id):
    """Test updating a recommendation"""
    data = {
        "exclude": ["Colosseum"]
    }
    
    response = requests.put(
        f"{BASE_URL}/api/v1/recommendations/{request_id}",
        json=data
    )
    
    print(f"Update recommendation: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Updated places: {[place['name'] for place in result['response_json']]}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Testing Travel Recommender API...")
    print("=" * 50)
    
    # Test health endpoint
    test_health()
    print()
    
    # Test creating recommendation
    request_id = test_create_recommendation()
    print()
    
    # Test updating recommendation
    if request_id:
        test_update_recommendation(request_id) 