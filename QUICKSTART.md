# Quick Start Guide

## 5-Minute Setup

### 1. Get API Keys (2 minutes)

**OpenAI API Key:**
- Go to https://platform.openai.com/api-keys
- Create new key
- Copy it

**GNews API Key (Free):**
- Go to https://gnews.io/register
- Sign up (no credit card needed)
- Copy your API key from dashboard
- Free tier: 100 requests/day, 10 articles/request

### 2. Install (1 minute)

```bash
# Clone/download the project
cd live-news-analyst

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure (1 minute)

Create `.env` file:

```bash
# Copy the example
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux

# Edit .env and add your keys
OPENAI_API_KEY=sk-your-key-here
GNEWS_API_KEY=your-gnews-key-here
```

### 4. Run (1 minute)

**Terminal 1 - Start the server:**
```bash
python app.py
```

Wait for: `✅ Server running on http://0.0.0.0:8080`

**Terminal 2 - Run the demo:**
```bash
python demo.py
```

## What You'll See

1. **Initial Query**: System answers based on current news
2. **Wait Period**: New articles are fetched (60 seconds)
3. **Updated Query**: Same question, different answer with new info
4. **Proof**: The knowledge updated in real-time!

## Testing Manually

```bash
# Query the API directly
curl -X POST http://localhost:8080/v1/pw_ai_answer \
  -H "Content-Type: application/json" \
  -d "{\"prompt\": \"What's happening in AI today?\"}"
```

## Troubleshooting

**"Cannot connect to server"**
- Make sure `python app.py` is running in another terminal

**"API key not set"**
- Check your `.env` file exists and has valid keys

**"Rate limit exceeded"**
- GNews free tier: 100 requests/day
- Increase `POLLING_INTERVAL` in config.py to 300 (5 minutes)

**No new articles**
- News APIs may have delays
- Try different topics in `config.py`: `NEWS_TOPICS = ["world", "nation", "business"]`

## Next Steps

1. **Customize topics**: Edit `NEWS_TOPICS` in `config.py`
2. **Add more sources**: Implement NewsAPI.org or NewsData.io connectors
3. **Improve chunking**: Use Pathway's built-in splitters
4. **Add UI**: Build a Streamlit or Gradio interface
5. **Deploy**: Use the included Dockerfile

## Video Demo Tips

For your 3-minute video:

1. **Show the code** (10 seconds): Highlight the custom connector
2. **Start the server** (20 seconds): Show it ingesting news
3. **First query** (30 seconds): Ask about recent news
4. **Wait & explain** (60 seconds): Explain the architecture while waiting
5. **Second query** (30 seconds): Show updated answer
6. **Proof** (30 seconds): Compare responses, show timestamps

## Architecture Highlights to Mention

- **Custom Python Connector**: Extends Pathway's ingestion layer
- **Incremental Indexing**: Only new articles are embedded
- **Sub-second Latency**: From ingestion to queryable
- **Production Ready**: Docker, persistence, fault tolerance
- **Scalable**: Stateless design, can add more sources

Good luck with your hackathon! 🚀
