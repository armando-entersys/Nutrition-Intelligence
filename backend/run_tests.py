"""
Simple test runner for backend health checks
"""
import asyncio
import httpx


async def test_backend_health():
    """Test if backend health endpoint is working"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8001/health")

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ Backend health endpoint test PASSED")
                    return True
                else:
                    print("❌ Backend health endpoint returned unexpected data")
                    return False
            else:
                print(f"❌ Backend health endpoint returned status {response.status_code}")
                return False

    except Exception as e:
        print(f"❌ Backend health endpoint test FAILED: {e}")
        return False


async def test_foods_api():
    """Test if foods API endpoint is working"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:8001/api/v1/foods/")

            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    print("✅ Foods API endpoint test PASSED")
                    return True
                else:
                    print("❌ Foods API endpoint returned unexpected data format")
                    return False
            else:
                print(f"❌ Foods API endpoint returned status {response.status_code}")
                return False

    except Exception as e:
        print(f"❌ Foods API endpoint test FAILED: {e}")
        return False


async def main():
    """Run all tests"""
    print("Running Backend API Tests...")
    print("=" * 50)

    tests = [
        test_backend_health(),
        test_foods_api(),
    ]

    results = await asyncio.gather(*tests, return_exceptions=True)

    passed = sum(1 for result in results if result is True)
    total = len(results)

    # Show any exceptions that occurred
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Test {i+1} failed with exception: {result}")

    print("=" * 50)
    print(f"Tests completed: {passed}/{total} passed")

    if passed == total:
        print("All tests passed!")
        exit(0)
    else:
        print("Some tests failed!")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())