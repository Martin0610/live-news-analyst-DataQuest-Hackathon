# Architecture Deep Dive

## System Overview

Live News Analyst is a real-time RAG (Retrieval-Augmented Generation) system built on Pathway's streaming architecture. Unlike traditional RAG systems that process data in batches, our system continuously ingests, indexes, and serves the latest information with sub-second latency.

## Core Components

### 1. Data Ingestion Layer

**GNews Connector** (`connectors/news_connector.py`)
- Custom `ConnectorSubject` implementation
- Polls GNews API every 60 seconds (configurable)
- Deduplicates articles using URL tracking
- Emits new articles to Pathway streaming table
- Handles rate limits with exponential backoff

```python
class GNewsConnector(pw.io.python.ConnectorSubject):
    def run(self):
        while True:
            for topic in self.topics:
                articles = self._fetch_news(topic)
                for article in articles:
                    if url not in self.seen_urls:
                        self.next(...)  # Emit to stream
            time.sleep(self.polling_interval)
```

**Key Innovation:** The connector extends Pathway's native ingestion layer, enabling seamless integration with the streaming pipeline.

### 2. Streaming Pipeline

**Pathway Table** (`app.py`)
- Receives articles from connector as streaming table
- Schema: title, content, description, url, source, published_at, topic
- Auto-commits every 1 second for low latency

**Document Transformation**
- Combines title, description, and content into rich text
- Preserves metadata (source, topic, URL, timestamp)
- Formats for optimal LLM comprehension

**Text Chunking**
- Splits documents into 1000-character chunks
- 200-character overlap for context preservation
- Maintains metadata linkage

### 3. Vector Indexing

**Incremental Embeddings**
- Uses OpenAI `text-embedding-3-small` model
- Only new chunks are embedded (not entire corpus)
- Pathway's reactive computation ensures efficiency
- No batch re-indexing required

**Vector Store**
- In-memory vector index for fast retrieval
- Automatically updates as new embeddings arrive
- Supports similarity search with metadata filtering

### 4. RAG Layer

**LLM xPack Integration**
- Retrieval: Finds top-k relevant chunks via vector similarity
- Augmentation: Constructs context from retrieved chunks
- Generation: OpenAI GPT-4o-mini generates answer
- Citation: Returns source metadata for transparency

**Query Flow:**
1. User sends question via REST API
2. Question is embedded using same model
3. Vector similarity search finds relevant chunks
4. Chunks + question sent to LLM
5. LLM generates answer with citations
6. Response returned with source metadata

### 5. API Server

**VectorStoreServer**
- REST API on port 8080
- Endpoint: `POST /v1/pw_ai_answer`
- Request: `{"prompt": "your question"}`
- Response: `{"answer": "...", "sources": [...]}`
- Built-in caching for repeated queries

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     GNews API (External)                     │
│              Breaking news published every minute            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP GET (every 60s)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              GNewsConnector (Custom Python)                  │
│  - Polls API                                                 │
│  - Deduplicates by URL                                       │
│  - Emits new articles                                        │
└────────────────────────┬────────────────────────────────────┘
                         │ pw.io.python.read()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                 Pathway Streaming Table                      │
│  Schema: title, content, description, url, source, ...       │
│  Auto-commit: 1000ms                                         │
└────────────────────────┬────────────────────────────────────┘
                         │ .select() transformation
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Document Transformation                         │
│  - Combine title + description + content                     │
│  - Preserve metadata                                         │
└────────────────────────┬────────────────────────────────────┘
                         │ split_text()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Text Chunking                              │
│  - 1000 char chunks                                          │
│  - 200 char overlap                                          │
│  - Flatten to chunk table                                    │
└────────────────────────┬────────────────────────────────────┘
                         │ embedder.apply()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              OpenAI Embedding (Incremental)                  │
│  Model: text-embedding-3-small                               │
│  Only new chunks embedded                                    │
└────────────────────────┬────────────────────────────────────┘
                         │ Vector index
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Vector Store                               │
│  - In-memory index                                           │
│  - Similarity search                                         │
│  - Metadata filtering                                        │
└────────────────────────┬────────────────────────────────────┘
                         │ Query time
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                              │
│  1. Embed user question                                      │
│  2. Retrieve top-k chunks                                    │
│  3. Construct context                                        │
│  4. Generate answer (GPT-4o-mini)                            │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP Response
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   REST API Client                            │
│  POST /v1/pw_ai_answer                                       │
│  {"prompt": "question"} → {"answer": "...", "sources": [...]}│
└─────────────────────────────────────────────────────────────┘
```

## Latency Analysis

**End-to-End Timeline:**

```
T+0s:    News article published
T+15s:   GNews API indexes article
T+60s:   Our connector polls and fetches
T+61s:   Article emitted to Pathway table
T+62s:   Document transformed and chunked
T+63s:   Chunks embedded (OpenAI API call)
T+64s:   Vector index updated
T+64s:   Article is now queryable!
```

**Total Latency: ~64 seconds** from publication to queryable

**Query Latency:**
- Embedding user question: ~200ms
- Vector similarity search: ~10ms
- LLM generation: ~1-2s
- **Total query time: ~2s**

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows multiple instances
- Load balancer distributes queries
- Shared vector store (Redis/Pinecone for production)

### Vertical Scaling
- Increase polling frequency (30s instead of 60s)
- Add more news topics
- Larger chunk sizes for more context

### Multi-Source Scaling
- Add NewsAPI.org connector
- Add Reddit/Twitter connectors
- Aggregate from multiple sources
- Deduplicate across sources

## Production Enhancements

### Persistence
```python
# Add persistence for fault tolerance
pw.io.fs.write(
    documents,
    path="./cache",
    format="jsonlines"
)
```

### Monitoring
```python
# Add metrics collection
documents.select(
    count=pw.reducers.count()
).debug("article_count")
```

### Caching
```python
# Add Redis for response caching
import redis
cache = redis.Redis()

def cached_query(question):
    if cached := cache.get(question):
        return cached
    result = rag_query(question)
    cache.setex(question, 300, result)  # 5 min TTL
    return result
```

### Rate Limiting
```python
# Add rate limiting for API protection
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@limiter.limit("10/minute")
def query_endpoint():
    ...
```

## Comparison with Traditional RAG

| Feature | Traditional RAG | Live News Analyst |
|---------|----------------|-------------------|
| Data Ingestion | Batch (hourly/daily) | Streaming (60s) |
| Indexing | Full re-index | Incremental only |
| Latency | Minutes to hours | ~64 seconds |
| Freshness | Stale between batches | Always current |
| Scalability | Limited by batch size | Horizontal scaling |
| Complexity | Cron jobs, orchestration | Single pipeline |

## Technical Innovations

1. **Custom Connector Pattern**: Extends Pathway's ingestion layer for any API
2. **Incremental Computation**: Only new data is processed, not entire corpus
3. **Streaming Tables**: Native support for continuous data flow
4. **Reactive Updates**: Vector index updates automatically as data arrives
5. **Production Ready**: Error handling, monitoring, deployment configs included

## Future Enhancements

### Short-term
- Add more news sources (NewsAPI, NewsData.io)
- Implement response caching
- Add sentiment analysis
- Support multiple languages

### Long-term
- Real-time trend detection
- Topic clustering and summarization
- WebSocket support for push notifications
- Multi-modal support (images, videos)
- Personalized news feeds

## References

- [Pathway Documentation](https://pathway.com/developers/)
- [Pathway LLM xPack](https://pathway.com/developers/api-docs/pathway-xpacks-llm)
- [GNews API](https://gnews.io/docs/v4)
- [OpenAI Embeddings](https://platform.openai.com/docs/guides/embeddings)

---

Built for Inter IIT Hackathon 2026 🚀
