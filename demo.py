"""
Real-time demonstration script
Proves that the RAG system updates knowledge instantly as new data arrives
"""

import requests
import time
from datetime import datetime


API_URL = "http://localhost:8080/v1/pw_ai_answer"


def query_rag(question: str) -> dict:
    """Query the RAG system"""
    response = requests.post(
        API_URL,
        json={"prompt": question},
        headers={"Content-Type": "application/json"}
    )
    response.raise_for_status()
    return response.json()


def print_response(question: str, response: dict, iteration: int):
    """Pretty print the response"""
    print(f"\n{'='*80}")
    print(f"Query #{iteration} at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*80}")
    print(f"❓ Question: {question}")
    print(f"\n💡 Answer:\n{response.get('answer', 'No answer')}")
    print(f"\n📚 Sources used: {len(response.get('sources', []))}")
    print(f"{'='*80}\n")


def main():
    """Run the real-time demonstration"""
    
    print("🎬 Live RAG Demonstration - Real-Time Knowledge Updates")
    print("=" * 80)
    print("\nThis demo will:")
    print("1. Query about recent AI/tech news")
    print("2. Wait for new articles to be ingested")
    print("3. Query again and show updated knowledge")
    print("\nMake sure app.py is running in another terminal!")
    print("=" * 80)
    
    # Wait for user to start
    input("\nPress Enter to start the demonstration...")
    
    # Test question about recent news
    question = "What are the latest developments in artificial intelligence and technology?"
    
    try:
        # Query 1: Initial state
        print("\n🔍 Querying initial knowledge base...")
        response1 = query_rag(question)
        print_response(question, response1, 1)
        
        # Wait for new data
        wait_time = 70  # Slightly longer than polling interval
        print(f"⏳ Waiting {wait_time} seconds for new articles to be ingested...")
        print("   (The connector polls every 60 seconds)")
        
        for remaining in range(wait_time, 0, -10):
            print(f"   {remaining} seconds remaining...")
            time.sleep(10)
        
        # Query 2: After new data
        print("\n🔍 Querying updated knowledge base...")
        response2 = query_rag(question)
        print_response(question, response2, 2)
        
        # Compare responses
        print("\n📊 REAL-TIME CAPABILITY PROOF:")
        print("-" * 80)
        
        answer1 = response1.get('answer', '')
        answer2 = response2.get('answer', '')
        
        if answer1 != answer2:
            print("✅ SUCCESS: Answers are different!")
            print("   The knowledge base updated automatically with new articles.")
            print(f"   Sources in query 1: {len(response1.get('sources', []))}")
            print(f"   Sources in query 2: {len(response2.get('sources', []))}")
        else:
            print("⚠️  Answers are similar (no new relevant articles arrived)")
            print("   Try running the demo again or wait for breaking news.")
        
        print("-" * 80)
        
        # Interactive mode
        print("\n🎮 Interactive Mode - Ask your own questions!")
        print("(Type 'quit' to exit)\n")
        
        while True:
            user_question = input("Your question: ").strip()
            
            if user_question.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Demo complete!")
                break
            
            if not user_question:
                continue
            
            try:
                response = query_rag(user_question)
                print(f"\n💡 Answer:\n{response.get('answer', 'No answer')}\n")
            except Exception as e:
                print(f"❌ Error: {e}\n")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the RAG server")
        print("   Make sure app.py is running: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()
