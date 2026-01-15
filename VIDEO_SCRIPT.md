# 3-Minute Video Demo Script 🎬

## Setup Before Recording
- [ ] Have deployment URL ready
- [ ] Test API is responding
- [ ] Prepare browser tabs: GitHub repo, Render dashboard, API testing tool
- [ ] Have architecture diagram ready (can use README diagram)

---

## Script (180 seconds total)

### Opening (15 seconds)
**[Show title slide or GitHub repo]**

> "Hi! I'm presenting Live News Analyst - a real-time RAG system that updates its knowledge base instantly as breaking news arrives. Unlike traditional RAG systems that require batch re-indexing, ours uses Pathway's streaming architecture for sub-second latency updates."

---

### Architecture Overview (30 seconds)
**[Show architecture diagram from README]**

> "Here's how it works: GNews API streams breaking news every 60 seconds. Our custom Pathway connector ingests this data in real-time. The streaming table flows through incremental vector indexing - meaning only new articles are embedded, not the entire corpus. Finally, the LLM xPack provides RAG capabilities with OpenAI for retrieval and generation."

**Key points to emphasize:**
- Real-time streaming (not batch)
- Incremental indexing (not full re-indexing)
- Sub-second latency from ingestion to queryable

---

### Code Walkthrough (45 seconds)
**[Show code in IDE or GitHub]**

**1. Custom Connector (20 seconds)**
```python
# connectors/news_connector.py
class GNewsConnector(pw.io.python.ConnectorSubject):
    def run(self):
        while True:
            articles = self._fetch_news(topic)
            for article in articles:
                if url not in self.seen_urls:
                    self.next(...)  # Emit to Pathway
```

> "First, our custom connector extends Pathway's ingestion layer. It polls GNews API, tracks seen URLs, and emits only new articles to the streaming table. This is the key to real-time updates."

**2. Pipeline (25 seconds)**
```python
# app.py
documents = create_news_stream()  # Streaming table
chunks = split_and_flatten(documents)
embedded = embedder.apply(chunks)  # Incremental
server.run_server(embedded)
```

> "The main pipeline is simple: create streaming table, chunk documents, apply embeddings incrementally, and serve via REST API. Notice there's no batch processing - everything flows in real-time."

---

### Live Demo - The Proof (75 seconds)

**[Show terminal or Postman/curl]**

**Query 1 (20 seconds)**
```bash
curl -X POST https://your-app.onrender.com/v1/pw_ai_answer \
  -d '{"prompt": "What are the latest AI developments?"}'
```

> "Let me query our deployed system about latest AI developments."

**[Show response]**

> "Here's the answer based on current knowledge. Note the timestamp: [read timestamp]. The system cites 3 sources from articles published in the last hour."

**Wait Period (25 seconds)**

> "Now, our connector polls every 60 seconds. While we wait for the next batch, let me explain why this matters: Traditional RAG systems would need to re-index the entire vector database when new documents arrive. With Pathway's streaming architecture, new articles are automatically embedded and immediately queryable. No downtime, no batch jobs, no stale data."

**[Show timer or wait animation]**

**Query 2 (20 seconds)**
```bash
# Same query again
curl -X POST https://your-app.onrender.com/v1/pw_ai_answer \
  -d '{"prompt": "What are the latest AI developments?"}'
```

> "Same question, 60 seconds later..."

**[Show response]**

> "And here's the updated answer! Notice the new sources - articles that were published just minutes ago. The timestamp shows [read timestamp]. This proves our system updated its knowledge in real-time without any manual intervention."

**Comparison (10 seconds)**

> "Let me highlight the difference: Query 1 had 3 sources from [time]. Query 2 has 5 sources including articles from [newer time]. The knowledge base grew automatically."

---

### Technical Highlights (10 seconds)
**[Show bullet points or code]**

> "Key innovations: Custom Python connector for GNews, incremental vector indexing with Pathway, production-ready with Docker and Render deployment, and fault-tolerant with exponential backoff and rate limit handling."

---

### Closing (5 seconds)
**[Show GitHub repo or deployment URL]**

> "The entire system is open source, deployed on Render's free tier, and ready for production. Thank you!"

---

## Alternative: If Live Demo Fails

**Backup Plan (use pre-recorded demo):**

1. Show logs from Render dashboard proving real-time ingestion
2. Show two screenshots of API responses with different timestamps
3. Explain: "Here's a pre-recorded demo showing the same behavior"

---

## Visual Aids to Prepare

1. **Architecture Diagram** - Use the ASCII art from README or create a simple flowchart
2. **Code Snippets** - Highlight key sections in IDE
3. **API Responses** - Format JSON nicely or use Postman
4. **Timestamps** - Circle or highlight timestamps in responses
5. **Comparison Table** - Side-by-side of Query 1 vs Query 2

---

## Pro Tips

✅ **Do:**
- Speak clearly and confidently
- Show actual working deployment (not localhost)
- Emphasize "real-time" and "incremental"
- Highlight timestamps as proof
- Mention production-readiness

❌ **Don't:**
- Rush through the demo
- Use technical jargon without explanation
- Show errors (test everything first!)
- Forget to mention the innovation (custom connector)
- Skip the comparison (that's the proof!)

---

## Timing Breakdown

| Section | Time | Purpose |
|---------|------|---------|
| Opening | 15s | Hook the audience |
| Architecture | 30s | Show understanding |
| Code | 45s | Prove technical skill |
| Demo | 75s | Provide evidence |
| Highlights | 10s | Summarize innovation |
| Closing | 5s | Call to action |
| **Total** | **180s** | **3 minutes** |

---

## Questions You Might Get

**Q: Why not use batch processing?**
A: Batch processing has latency - you need to wait for the next batch job. Our streaming approach updates knowledge instantly.

**Q: How does this scale?**
A: Pathway's stateless design allows horizontal scaling. We can add more news sources, increase polling frequency, or distribute across multiple instances.

**Q: What about API rate limits?**
A: We implement exponential backoff and rate limit detection. For production, we'd use multiple API sources and caching.

**Q: Can this work with other data sources?**
A: Absolutely! The connector pattern is extensible. We could add Twitter, Reddit, RSS feeds, or any streaming data source.

---

## Recording Checklist

- [ ] Test deployment is working
- [ ] Prepare all browser tabs
- [ ] Test screen recording software
- [ ] Check audio quality
- [ ] Have backup plan ready
- [ ] Time yourself (aim for 2:45 to leave buffer)
- [ ] Record in quiet environment
- [ ] Use clear, large fonts
- [ ] Highlight important parts
- [ ] End with clear call-to-action

Good luck! 🚀
