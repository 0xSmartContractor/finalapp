import requests
import time

BASE_URL = "http://localhost:8000"
# Get this from Clerk Dashboard -> JWT Templates -> Debug
TEST_TOKEN = "YOUR_CLERK_JWT_TOKEN"

def test_endpoints():
    # Test headers
    headers = {
        "Authorization": f"Bearer {TEST_TOKEN}"
    }
    
    # 1. Test health endpoint (no auth required)
    response = requests.get(f"{BASE_URL}/health")
    print("\nHealth Check:")
    print(response.json())
    
    # 2. Test /me endpoint without auth (should fail)
    response = requests.get(f"{BASE_URL}/api/v1/test/me")
    print("\nME Endpoint (No Auth):")
    print(response.status_code, response.json())
    
    # 3. Test /me endpoint with auth
    response = requests.get(f"{BASE_URL}/api/v1/test/me", headers=headers)
    print("\nME Endpoint (With Auth):")
    print(response.json())
    
    # 4. Test tier endpoint
    response = requests.get(f"{BASE_URL}/api/v1/test/tier", headers=headers)
    print("\nTier Endpoint:")
    print(response.json())
    
    # 5. Test rate limiting
    print("\nTesting Rate Limiting:")
    for i in range(12):  # Should hit rate limit for free tier
        response = requests.get(
            f"{BASE_URL}/api/v1/test/rate-limit-test", 
            headers=headers
        )
        print(f"Request {i+1}: {response.status_code}")
        print(f"Rate Limit Headers:", {
            k: v for k, v in response.headers.items() 
            if k.lower().startswith('x-ratelimit')
        })
        if response.status_code == 429:
            print("Rate limit hit!")
            break
        time.sleep(0.1)  # Small delay between requests

if __name__ == "__main__":
    test_endpoints()