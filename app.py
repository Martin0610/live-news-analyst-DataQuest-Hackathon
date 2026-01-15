import pathway as pw
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.vector_store import VectorStoreServer
import config
from connectors.news_connector import create_news_stream


def main():
    """Main Pathway pipeline for real-time RAG"""
    
    # Validate configuration
    config.validate_config()
    
    print("🚀 Starting Live News Analyst RAG Pipeline")
    print(f"📡 Monitoring topics: {', '.join(config.NEWS_TOPICS)}")
    print(f"🌐 Environment: {'Production' if config.HOST == '0.0.0.0' else 'Development'}")
    
    # Step 1: Create streaming news table
    news_table = create_news_stream()
    
    # Step 2: Transform to document format
    # Combine title, description, and content into rich text
    documents = news_table.select(
        data=pw.apply(
            lambda title, desc, content, source, url, topic: 
                f"Title: {title}\n\n"
                f"Source: {source}\n"
                f"Topic: {topic}\n"
                f"URL: {url}\n\n"
                f"{desc}\n\n"
                f"{content}",
            news_table.title,
            news_table.description,
            news_table.content,
            news_table.source,
            news_table.url,
            news_table.topic
        ),
        metadata=pw.apply(
            lambda url, source, topic, published: {
                "url": url,
                "source": source,
                "topic": topic,
                "published_at": published
            },
            news_table.url,
            news_table.source,
            news_table.topic,
            news_table.published_at
        )
    )
    
    # Step 3: Split documents into chunks
    chunked_documents = documents.select(
        chunks=pw.apply(
            lambda text: [
                {"text": chunk, "metadata": {}}
                for chunk in split_text(text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
            ],
            documents.data
        ),
        metadata=documents.metadata
    )
    
    # Flatten chunks
    chunks = chunked_documents.flatten(chunked_documents.chunks).select(
        data=pw.this.chunks["text"],
        metadata=chunked_documents.metadata
    )
    
    # Step 4: Create embeddings
    embedder = embedders.GeminiEmbedder(
        api_key=config.GEMINI_API_KEY,
        model=config.EMBEDDING_MODEL
    )
    
    embedded_chunks = chunks + chunks.select(
        vector=embedder.apply(text=chunks.data)
    )
    
    # Step 5: Create LLM
    llm = llms.GeminiChat(
        api_key=config.GEMINI_API_KEY,
        model=config.LLM_MODEL,
        temperature=0.0
    )
    
    # Step 6: Create vector store server
    server = VectorStoreServer(
        host=config.HOST,
        port=config.PORT,
        embedder=embedder,
        llm=llm
    )
    
    # Step 7: Serve the RAG endpoint
    print(f"✅ Server starting on http://{config.HOST}:{config.PORT}")
    print("📊 Real-time indexing active - knowledge updates automatically")
    print("🔗 API endpoint: POST /v1/pw_ai_answer")
    
    server.run_server(
        documents=embedded_chunks,
        with_cache=True
    )


def split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Simple text splitter"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    
    return chunks


if __name__ == "__main__":
    main()
