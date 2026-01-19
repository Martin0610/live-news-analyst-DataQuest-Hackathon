"""
Simplified version without Pathway - just a REST API with news ingestion
"""
import os
import time
import requests
import threading
from datetime import datetime
from flask import Flask, request, jsonify, render_template
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
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini model initialized successfully")
    except Exception as e:
        print(f"⚠️  Warning: Gemini model initialization failed: {e}")
        model = None
else:
    print("⚠️  Warning: GEMINI_API_KEY not found")
    model = None

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
    """Serve the web interface"""
    return render_template('index.html')


@app.route('/api/status')
def status():
    """API endpoint for status"""
    return jsonify({
        "status": "running",
        "articles_count": len(news_articles),
        "topics": NEWS_TOPICS
    })


@app.route('/api/articles')
def get_articles():
    """Get recent articles"""
    recent = news_articles[-10:] if len(news_articles) > 10 else news_articles
    return jsonify({
        "articles": [
            {
                "title": a['title'],
                "source": a['source'],
                "topic": a['topic'],
                "published_at": a['published_at'],
                "url": a['url']
            }
            for a in recent
        ],
        "total": len(news_articles)
    })


@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    topic_counts = {}
    source_counts = {}
    
    for article in news_articles:
        topic = article['topic']
        source = article['source']
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
    
    return jsonify({
        "total_articles": len(news_articles),
        "by_topic": topic_counts,
        "top_sources": dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
        "last_updated": news_articles[-1]['fetched_at'] if news_articles else None
    })


@app.route('/v1/pw_ai_answer', methods=['POST'])
def answer_question():
    """Answer questions using Gemini and news context"""
    try:
        data = request.get_json()
        question = data.get('prompt', '')
        
        print(f"📥 Received question: {question[:100]}")
        
        if not question:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Check if Gemini API key is configured
        if not GEMINI_API_KEY or not model:
            return jsonify({
                "error": "Gemini API not properly configured",
                "details": "GEMINI_API_KEY environment variable is missing or model failed to initialize"
            }), 500
        
        # Get recent articles as context
        recent_articles = news_articles[-20:] if len(news_articles) > 20 else news_articles
        
        print(f"📚 Using {len(recent_articles)} articles for context")
        
        if not recent_articles:
            return jsonify({
                "answer": "No news articles available yet. The system is still fetching the first batch of articles. Please wait a moment and try again.",
                "sources": []
            })
        
        # Build shorter context to avoid token limits
        context = "Recent news headlines:\n\n"
        for i, article in enumerate(recent_articles[-5:], 1):  # Only use last 5 articles
            context += f"{i}. {article['title']}\n"
            if article['description']:
                context += f"   Summary: {article['description'][:150]}...\n"
            context += f"   Source: {article['source']} | Topic: {article['topic']}\n\n"
        
        # Shorter, more focused prompt
        prompt = f"""Based on these recent news articles:

{context}

Question: {question}

Please provide a helpful answer based on the news above. If the question is not related to the news, say so politely."""
        
        print(f"🤔 Calling Gemini API with prompt length: {len(prompt)} characters")
        
        try:
            # Use more conservative settings
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower temperature for more focused responses
                    max_output_tokens=300,  # Shorter responses
                    top_p=0.8,
                    top_k=40
                )
            )
            
            if not response.text:
                raise Exception("Empty response from Gemini")
                
            answer = response.text.strip()
            print(f"✅ Answer generated: {len(answer)} characters")
            
        except Exception as gemini_error:
            print(f"❌ Gemini API Error: {type(gemini_error).__name__}: {str(gemini_error)}")
            
            # Handle specific Gemini errors
            error_str = str(gemini_error).lower()
            if "quota" in error_str or "429" in error_str:
                return jsonify({
                    "error": "API quota exceeded. Please try again in a few moments.",
                    "details": "Gemini API rate limit reached"
                }), 429
            elif "safety" in error_str:
                return jsonify({
                    "error": "Content filtered for safety. Please try rephrasing your question.",
                    "details": "Gemini safety filters triggered"
                }), 400
            elif "invalid" in error_str and "key" in error_str:
                return jsonify({
                    "error": "API configuration error. Please contact support.",
                    "details": "Invalid API key"
                }), 500
            else:
                # Generic fallback response
                return jsonify({
                    "answer": f"I'm having trouble processing your question right now. However, based on the recent news, here are the latest headlines: {', '.join([a['title'][:50] + '...' for a in recent_articles[-3:]])}",
                    "sources": [
                        {
                            "title": article['title'],
                            "source": article['source'],
                            "url": article['url'],
                            "topic": article['topic']
                        }
                        for article in recent_articles[-3:]
                    ]
                })
        
        # Return successful response
        sources = [
            {
                "title": article['title'],
                "source": article['source'],
                "url": article['url'],
                "topic": article['topic']
            }
            for article in recent_articles[-5:]
        ]
        
        return jsonify({
            "answer": answer,
            "sources": sources
        })
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"❌ ERROR in answer_question: {error_type}: {error_msg}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        # Always return a response, even if there's an error
        return jsonify({
            "answer": "I'm experiencing technical difficulties right now. Please try again in a moment, or check back as I continue to gather more news articles.",
            "sources": [],
            "error": f"Technical error: {error_type}",
            "details": error_msg
        }), 500


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
