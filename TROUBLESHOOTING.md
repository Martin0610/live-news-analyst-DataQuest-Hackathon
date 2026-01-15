# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 Deployment Issues

#### "Application failed to respond" on Render

**Symptoms:**
- Render shows "Application failed to respond"
- Logs show connection errors
- Health check fails

**Solutions:**
1. Check environment variables are set:
   ```bash
   # In Render dashboard, verify:
   OPENAI_API_KEY=sk-...
   GNEWS_API_KEY=...
   ```

2. Check logs for specific errors:
   - Go to Render dashboard → Your service → Logs
   - Look for Python errors or API failures

3. Verify PORT binding:
   - Render automatically sets PORT environment variable
   - Our config.py reads it: `PORT = int(os.getenv("PORT", "8080"))`

4. Check build logs:
   - Ensure all dependencies installed successfully
   - Look for `pip install` errors

#### "Build failed" on Render

**Symptoms:**
- Build process fails
- Can't install dependencies

**Solutions:**
1. Check `requirements.txt` syntax:
   ```
   pathway>=0.13.0
   openai>=1.0.0
   python-dotenv>=1.0.0
   requests>=2.31.0
   ```

2. Verify Python version:
   - `runtime.txt` should have: `python-3.11.0`
   - Render supports Python 3.8-3.11

3. Check for conflicting dependencies:
   ```bash
   # Test locally first
   pip install -r requirements.txt
   ```

---

### 🔑 API Key Issues

#### "OPENAI_API_KEY not set"

**Symptoms:**
- Error on startup: "OPENAI_API_KEY not set in .env file"
- App crashes immediately

**Solutions:**
1. **Local development:**
   ```bash
   # Create .env file
   copy .env.example .env  # Windows
   cp .env.example .env    # Mac/Linux
   
   # Edit .env and add:
   OPENAI_API_KEY=sk-your-actual-key-here
   ```

2. **Render deployment:**
   - Go to dashboard → Your service → Environment
   - Add variable: `OPENAI_API_KEY` = `sk-...`
   - Click "Save Changes"
   - Redeploy if needed

3. **Verify key is valid:**
   - Go to https://platform.openai.com/api-keys
   - Check key is active and has credits

#### "Invalid API key" from OpenAI

**Symptoms:**
- Error: "Incorrect API key provided"
- 401 Unauthorized errors

**Solutions:**
1. Regenerate API key:
   - Go to https://platform.openai.com/api-keys
   - Create new key
   - Update in .env or Render

2. Check for extra spaces:
   ```bash
   # Bad:
   OPENAI_API_KEY= sk-...  # Space before key
   
   # Good:
   OPENAI_API_KEY=sk-...
   ```

3. Verify billing:
   - Check https://platform.openai.com/account/billing
   - Ensure you have credits

#### "Rate limit exceeded" from GNews

**Symptoms:**
- Error: "429 Too Many Requests"
- Connector stops fetching

**Solutions:**
1. Check your quota:
   - Go to https://gnews.io/dashboard
   - Free tier: 100 requests/day
   - Each poll = 1 request per topic

2. Increase polling interval:
   ```bash
   # In Render environment variables:
   POLLING_INTERVAL=300  # 5 minutes instead of 60 seconds
   ```

3. Reduce topics:
   ```bash
   # In Render environment variables:
   NEWS_TOPICS=technology  # Just one topic
   ```

4. Upgrade plan:
   - GNews Pro: $9/month for 10,000 requests/day

---

### 🐛 Runtime Errors

#### "No articles found"

**Symptoms:**
- Connector runs but no articles appear
- Logs show "No new articles"

**Solutions:**
1. Check GNews API is working:
   ```bash
   curl "https://gnews.io/api/v4/top-headlines?apikey=YOUR_KEY&topic=technology&lang=en"
   ```

2. Try different topics:
   ```python
   # In config.py or environment variable:
   NEWS_TOPICS = ["world", "nation", "business"]
   ```

3. Check country/language settings:
   ```python
   # In config.py:
   NEWS_LANGUAGE = "en"
   NEWS_COUNTRY = "us"  # Try "uk", "ca", etc.
   ```

4. Verify API key permissions:
   - Some GNews plans have topic restrictions

#### "Out of memory" on Render

**Symptoms:**
- App crashes with memory errors
- Render shows "Out of memory"

**Solutions:**
1. Reduce chunk size:
   ```bash
   # In Render environment variables:
   CHUNK_SIZE=500
   CHUNK_OVERLAP=100
   ```

2. Limit article history:
   ```python
   # In connectors/news_connector.py:
   # Add max size to seen_urls
   if len(self.seen_urls) > 1000:
       self.seen_urls = set(list(self.seen_urls)[-500:])
   ```

3. Upgrade Render plan:
   - Free tier: 512MB RAM
   - Starter: 2GB RAM ($7/month)

#### "Connection timeout" errors

**Symptoms:**
- Connector fails to fetch news
- Timeout errors in logs

**Solutions:**
1. Increase timeout:
   ```python
   # In connectors/news_connector.py:
   response = requests.get(url, params=params, timeout=30)  # Increase from 10
   ```

2. Check network connectivity:
   - Render may have temporary network issues
   - Wait and retry

3. Add retry logic (already implemented):
   - Exponential backoff handles transient failures

---

### 🧪 Testing Issues

#### "Cannot connect to server" when running demo.py

**Symptoms:**
- `demo.py` fails with connection error
- "Cannot connect to the RAG server"

**Solutions:**
1. Ensure `app.py` is running:
   ```bash
   # Terminal 1:
   python app.py
   
   # Wait for: "✅ Server starting on..."
   
   # Terminal 2:
   python demo.py
   ```

2. Check port is correct:
   ```python
   # In demo.py:
   API_URL = "http://localhost:8080/v1/pw_ai_answer"
   ```

3. Verify firewall:
   - Windows: Allow Python through firewall
   - Mac: Check System Preferences → Security

#### "No answer returned" from API

**Symptoms:**
- API returns 200 but answer is empty
- Response: `{"answer": ""}`

**Solutions:**
1. Wait for articles to be ingested:
   - First query may be empty if no articles yet
   - Wait 60 seconds for first poll

2. Check vector index:
   - Logs should show "📰 New article: ..."
   - If not, check GNews API key

3. Try different question:
   ```bash
   # More specific:
   "What happened in technology today?"
   
   # Instead of:
   "Tell me about stuff"
   ```

---

### 🔧 Configuration Issues

#### "Module not found" errors

**Symptoms:**
- `ImportError: No module named 'pathway'`
- Missing dependency errors

**Solutions:**
1. Activate virtual environment:
   ```bash
   # Windows:
   venv\Scripts\activate
   
   # Mac/Linux:
   source venv/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Check Python version:
   ```bash
   python --version  # Should be 3.10+
   ```

#### "Invalid configuration" errors

**Symptoms:**
- App fails validation
- Config errors on startup

**Solutions:**
1. Check all required variables:
   ```bash
   # Required in .env:
   OPENAI_API_KEY=sk-...
   GNEWS_API_KEY=...
   ```

2. Verify format:
   ```bash
   # No quotes needed:
   OPENAI_API_KEY=sk-abc123
   
   # Not:
   OPENAI_API_KEY="sk-abc123"
   ```

---

### 📊 Performance Issues

#### "Slow response times"

**Symptoms:**
- Queries take >10 seconds
- Timeout errors

**Solutions:**
1. Check OpenAI API latency:
   - May be slow during peak hours
   - Try different model: `gpt-3.5-turbo`

2. Reduce chunk retrieval:
   ```python
   # In app.py, reduce top_k:
   server = VectorStoreServer(
       ...,
       top_k=3  # Default is 5
   )
   ```

3. Enable caching:
   ```python
   # Already enabled:
   server.run_server(documents=embedded_chunks, with_cache=True)
   ```

#### "High API costs"

**Symptoms:**
- OpenAI bill is high
- Unexpected charges

**Solutions:**
1. Use cheaper models:
   ```python
   # In config.py:
   EMBEDDING_MODEL = "text-embedding-3-small"  # Already optimal
   LLM_MODEL = "gpt-3.5-turbo"  # Cheaper than gpt-4
   ```

2. Reduce polling frequency:
   ```bash
   POLLING_INTERVAL=300  # 5 minutes
   ```

3. Limit chunk size:
   ```bash
   CHUNK_SIZE=500  # Fewer embeddings
   ```

4. Monitor usage:
   - https://platform.openai.com/usage

---

### 🚀 Deployment-Specific Issues

#### Render Free Tier Limitations

**Issue:** App spins down after 15 minutes

**Solutions:**
- Accept cold starts (30-60s first request)
- Upgrade to Starter plan ($7/month) for always-on
- Use cron job to ping every 10 minutes:
  ```bash
  # External service like cron-job.org
  curl https://your-app.onrender.com/v1/pw_ai_answer
  ```

#### Docker Deployment Issues

**Symptoms:**
- Docker build fails
- Container crashes

**Solutions:**
1. Build locally first:
   ```bash
   docker build -t live-news-analyst .
   docker run -p 8080:8080 \
     -e OPENAI_API_KEY=sk-... \
     -e GNEWS_API_KEY=... \
     live-news-analyst
   ```

2. Check logs:
   ```bash
   docker logs <container-id>
   ```

3. Verify environment variables:
   ```bash
   docker run -it live-news-analyst env
   ```

---

## Getting Help

### Debug Checklist

Before asking for help, check:

- [ ] All API keys are set and valid
- [ ] Dependencies are installed (`pip list`)
- [ ] Python version is 3.10+ (`python --version`)
- [ ] Logs show specific error messages
- [ ] API quotas are not exceeded
- [ ] Network connectivity is working
- [ ] Environment variables are correct

### Useful Commands

```bash
# Check if server is running
curl http://localhost:8080/v1/pw_ai_answer

# Test API keys
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"

# View logs (Render)
# Go to dashboard → Logs

# Test GNews API
curl "https://gnews.io/api/v4/top-headlines?apikey=YOUR_KEY&topic=technology"

# Check Python packages
pip list | grep pathway
pip list | grep openai
```

### Contact & Resources

- **Pathway Docs**: https://pathway.com/developers/
- **OpenAI Support**: https://help.openai.com/
- **GNews Support**: https://gnews.io/contact
- **Render Support**: https://render.com/docs

---

## Still Having Issues?

1. Check logs carefully for specific error messages
2. Search error message in documentation
3. Try the solution in this guide
4. Test with minimal configuration
5. Ask for help with:
   - Exact error message
   - Steps to reproduce
   - Environment details (OS, Python version)
   - Logs (remove API keys!)

Good luck! 🚀
