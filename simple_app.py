"""
Completely FREE version - No paid APIs!
Uses intelligent text analysis and keyword matching
"""
import os
import time
import requests
import threading
import re
from datetime import datetime
from collections import Counter
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

# Configuration
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
GNEWS_BASE_URL = "https://gnews.io/api/v4"
NEWS_TOPICS = ["technology", "business", "science"]
POLLING_INTERVAL = 60

# In-memory storage
news_articles = []
seen_urls = set()

app = Flask(__name__)

# Keywords for different topics
TOPIC_KEYWORDS = {
    "ai": ["artificial intelligence", "ai", "machine learning", "neural", "chatgpt", "openai", "google ai", "deepmind", "llm", "gpt", "claude", "gemini"],
    "technology": ["tech", "software", "app", "digital", "internet", "computer", "smartphone", "apple", "google", "microsoft", "meta", "tesla"],
    "business": ["company", "business", "market", "stock", "investment", "economy", "financial", "revenue", "profit", "startup", "ipo"],
    "science": ["research", "study", "discovery", "scientist", "university", "breakthrough", "experiment", "climate", "space", "nasa"],
    "health": ["health", "medical", "doctor", "hospital", "treatment", "vaccine", "drug", "disease", "covid", "medicine"],
    "crypto": ["bitcoin", "cryptocurrency", "blockchain", "crypto", "ethereum", "nft", "defi", "web3"],
    "politics": ["government", "president", "election", "policy", "congress", "senate", "political", "vote"],
    "sports": ["sports", "football", "basketball", "soccer", "olympics", "championship", "team", "player"]
}

def extract_keywords(text):
    """Extract important keywords from text"""
    if not text:
        return []
    
    # Convert to lowercase and remove special characters
    text = re.sub(r'[^\w\s]', ' ', text.lower())
    words = text.split()
    
    # Filter out common words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
    
    keywords = [word for word in words if len(word) > 3 and word not in stop_words]
    return keywords

def categorize_article(article):
    """Categorize article based on content"""
    text = f"{article.get('title', '')} {article.get('description', '')}".lower()
    
    scores = {}
    for category, keywords in TOPIC_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text)
        if score > 0:
            scores[category] = score
    
    return max(scores.items(), key=lambda x: x[1])[0] if scores else "general"

def find_relevant_articles(question, articles):
    """Find articles relevant to the question"""
    question_lower = question.lower()
    question_keywords = extract_keywords(question)
    
    scored_articles = []
    
    for article in articles:
        score = 0
        article_text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        
        # Direct keyword matches
        for keyword in question_keywords:
            if keyword in article_text:
                score += 2
        
        # Topic category matches
        for category, keywords in TOPIC_KEYWORDS.items():
            if category in question_lower:
                for keyword in keywords:
                    if keyword in article_text:
                        score += 3
        
        # Title relevance (higher weight)
        title_lower = article.get('title', '').lower()
        for keyword in question_keywords:
            if keyword in title_lower:
                score += 5
        
        if score > 0:
            scored_articles.append((article, score))
    
    # Sort by relevance score
    scored_articles.sort(key=lambda x: x[1], reverse=True)
    return [article for article, score in scored_articles[:8]]

def generate_smart_answer(question, relevant_articles):
    """Generate intelligent answer based on articles"""
    if not relevant_articles:
        return "I don't have any recent news articles that directly relate to your question. Please try asking about technology, business, science, or current events."
    
    question_lower = question.lower()
    
    # Determine question type
    if any(word in question_lower for word in ["what", "what's", "what is"]):
        answer_type = "explanation"
    elif any(word in question_lower for word in ["how", "how to"]):
        answer_type = "process"
    elif any(word in question_lower for word in ["why", "why is"]):
        answer_type = "reason"
    elif any(word in question_lower for word in ["when", "when did"]):
        answer_type = "time"
    elif any(word in question_lower for word in ["who", "who is"]):
        answer_type = "person"
    elif any(word in question_lower for word in ["latest", "recent", "new", "update"]):
        answer_type = "latest"
    else:
        answer_type = "general"
    
    # Build answer based on type
    if answer_type == "latest":
        answer = "Here are the latest developments:\n\n"
        for i, article in enumerate(relevant_articles[:5], 1):
            answer += f"{i}. **{article['title']}**\n"
            if article.get('description'):
                answer += f"   {article['description'][:200]}...\n"
            answer += f"   Source: {article['source']} | Topic: {article['topic']}\n\n"
    
    elif answer_type == "explanation":
        answer = "Based on recent news, here's what I found:\n\n"
        top_article = relevant_articles[0]
        answer += f"**{top_article['title']}**\n\n"
        if top_article.get('description'):
            answer += f"{top_article['description']}\n\n"
        answer += f"Source: {top_article['source']}\n\n"
        
        if len(relevant_articles) > 1:
            answer += "Related news:\n"
            for article in relevant_articles[1:4]:
                answer += f"• {article['title']} ({article['source']})\n"
    
    else:
        # General response
        answer = f"Based on recent news coverage, here's what I found:\n\n"
        
        # Group by topic
        topic_groups = {}
        for article in relevant_articles[:6]:
            topic = article.get('topic', 'general')
            if topic not in topic_groups:
                topic_groups[topic] = []
            topic_groups[topic].append(article)
        
        for topic, articles in topic_groups.items():
            answer += f"**{topic.title()} News:**\n"
            for article in articles[:3]:
                answer += f"• {article['title']} ({article['source']})\n"
            answer += "\n"
    
    return answer

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
                            
                            # Add category
                            category = categorize_article(article)
                            
                            news_articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "content": article.get("content", ""),
                                "source": article.get("source", {}).get("name", "Unknown"),
                                "url": url,
                                "topic": topic,
                                "category": category,
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
                "category": a.get('category', 'general'),
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
    category_counts = {}
    
    for article in news_articles:
        topic = article['topic']
        source = article['source']
        category = article.get('category', 'general')
        
        topic_counts[topic] = topic_counts.get(topic, 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
        category_counts[category] = category_counts.get(category, 0) + 1
    
    return jsonify({
        "total_articles": len(news_articles),
        "by_topic": topic_counts,
        "by_category": category_counts,
        "top_sources": dict(sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
        "last_updated": news_articles[-1]['fetched_at'] if news_articles else None
    })


@app.route('/v1/pw_ai_answer', methods=['POST'])
def answer_question():
    """Answer questions using intelligent text analysis - 100% FREE!"""
    try:
        data = request.get_json()
        question = data.get('prompt', '')
        
        print(f"📥 Received question: {question[:100]}")
        
        if not question:
            return jsonify({"error": "No prompt provided"}), 400
        
        # Get recent articles
        recent_articles = news_articles[-50:] if len(news_articles) > 50 else news_articles
        
        print(f"📚 Analyzing {len(recent_articles)} articles")
        
        if not recent_articles:
            return jsonify({
                "answer": "No news articles available yet. The system is still fetching the first batch of articles. Please wait a moment and try again.",
                "sources": []
            })
        
        # Find relevant articles
        relevant_articles = find_relevant_articles(question, recent_articles)
        
        print(f"🎯 Found {len(relevant_articles)} relevant articles")
        
        # Generate smart answer
        answer = generate_smart_answer(question, relevant_articles)
        
        # Prepare sources
        sources = [
            {
                "title": article['title'],
                "source": article['source'],
                "url": article['url'],
                "topic": article['topic'],
                "category": article.get('category', 'general')
            }
            for article in relevant_articles[:5]
        ]
        
        print(f"✅ Answer generated: {len(answer)} characters")
        
        return jsonify({
            "answer": answer,
            "sources": sources,
            "method": "intelligent_analysis",
            "articles_analyzed": len(recent_articles),
            "relevant_found": len(relevant_articles)
        })
        
    except Exception as e:
        error_msg = str(e)
        error_type = type(e).__name__
        print(f"❌ ERROR in answer_question: {error_type}: {error_msg}")
        import traceback
        print(f"❌ Full traceback: {traceback.format_exc()}")
        
        # Return helpful fallback
        recent = news_articles[-5:] if news_articles else []
        headlines = [a['title'] for a in recent]
        
        return jsonify({
            "answer": f"I'm experiencing technical difficulties, but here are the latest headlines I can share: {' | '.join(headlines) if headlines else 'No articles available yet.'}",
            "sources": [
                {
                    "title": article['title'],
                    "source": article['source'],
                    "url": article['url'],
                    "topic": article['topic']
                }
                for article in recent
            ],
            "error": f"Technical error: {error_type}",
            "details": error_msg
        }), 500


if __name__ == '__main__':
    # Start news fetcher in background
    fetcher_thread = threading.Thread(target=fetch_news, daemon=True)
    fetcher_thread.start()
    
    print("🚀 Starting Live News Analyst (100% FREE VERSION)")
    print("💚 No paid APIs - Uses intelligent text analysis!")
    print(f"📡 Monitoring topics: {', '.join(NEWS_TOPICS)}")
    print(f"✅ Server starting on port 8080")
    
    # Run Flask app
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
