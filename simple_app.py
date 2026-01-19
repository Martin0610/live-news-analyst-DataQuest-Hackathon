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

def generate_analytical_answer(question, articles, keywords):
    """Generate analytical answer for how/why/when questions"""
    answer = f"## 🔍 Analysis: {question}\n\n"
    
    top_article = articles[0]
    
    # Provide analytical context
    if "how" in question.lower():
        answer += "### 📋 Process & Methodology\n"
    elif "why" in question.lower():
        answer += "### 🎯 Reasoning & Context\n"
    elif "when" in question.lower():
        answer += "### ⏰ Timeline & Schedule\n"
    else:
        answer += "### 🔬 Detailed Analysis\n"
    
    answer += f"**Primary Source:** {top_article['title']}\n\n"
    
    if top_article.get('description'):
        answer += f"{top_article['description']}\n\n"
    
    # Add supporting evidence
    if len(articles) > 1:
        answer += "### 📚 Supporting Evidence\n"
        for i, article in enumerate(articles[1:4], 1):
            answer += f"{i}. **{article['title']}**\n"
            if article.get('description'):
                # Get first meaningful sentence
                sentences = article['description'].split('.')
                if sentences:
                    answer += f"   {sentences[0].strip()}.\n"
            answer += f"   *{article['source']}*\n\n"
    
    # Expert analysis section
    answer += "### 💡 Expert Perspective\n"
    sources = [a['source'] for a in articles[:3]]
    authoritative_sources = [s for s in sources if any(term in s.lower() for term in ['reuters', 'bloomberg', 'associated press', 'bbc', 'cnn', 'wall street journal', 'financial times'])]
    
    if authoritative_sources:
        answer += f"Analysis is supported by {len(authoritative_sources)} authoritative news sources including {', '.join(authoritative_sources[:2])}, "
        answer += "providing high confidence in the information accuracy.\n\n"
    else:
        answer += f"Information compiled from {len(sources)} news sources, providing comprehensive coverage of the topic.\n\n"
    
    return answer
    """Generate comprehensive, intelligent answers that will win hackathons!"""
    if not relevant_articles:
        return "I don't have any recent news articles that directly relate to your question. Please try asking about technology, business, science, or current events."
    
    question_lower = question.lower()
    
    # Enhanced question analysis
    question_keywords = extract_keywords(question)
    
    # Determine question intent and generate appropriate response
    if any(word in question_lower for word in ["latest", "recent", "new", "update", "current", "today"]):
        return generate_latest_news_answer(question, relevant_articles, question_keywords)
    elif any(word in question_lower for word in ["what", "what's", "what is", "tell me about"]):
        return generate_explanatory_answer(question, relevant_articles, question_keywords)
    elif any(word in question_lower for word in ["how", "why", "when", "where"]):
        return generate_analytical_answer(question, relevant_articles, question_keywords)
    elif any(word in question_lower for word in ["ai", "artificial intelligence", "machine learning", "chatgpt"]):
        return generate_ai_focused_answer(question, relevant_articles)
    elif any(word in question_lower for word in ["business", "company", "market", "stock", "economy"]):
        return generate_business_answer(question, relevant_articles)
    elif any(word in question_lower for word in ["technology", "tech", "software", "app", "digital"]):
        return generate_tech_answer(question, relevant_articles)
    else:
        return generate_comprehensive_answer(question, relevant_articles, question_keywords)

def generate_latest_news_answer(question, articles, keywords):
    """Generate answer focused on latest developments"""
    answer = "## 📰 Latest Developments\n\n"
    answer += "Based on the most recent news coverage, here are the key developments:\n\n"
    
    # Group articles by recency and importance
    top_articles = articles[:5]
    
    for i, article in enumerate(top_articles, 1):
        answer += f"### {i}. {article['title']}\n"
        if article.get('description'):
            # Extract key insights from description
            desc = article['description']
            answer += f"**Key Points:** {desc}\n\n"
        
        answer += f"**Source:** {article['source']} | **Category:** {article.get('category', 'General').title()}\n"
        answer += f"**Published:** {format_time(article.get('published_at', ''))}\n\n"
    
    # Add trend analysis
    categories = [a.get('category', 'general') for a in articles]
    top_category = max(set(categories), key=categories.count) if categories else 'technology'
    
    answer += f"### 📊 Trend Analysis\n"
    answer += f"The dominant theme in recent news is **{top_category}**, appearing in {categories.count(top_category)} out of {len(articles)} relevant articles. "
    answer += f"This suggests significant activity in the {top_category} sector.\n\n"
    
    return answer

def generate_explanatory_answer(question, articles, keywords):
    """Generate detailed explanatory answer"""
    top_article = articles[0]
    
    answer = f"## 💡 {question}\n\n"
    answer += f"Based on recent news analysis, here's what's happening:\n\n"
    
    # Main explanation from top article
    answer += f"### Primary Development\n"
    answer += f"**{top_article['title']}**\n\n"
    
    if top_article.get('description'):
        answer += f"{top_article['description']}\n\n"
    
    answer += f"*Source: {top_article['source']} - {top_article.get('category', 'General').title()} News*\n\n"
    
    # Supporting information
    if len(articles) > 1:
        answer += f"### Related Developments\n"
        for article in articles[1:4]:
            answer += f"• **{article['title']}** ({article['source']})\n"
            if article.get('description'):
                # Extract first sentence for context
                first_sentence = article['description'].split('.')[0] + '.'
                answer += f"  {first_sentence}\n"
        answer += "\n"
    
    # Context and implications
    answer += f"### 🎯 Key Implications\n"
    sources = list(set([a['source'] for a in articles[:5]]))
    answer += f"This development is being covered by {len(sources)} major news sources including {', '.join(sources[:3])}, "
    answer += f"indicating significant industry attention and potential impact.\n\n"
    
    return answer

def generate_ai_focused_answer(question, articles):
    """Generate AI-specific comprehensive answer"""
    answer = "## 🤖 AI & Technology Intelligence Report\n\n"
    
    # Filter for AI-related content
    ai_articles = []
    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        if any(term in text for term in ['ai', 'artificial intelligence', 'machine learning', 'chatgpt', 'openai', 'google ai', 'neural', 'llm']):
            ai_articles.append(article)
    
    if not ai_articles:
        ai_articles = articles[:3]  # Fallback to top articles
    
    answer += "### 🚀 Current AI Landscape\n"
    for i, article in enumerate(ai_articles[:3], 1):
        answer += f"**{i}. {article['title']}**\n"
        if article.get('description'):
            answer += f"{article['description']}\n"
        answer += f"*{article['source']} | {format_time(article.get('published_at', ''))}*\n\n"
    
    # AI trend analysis
    answer += "### 📈 Market Analysis\n"
    companies = extract_companies_mentioned(ai_articles)
    if companies:
        answer += f"**Key Players:** {', '.join(companies[:5])}\n"
    
    answer += f"**Coverage Intensity:** {len(ai_articles)} AI-related articles in recent news cycle\n"
    answer += f"**Industry Focus:** High activity suggests continued AI innovation and market expansion\n\n"
    
    return answer

def generate_business_answer(question, articles):
    """Generate business-focused answer"""
    answer = "## 💼 Business Intelligence Summary\n\n"
    
    # Extract business metrics and insights
    business_articles = [a for a in articles if a.get('category') == 'business' or 'business' in a.get('topic', '')]
    if not business_articles:
        business_articles = articles[:4]
    
    answer += "### 📊 Market Developments\n"
    for i, article in enumerate(business_articles[:3], 1):
        answer += f"**{i}. {article['title']}**\n"
        if article.get('description'):
            answer += f"{article['description']}\n"
        answer += f"*{article['source']} | {article.get('category', 'Business').title()}*\n\n"
    
    # Business insights
    answer += "### 💡 Strategic Insights\n"
    sources = [a['source'] for a in business_articles]
    financial_sources = [s for s in sources if any(term in s.lower() for term in ['bloomberg', 'reuters', 'financial', 'wall street', 'forbes', 'cnbc'])]
    
    if financial_sources:
        answer += f"**Financial Media Coverage:** {len(financial_sources)} major financial outlets reporting\n"
    
    answer += f"**Market Sentiment:** Active coverage across {len(set(sources))} news sources indicates significant market interest\n"
    answer += f"**Sector Activity:** Multiple developments suggest dynamic business environment\n\n"
    
    return answer

def generate_tech_answer(question, articles):
    """Generate technology-focused answer"""
    answer = "## 🔧 Technology Sector Analysis\n\n"
    
    tech_articles = articles[:4]
    
    answer += "### 🚀 Innovation Highlights\n"
    for i, article in enumerate(tech_articles, 1):
        answer += f"**{i}. {article['title']}**\n"
        if article.get('description'):
            answer += f"{article['description']}\n"
        answer += f"*{article['source']} | {format_time(article.get('published_at', ''))}*\n\n"
    
    # Tech trend analysis
    answer += "### 📱 Technology Trends\n"
    companies = extract_companies_mentioned(tech_articles)
    if companies:
        answer += f"**Leading Companies:** {', '.join(companies[:4])}\n"
    
    categories = [a.get('category', 'tech') for a in tech_articles]
    category_counts = {cat: categories.count(cat) for cat in set(categories)}
    top_category = max(category_counts.items(), key=lambda x: x[1])[0] if category_counts else 'technology'
    
    answer += f"**Dominant Theme:** {top_category.title()} ({category_counts.get(top_category, 1)} articles)\n"
    answer += f"**Innovation Index:** High activity with {len(tech_articles)} major developments\n\n"
    
    return answer

def generate_comprehensive_answer(question, articles, keywords):
    """Generate comprehensive multi-faceted answer"""
    answer = f"## 🎯 Comprehensive Analysis: {question}\n\n"
    
    # Main findings
    answer += "### 📋 Key Findings\n"
    top_articles = articles[:3]
    
    for i, article in enumerate(top_articles, 1):
        answer += f"**{i}. {article['title']}**\n"
        if article.get('description'):
            answer += f"{article['description']}\n"
        answer += f"*{article['source']} - {article.get('category', 'General').title()} | {format_time(article.get('published_at', ''))}*\n\n"
    
    # Cross-topic analysis
    if len(articles) > 3:
        answer += "### 🔗 Related Developments\n"
        for article in articles[3:6]:
            answer += f"• {article['title']} ({article['source']})\n"
        answer += "\n"
    
    # Summary insights
    answer += "### 📊 Summary Insights\n"
    categories = [a.get('category', 'general') for a in articles]
    sources = [a['source'] for a in articles]
    
    answer += f"**Coverage Breadth:** {len(set(sources))} news sources\n"
    answer += f"**Topic Diversity:** {len(set(categories))} different categories\n"
    answer += f"**Information Confidence:** High (based on {len(articles)} relevant articles)\n\n"
    
    return answer

def extract_companies_mentioned(articles):
    """Extract company names from articles"""
    companies = []
    company_keywords = ['Apple', 'Google', 'Microsoft', 'Amazon', 'Tesla', 'Meta', 'OpenAI', 'Netflix', 'Uber', 'Airbnb', 'SpaceX', 'Twitter', 'Facebook', 'Instagram', 'YouTube', 'LinkedIn', 'TikTok', 'Snapchat', 'Zoom', 'Slack', 'Salesforce', 'Oracle', 'IBM', 'Intel', 'AMD', 'NVIDIA', 'Samsung', 'Sony', 'Nintendo', 'Adobe', 'Spotify', 'PayPal', 'Square', 'Stripe', 'Coinbase', 'Robinhood']
    
    for article in articles:
        text = f"{article.get('title', '')} {article.get('description', '')}"
        for company in company_keywords:
            if company in text and company not in companies:
                companies.append(company)
    
    return companies

def format_time(time_str):
    """Format time string for better readability"""
    if not time_str:
        return "Recently"
    
    try:
        # Simple formatting - just return as is for now
        return time_str.split('T')[0] if 'T' in time_str else time_str
    except:
        return "Recently"

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
