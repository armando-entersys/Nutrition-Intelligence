"""
Simple test for API endpoints
"""
import requests
import sys

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8001/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("PASS: Health endpoint working")
                return True
            else:
                print("FAIL: Health endpoint returned wrong data")
                return False
        else:
            print(f"FAIL: Health endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Health endpoint error: {e}")
        return False

def test_foods():
    """Test foods endpoint"""
    try:
        response = requests.get("http://localhost:8001/api/v1/foods/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print("PASS: Foods endpoint working")
                return True
            else:
                print("FAIL: Foods endpoint returned wrong format")
                return False
        else:
            print(f"FAIL: Foods endpoint returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAIL: Foods endpoint error: {e}")
        return False

def main():
    print("Testing Backend APIs...")
    print("-" * 30)

    tests = [test_health(), test_foods()]
    passed = sum(tests)
    total = len(tests)

    print("-" * 30)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("SUCCESS: All tests passed!")
        sys.exit(0)
    else:
        print("ERROR: Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()