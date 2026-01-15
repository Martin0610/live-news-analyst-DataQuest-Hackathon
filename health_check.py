"""
Simple health check script for monitoring
"""
import requests
import sys

def check_health():
    try:
        response = requests.post(
            "http://localhost:8080/v1/pw_ai_answer",
            json={"prompt": "test"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ Service is healthy")
            return 0
        else:
            print(f"⚠️ Service returned status {response.status_code}")
            return 1
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_health())
