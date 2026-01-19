![alt text](<WhatsApp Image 2026-01-16 at 5.56.20 PM.jpeg>)# 🚀 Live News Analyst - Real-Time RAG System

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://live-news-analyst.onrender.com)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A real-time Retrieval-Augmented Generation (RAG) system that continuously ingests breaking news and answers questions using the latest information. Built for the Inter IIT Hackathon 2026.

**� Live Demo**: https://live-news-analyst.onre6nder.com

---

## ✨ Key Features

- **⚡ Real-Time Updates**: Fetches news every 60 seconds automatically
- **🤖 AI-Powered Answers**: Uses Google Gemini 2.0 for intelligent responses
- **📊 Live Statistics**: Track articles by topic and source in real-time
- **🎨 Beautiful UI**: Modern, responsive web interface
- **🔌 REST API**: Full API access for integrations
- **💰 100% Free**: Runs on free tier (Render + Gemini + GNews)

---

## 🏗️ Architecture

```
┌─────────────────┐
│  GNews API      │  Fetches breaking news every 60s
│  (3 topics)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ News Ingestion  │  Background thread continuously polls
│ (Flask Thread)  │  Deduplicates and stores articles
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ In-Memory Store │  Fast access to latest articles
│ (Python List)   │  No database needed
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Gemini AI      │  Analyzes articles and generates answers
│  (2.0 Flash)    │  Context-aware responses
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Web UI +      │  Beautiful interface + REST API
│   REST API      │  Real-time updates via JavaScript
└─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Gemini API key (free): https://aistudio.google.com/app/apikey
- GNews API key (free): https://gnews.io/register

### Installation

```bash
# Clone repository
git clone https://github.com/Martin0610/live-news-analyst-DataQuest-Hackathon.git
cd live-news-analyst-DataQuest-Hackathon

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys

# Run application
python simple_app.py
```

Visit: http://localhost:8080

---

## 📡 API Endpoints

### GET `/`
Web interface (HTML)

### GET `/api/status`
```json
{
  "status": "running",
  "articles_count": 42,
  "topics": ["technology", "business", "science"]
}
```

### GET `/api/articles`
Returns latest 10 articles with metadata

### GET `/api/stats`
Returns statistics by topic and source

### POST `/v1/pw_ai_answer`
```json
{
  "prompt": "What are the latest AI developments?"
}
```

Response:
```json
{
  "answer": "Based on recent articles...",
  "sources": [...]
}
```

---

## 🎯 How It Works

1. **Background Thread**: Continuously polls GNews API every 60 seconds
2. **Deduplication**: Tracks seen URLs to avoid duplicates
3. **Storage**: Stores articles in memory for fast access
4. **Context Building**: Combines recent articles into context for AI
5. **AI Generation**: Gemini analyzes context and generates answers
6. **Real-Time UI**: JavaScript updates stats and articles automatically

---

## 🎨 Features Showcase

### Real-Time Article Feed
- See new articles appear automatically
- Organized by topic (technology, business, science)
- Source attribution for each article

### Live Statistics
- Articles by topic breakdown
- Top news sources
- Total article count
- Last update timestamp

### Intelligent Q&A
- Ask questions in natural language
- Get answers based on latest news
- See source articles for transparency
- Context-aware responses

---

## 🛠️ Technology Stack

- **Backend**: Flask (Python web framework)
- **AI**: Google Gemini 2.0 Flash
- **News API**: GNews.io
- **Frontend**: Vanilla JavaScript + CSS
- **Deployment**: Render (Docker)
- **Storage**: In-memory (Python lists)

---

## 📊 Performance

- **Latency**: ~2 seconds per query
- **Update Frequency**: 60 seconds
- **Memory Usage**: ~50MB
- **API Calls**: ~1,440/day (GNews), ~100/day (Gemini)
- **Cost**: $0/month (all free tiers)

---

## � Deployment

### Deploy to Render

1. Fork this repository
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. New Web Service → Connect repository
4. Add environment variables:
   - `GEMINI_API_KEY`
   - `GNEWS_API_KEY`
5. Deploy!

Render auto-detects the `Dockerfile` and deploys automatically.

---

## 🧪 Testing

```bash
# Test API
python test_api.py

# Test remote deployment
python test_api.py https://your-app.onrender.com
```

---

## � Environment Variables

```env
GEMINI_API_KEY=your_gemini_key_here
GNEWS_API_KEY=your_gnews_key_here
PORT=8080  # Optional, defaults to 8080
```

---

## 🎓 Hackathon Highlights

### Innovation
- Real-time news ingestion without batch processing
- Automatic knowledge updates every 60 seconds
- No database required - pure streaming architecture

### Technical Excellence
- Clean, modular code
- Production-ready deployment
- Comprehensive error handling
- Real-time UI updates

### User Experience
- Beautiful, intuitive interface
- Instant answers to questions
- Transparent source attribution
- Live statistics dashboard

---

## 🔮 Future Enhancements

- [ ] Add more news sources (NewsAPI, Reddit, Twitter)
- [ ] Implement caching for faster responses
- [ ] Add sentiment analysis
- [ ] Support multiple languages
- [ ] WebSocket for push notifications
- [ ] User authentication and saved queries

---

## 📄 License

MIT License - Built for Inter IIT Hackathon 2026

---

## 🙏 Acknowledgments

- **Google Gemini**: For free AI API
- **GNews.io**: For free news API
- **Render**: For free hosting
- **Inter IIT**: For the hackathon opportunity

---

## 📞 Contact

**GitHub**: https://github.com/Martin0610/live-news-analyst-DataQuest-Hackathon

**Live Demo**: https://live-news-analyst.onrender.com

---

**Built with ❤️ for Inter IIT Hackathon 2026** 🏆
