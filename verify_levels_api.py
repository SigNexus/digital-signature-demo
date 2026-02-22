import requests
import json
import sys

# Ensure UTF-8 output for Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

def test_api():
    base_url = "http://127.0.0.1"
    tests = [
        {"name": "Level 1 (Plaintext)", "url": f"{base_url}:8022/forward", "msg": "Hello Level 1"},
        {"name": "Level 2 (Hashing)", "url": f"{base_url}:8012/forward", "msg": "Hello Level 2"},
        {"name": "Level 3 (Signature)", "url": f"{base_url}:8002/forward", "msg": "Hello Level 3"},
    ]

    print("--- API Verification Results ---")
    for test in tests:
        print(f"Testing {test['name']}...")
        try:
            response = requests.post(test['url'], json={"message": test['msg']}, timeout=10)
            if response.status_code == 200:
                data = response.json()
                receiver_resp = data.get("receiver_response", {})
                status = receiver_resp.get("status", "No Status")
                print(f"  Result: {status}")
                if "Valid" in status or "Received" in status:
                    print(f"  [PASS]")
                else:
                    print(f"  [FAIL] Unexpected response: {data}")
            else:
                print(f"  [FAIL] HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"  [FAIL] Error: {e}")
        print("-" * 30)

if __name__ == "__main__":
    test_api()
