import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_docs():
    """Test if docs are available"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ Docs available: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ Docs failed: {e}")
        return False

def test_openapi():
    """Test OpenAPI schema"""
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        print(f"✅ OpenAPI schema: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ OpenAPI schema failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Travel Recommender API...")
    print("=" * 50)
    
    # Test basic endpoints
    test_health()
    print()
    
    test_root()
    print()
    
    test_docs()
    print()
    
    test_openapi()
    print()
    
    print("🎯 To test with OpenAI:")
    print("1. Edit app/config.py and add your OpenAI API key")
    print("2. Run: python3 run.py")
    print("3. Visit: http://localhost:8000/docs")
    print("4. Try the POST /api/v1/recommendations endpoint") 