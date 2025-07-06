import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_chat_recommendations():
    """Test chat-like recommendations according to TЗ"""
    print("\n=== Testing Chat-like Recommendations ===")
    
    # Test 1: Initial request
    print("\n1. Initial request: 'Хочу в Рим, люблю історію та макарони'")
    data1 = {
        "text": "Хочу в Рим, люблю історію та макарони",
        "num_places": 3
    }
    
    response1 = requests.post(
        f"{BASE_URL}/api/v1/recommendations/",
        json=data1
    )
    
    print(f"Status: {response1.status_code}")
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"ID: {result1['id']}")
        print(f"Places: {[place['name'] for place in result1['response_json']]}")
        print(f"Exclusions: {result1['exclude']}")
        request_id1 = result1['id']
    else:
        print(f"Error: {response1.text}")
        return False
    
    time.sleep(1)  # Small delay between requests
    
    # Test 2: Refinement with exclusion
    print("\n2. Refinement: 'не хочу в Колізей'")
    data2 = {
        "text": "не хочу в Колізей",
        "num_places": 3
    }
    
    response2 = requests.post(
        f"{BASE_URL}/api/v1/recommendations/",
        json=data2
    )
    
    print(f"Status: {response2.status_code}")
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"ID: {result2['id']}")
        print(f"Places: {[place['name'] for place in result2['response_json']]}")
        print(f"Exclusions: {result2['exclude']}")
        request_id2 = result2['id']
    else:
        print(f"Error: {response2.text}")
        return False
    
    time.sleep(1)
    
    # Test 3: Additional refinement
    print("\n3. Additional refinement: 'і ще не хочу в Ватикан'")
    data3 = {
        "text": "і ще не хочу в Ватикан",
        "num_places": 2
    }
    
    response3 = requests.post(
        f"{BASE_URL}/api/v1/recommendations/",
        json=data3
    )
    
    print(f"Status: {response3.status_code}")
    if response3.status_code == 200:
        result3 = response3.json()
        print(f"ID: {result3['id']}")
        print(f"Places: {[place['name'] for place in result3['response_json']]}")
        print(f"Exclusions: {result3['exclude']}")
        request_id3 = result3['id']
    else:
        print(f"Error: {response3.text}")
        return False
    
    return True

def test_history():
    """Test getting history"""
    print("\n=== Testing History ===")
    
    response = requests.get(f"{BASE_URL}/api/v1/recommendations/history?limit=5")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        history = response.json()
        print(f"Found {len(history)} records in history:")
        for i, record in enumerate(history, 1):
            places = [place['name'] for place in record['response_json']]
            print(f"  {i}. ID: {record['id']}, Text: '{record['text']}', Places: {places}, Exclusions: {record['exclude']}")
    else:
        print(f"Error: {response.text}")
        return False
    
    return True

def test_search():
    """Test search functionality"""
    print("\n=== Testing Search ===")
    
    response = requests.get(f"{BASE_URL}/api/v1/recommendations/search/?q=Рим&limit=5")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        results = response.json()
        print(f"Found {len(results)} results for 'Рим':")
        for i, result in enumerate(results, 1):
            places = [place['name'] for place in result['response_json']]
            print(f"  {i}. ID: {result['id']}, Text: '{result['text']}', Places: {places}")
    else:
        print(f"Error: {response.text}")
        return False
    
    return True

def test_statistics():
    """Test statistics endpoint"""
    print("\n=== Testing Statistics ===")
    
    response = requests.get(f"{BASE_URL}/api/v1/recommendations/statistics/")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        stats = response.json()
        print(f"Statistics: {stats}")
    else:
        print(f"Error: {response.text}")
        return False
    
    return True

def test_get_specific_recommendation():
    """Test getting specific recommendation by ID"""
    print("\n=== Testing Get Specific Recommendation ===")
    
    # First get history to find an ID
    response = requests.get(f"{BASE_URL}/api/v1/recommendations/history?limit=1")
    if response.status_code == 200:
        history = response.json()
        if history:
            request_id = history[0]['id']
            
            response = requests.get(f"{BASE_URL}/api/v1/recommendations/{request_id}")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                places = [place['name'] for place in result['response_json']]
                print(f"ID: {result['id']}, Text: '{result['text']}', Places: {places}, Exclusions: {result['exclude']}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
        else:
            print("No records in history to test")
            return False
    else:
        print(f"Error getting history: {response.text}")
        return False

if __name__ == "__main__":
    print("Testing Travel Recommender API according to TЗ...")
    print("=" * 60)
    
    # Test all endpoints
    tests = [
        ("Health Check", test_health),
        ("Chat Recommendations", test_chat_recommendations),
        ("History", test_history),
        ("Search", test_search),
        ("Statistics", test_statistics),
        ("Get Specific", test_get_specific_recommendation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*20} {test_name} {'='*20}")
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY:")
    print("=" * 60)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! API is working correctly according to TЗ.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.") 