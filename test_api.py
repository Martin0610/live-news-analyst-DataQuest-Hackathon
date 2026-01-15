"""
Quick test script to verify your deployment is working
"""
import requests
import sys
import json

def test_api(base_url="http://localhost:8080"):
    """Test the RAG API endpoint"""
    
    print(f"🧪 Testing API at: {base_url}")
    print("=" * 60)
    
    endpoint = f"{base_url}/v1/pw_ai_answer"
    test_question = "What are the latest technology news?"
    
    try:
        print(f"\n📤 Sending request...")
        print(f"   Question: {test_question}")
        
        response = requests.post(
            endpoint,
            json={"prompt": test_question},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        print(f"\n📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! API is working")
            print("\n💡 Answer:")
            print("-" * 60)
            print(data.get("answer", "No answer returned"))
            print("-" * 60)
            
            sources = data.get("sources", [])
            print(f"\n📚 Sources used: {len(sources)}")
            
            if sources:
                print("\nTop 3 sources:")
                for i, source in enumerate(sources[:3], 1):
                    print(f"  {i}. {source.get('metadata', {}).get('source', 'Unknown')}")
            
            return 0
        else:
            print(f"\n❌ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return 1
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the server")
        print("   Make sure the app is running:")
        print("   python app.py")
        return 1
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timed out")
        print("   The server might be processing. Try again in a moment.")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return 1

if __name__ == "__main__":
    # Check if custom URL provided
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8080"
    
    print("\n" + "=" * 60)
    print("Live News Analyst - API Test")
    print("=" * 60)
    
    exit_code = test_api(url)
    
    print("\n" + "=" * 60)
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Tests failed")
    print("=" * 60 + "\n")
    
    sys.exit(exit_code)
