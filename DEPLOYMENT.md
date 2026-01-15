# Deployment Guide - Render

## Quick Deploy to Render (5 minutes)

### Step 1: Prepare Your Repository

1. Push this code to GitHub (if not already done):
```bash
git init
git add .
git commit -m "Ready for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will auto-detect the `render.yaml` file

### Step 3: Configure Environment Variables

In the Render dashboard, add these environment variables:

```
OPENAI_API_KEY=sk-your-openai-key-here
GNEWS_API_KEY=your-gnews-key-here
```

### Step 4: Deploy

1. Click "Create Web Service"
2. Wait 2-3 minutes for deployment
3. Your app will be live at: `https://your-app-name.onrender.com`

## Testing Your Deployment

```bash
# Replace with your Render URL
curl -X POST https://your-app-name.onrender.com/v1/pw_ai_answer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the latest AI developments?"}'
```

## Important Notes for Render Free Tier

1. **Cold Starts**: Free tier spins down after 15 minutes of inactivity
   - First request after idle may take 30-60 seconds
   - Subsequent requests are fast

2. **Memory Limits**: 512MB RAM on free tier
   - Should be sufficient for this app
   - If issues occur, upgrade to Starter plan ($7/month)

3. **Build Time**: ~2-3 minutes
   - Pathway installation takes most time
   - Cached after first build

4. **API Rate Limits**:
   - GNews free tier: 100 requests/day
   - App polls every 60 seconds = ~1,440 requests/day
   - **Solution**: Increase `POLLING_INTERVAL` to 300 (5 minutes) in environment variables

## Environment Variables (Optional)

Add these to customize behavior:

```
POLLING_INTERVAL=300          # Poll every 5 minutes (saves API calls)
NEWS_TOPICS=technology,world  # Comma-separated topics
CHUNK_SIZE=1000              # Text chunk size
CHUNK_OVERLAP=200            # Chunk overlap
```

## Monitoring Your Deployment

1. **Logs**: View in Render dashboard → Your Service → Logs
2. **Health**: Check if service is running
3. **Metrics**: View request count and response times

## Troubleshooting

### "Application failed to respond"
- Check logs for errors
- Verify API keys are set correctly
- Ensure PORT environment variable is not overridden

### "Out of memory"
- Reduce `CHUNK_SIZE` to 500
- Upgrade to Starter plan

### "API rate limit exceeded"
- Increase `POLLING_INTERVAL` to 300 or 600
- Or upgrade GNews plan

### "No articles found"
- Check GNews API key is valid
- Try different topics: world, nation, business, sports

## Alternative: Docker Deployment

If you prefer Docker (works on any platform):

```bash
# Build
docker build -t live-news-analyst .

# Run
docker run -p 8080:8080 \
  -e OPENAI_API_KEY=your-key \
  -e GNEWS_API_KEY=your-key \
  live-news-analyst
```

## Production Optimizations

For production use, consider:

1. **Persistence**: Add volume mount for Pathway cache
2. **Monitoring**: Add Sentry or similar for error tracking
3. **Rate Limiting**: Implement request throttling
4. **Caching**: Add Redis for response caching
5. **Multi-source**: Add more news APIs for redundancy

## Cost Estimates

**Free Tier (Render + APIs):**
- Render: $0/month
- OpenAI: ~$0.50-2/month (depends on usage)
- GNews: $0/month (100 requests/day)
- **Total: ~$0.50-2/month**

**Paid Tier (Better performance):**
- Render Starter: $7/month
- OpenAI: ~$5-10/month
- GNews Pro: $9/month (10,000 requests/day)
- **Total: ~$21-26/month**

## Support

If you encounter issues:
1. Check Render logs first
2. Verify all environment variables
3. Test API keys locally before deploying
4. Check GNews API quota in dashboard

Good luck with your hackathon! 🚀
