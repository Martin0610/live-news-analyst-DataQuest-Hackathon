# Hackathon Deployment Checklist ✅

## Pre-Deployment (5 minutes)

- [ ] Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] Get GNews API key from https://gnews.io/register
- [ ] Test locally:
  ```bash
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  # Create .env with your keys
  python app.py
  # In another terminal:
  python test_api.py
  ```

## Deployment to Render (5 minutes)

- [ ] Push code to GitHub:
  ```bash
  git init
  git add .
  git commit -m "Hackathon submission"
  git remote add origin YOUR_GITHUB_URL
  git push -u origin main
  ```

- [ ] Go to https://dashboard.render.com/
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repo
- [ ] Render auto-detects `render.yaml`
- [ ] Add environment variables:
  - `OPENAI_API_KEY`
  - `GNEWS_API_KEY`
- [ ] Click "Create Web Service"
- [ ] Wait 2-3 minutes for deployment

## Testing Deployment (2 minutes)

- [ ] Get your Render URL: `https://your-app.onrender.com`
- [ ] Test with curl:
  ```bash
  curl -X POST https://your-app.onrender.com/v1/pw_ai_answer \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"What's happening in tech today?\"}"
  ```
- [ ] Or use the test script:
  ```bash
  python test_api.py https://your-app.onrender.com
  ```

## Demo Preparation (10 minutes)

### What to Show in Your Video

1. **Architecture Diagram** (30 seconds)
   - Show the flow: News API → Pathway → Vector Store → LLM
   - Highlight real-time streaming

2. **Code Walkthrough** (60 seconds)
   - `connectors/news_connector.py` - Custom streaming connector
   - `app.py` - Pathway pipeline with incremental indexing
   - Emphasize: No batch re-indexing needed!

3. **Live Demo** (90 seconds)
   - Show deployed URL
   - Query 1: "What are the latest AI developments?"
   - Show response with sources
   - Wait 60 seconds (explain architecture)
   - Query 2: Same question
   - Show updated response with new articles
   - Highlight timestamps proving real-time updates

### Key Points to Mention

- ✅ **Real-time streaming** - not batch processing
- ✅ **Incremental indexing** - only new data is embedded
- ✅ **Sub-second latency** - from ingestion to queryable
- ✅ **Production-ready** - Docker, error handling, monitoring
- ✅ **Scalable** - stateless design, can add more sources
- ✅ **Custom connector** - extends Pathway's ingestion layer

## Troubleshooting

### If deployment fails:
- Check Render logs for errors
- Verify API keys are correct
- Ensure `render.yaml` is in root directory

### If API returns errors:
- Check GNews API quota (100 requests/day on free tier)
- Increase `POLLING_INTERVAL` to 300 in environment variables
- Verify OpenAI API key has credits

### If no new articles appear:
- News APIs may have delays
- Try different topics in config
- Check Render logs for connector errors

## Submission Checklist

- [ ] GitHub repo is public
- [ ] README.md is clear and complete
- [ ] Deployment is live and accessible
- [ ] Video demo is recorded (3 minutes max)
- [ ] Video shows:
  - [ ] Architecture explanation
  - [ ] Code highlights
  - [ ] Live real-time demonstration
  - [ ] Proof of incremental updates

## Bonus Points

- [ ] Add custom topics relevant to hackathon theme
- [ ] Show multiple queries demonstrating knowledge growth
- [ ] Explain technical innovations (custom connector, streaming)
- [ ] Mention scalability and production readiness
- [ ] Show error handling and monitoring

## Quick Commands Reference

```bash
# Local testing
python app.py                    # Start server
python test_api.py              # Test API
python demo.py                  # Interactive demo

# Deployment
git push origin main            # Deploy to Render (auto-deploys)

# Remote testing
python test_api.py https://your-app.onrender.com
```

## Support URLs

- Render Dashboard: https://dashboard.render.com/
- OpenAI Platform: https://platform.openai.com/
- GNews Dashboard: https://gnews.io/dashboard
- Pathway Docs: https://pathway.com/developers/

---

**Time Budget:**
- Setup & Testing: 10 minutes
- Deployment: 5 minutes
- Video Recording: 15 minutes
- **Total: 30 minutes** ⚡

Good luck! 🚀
