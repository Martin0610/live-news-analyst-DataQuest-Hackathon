"""
Simplified version without Pathway - just a REST API with news ingestion
"""
import os
import time
import requests
import threading
from datetime import datetime
from flask import Flask, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GNEWS_BASE_URL = "https://gnews.io/api/v4"
NEWS_TOPICS = ["technology", "business", "science"]
POLLING_INTERVAL = 60

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-pro')

# In-memory storage
news_articles = []
seen_urls = set()

app = Flask(__name__)


def fetch_news():
    """Background thread to fetch news"""
    print("🔴 Starting news fetcher...")
    
    while True:
        try:
            for topic in NEWS_TOPICS:
                url = f"{GNEWS_BASE_URL}/top-headlines"
                params = {
                    "apikey": GNEWS_API_KEY,
                    "topic": topic,
                    "lang": "en",
                    "country": "us",
                    "max": 10
                }
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    articles = data.get("articles", [])
                    
                    for article in articles:
                        url = article.get("url")
                        if url and url not in seen_urls:
                            seen_urls.add(url)
                            news_articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "content": article.get("content", ""),
                                "source": article.get("source", {}).get("name", "Unknown"),
                                "url": url,
                                "topic": topic,
                                "published_at": article.get("publishedAt", ""),
                                "fetched_at": datetime.now().isoformat()
                            })
                            print(f"📰 New article: {article.get('title')[:60]}...")
            
            print(f"ℹ️  Total articles: {len(news_articles)}")
            time.sleep(POLLING_INTERVAL)
            
        except Exception as e:
            print(f"⚠️  Error fetching news: {e}")
            time.sleep(10)


@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "articles_count": len(news_articles),
        "topics": NEWS_TOPICS
    })


@app.route('/v1/pw_ai_answer', methods=['POST'])
def answer_question():
    """Answer questions using Gemini and news context"""
    try:
        data = request.get_json()
        question = data.get('prompt', '')
        
        if not question:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Get recent articles as context
        recent_articles = news_articles[-20:] if len(news_articles) > 20 else news_articles
        
        if not recent_articles:
            return jsonify({
                "answer": "No news articles available yet. Please wait for the first batch to be fetched.",
                "sources": []
            })
        
        # Build context from articles
        context = "Here are the latest news articles:\n\n"
        for i, article in enumerate(recent_articles, 1):
            context += f"{i}. {article['title']}\n"
            context += f"   Source: {article['source']} | Topic: {article['topic']}\n"
            context += f"   {article['description']}\n\n"
        
        # Generate answer with Gemini
        prompt = f"{context}\n\nBased on the above news articles, please answer this question:\n{question}"
        
        response = model.generate_content(prompt)
        answer = response.text
        
        # Return response with sources
        sources = [
            {
                "title": article['title'],
                "source": article['source'],
                "url": article['url'],
                "topic": article['topic']
            }
            for article in recent_articles
        ]
        
        return jsonify({
            "answer": answer,
            "sources": sources[:5]  # Top 5 sources
        })
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Start news fetcher in background
    fetcher_thread = threading.Thread(target=fetch_news, daemon=True)
    fetcher_thread.start()
    
    print("🚀 Starting Live News Analyst (Simplified)")
    print(f"📡 Monitoring topics: {', '.join(NEWS_TOPICS)}")
    print(f"✅ Server starting on port 8080")
    
    # Run Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
