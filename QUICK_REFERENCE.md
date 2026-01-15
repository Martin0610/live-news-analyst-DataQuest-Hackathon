# 🚀 Quick Reference Card

**Live News Analyst - Real-Time RAG System**

---

## ⚡ 30-Second Overview

Real-time RAG system that updates knowledge in 65 seconds vs 1-24 hours for traditional systems. Custom Pathway connector streams breaking news, incremental vector indexing, production-ready deployment.

---

## 🎯 Quick Commands

### Local Setup (10 minutes)
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Add your API keys to .env
python app.py
```

### Test Locally
```bash
python test_api.py
python demo.py
```

### Deploy to Render (5 minutes)
```bash
git init
git add .
git commit -m "Deploy"
git push origin main
# Then: Render dashboard → New Web Service → Connect repo
# Add env vars: OPENAI_API_KEY, GNEWS_API_KEY
```

### Test Remote
```bash
python test_api.py https://your-app.onrender.com
```

---

## 📚 Essential Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `README.md` | Overview | Start here |
| `HACKATHON_CHECKLIST.md` | Submission guide | Before submitting |
| `VIDEO_SCRIPT.md` | Demo script | Recording video |
| `DEPLOYMENT.md` | Deploy guide | Going to production |
| `QUICKSTART.md` | Local setup | First time setup |
| `PITCH.md` | Presentation | Pitching to judges |
| `TROUBLESHOOTING.md` | Fix issues | When stuck |

---

## 🔑 API Keys Needed

**BOTH 100% FREE!** 🎉

1. **Gemini**: https://aistudio.google.com/app/apikey (FREE - 1,500 req/day)
2. **GNews**: https://gnews.io/register (FREE - 100 req/day)

**See [GEMINI_SETUP.md](GEMINI_SETUP.md) for detailed setup!**

Add to `.env`:
```
GEMINI_API_KEY=AIza...
GNEWS_API_KEY=...
```

---

## 🎬 Demo Flow (3 minutes)

1. **Opening** (15s): "Real-time RAG, 55x faster"
2. **Architecture** (30s): Show streaming diagram
3. **Code** (45s): Highlight custom connector
4. **Live Demo** (75s): Query → Wait → Query → Compare
5. **Close** (15s): "Production-ready, thank you!"

---

## 💡 Key Talking Points

- ✅ **55x faster** than traditional RAG (65s vs 1-24 hours)
- ✅ **Custom connector** extends Pathway's ingestion layer
- ✅ **Incremental indexing** - only new data processed
- ✅ **Production-ready** - Docker, Render, error handling
- ✅ **Provable** - timestamps show real-time updates

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't connect | Check `python app.py` is running |
| API key error | Verify keys in `.env` or Render env vars |
| No articles | Wait 60s for first poll, check GNews key |
| Rate limit | Increase `POLLING_INTERVAL=300` |
| Out of memory | Reduce `CHUNK_SIZE=500` |

---

## 📊 Project Stats

- **Code**: 500 lines
- **Docs**: 2000+ lines
- **Files**: 20+
- **Setup Time**: 10 minutes
- **Deploy Time**: 5 minutes
- **Demo Time**: 3 minutes
- **Cost**: $1/month (free tier)

---

## 🏆 Winning Points

1. **Innovation**: Custom connector pattern
2. **Completeness**: Code + deployment + docs
3. **Proof**: Live demo with timestamps
4. **Quality**: Production-ready, error handling
5. **Documentation**: 10 comprehensive guides

---

## 📞 Important URLs

- **Live Demo**: https://your-app.onrender.com
- **GitHub**: https://github.com/your-username/live-news-analyst
- **OpenAI**: https://platform.openai.com/
- **GNews**: https://gnews.io/
- **Render**: https://dashboard.render.com/

---

## 🎯 API Usage

```bash
# Query the system
curl -X POST https://your-app.onrender.com/v1/pw_ai_answer \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the latest AI developments?"}'

# Response
{
  "answer": "Based on recent articles...",
  "sources": [...]
}
```

---

## ⏱️ Time Budget

- **Setup**: 10 minutes
- **Deploy**: 5 minutes
- **Video**: 15 minutes
- **Submit**: 5 minutes
- **Total**: 35 minutes

---

## ✅ Pre-Submission Checklist

- [ ] Code pushed to GitHub
- [ ] Deployed to Render
- [ ] Environment variables set
- [ ] Test API working
- [ ] Video recorded
- [ ] Documentation complete
- [ ] Links ready

---

## 🎓 Architecture in 3 Lines

```
GNews API → Custom Connector → Pathway Stream
    ↓
Incremental Embeddings → Vector Store → LLM
    ↓
REST API → Real-time Answers
```

---

## 💪 Competitive Edge

| Feature | Traditional | Ours |
|---------|------------|------|
| Latency | 1-24 hours | 65 seconds |
| Indexing | Full re-index | Incremental |
| Architecture | Batch + Cron | Streaming |
| Cost | High | Low |

---

## 🚀 Next Steps

1. **Now**: Deploy to Render (5 min)
2. **Then**: Record video (15 min)
3. **Finally**: Submit (5 min)

**You're ready to win! 🏆**

---

## 📱 Contact

- **Docs**: See all .md files
- **Issues**: Check TROUBLESHOOTING.md
- **Questions**: Review ARCHITECTURE.md

---

**Built for Inter IIT Hackathon 2026** 🚀

*Keep this card handy during demo and presentation!*
