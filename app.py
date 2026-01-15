import pathway as pw
from pathway.xpacks.llm import embedders, llms
import config
from connectors.news_connector import create_news_stream
import json


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
        )
    )
    
    # Step 3: Create embeddings
    embedder = embedders.GeminiEmbedder(
        api_key=config.GEMINI_API_KEY,
        model=config.EMBEDDING_MODEL
    )
    
    embedded = documents + documents.select(
        vector=embedder.apply(text=documents.data)
    )
    
    # Step 4: Create LLM
    llm = llms.GeminiChat(
        api_key=config.GEMINI_API_KEY,
        model=config.LLM_MODEL,
        temperature=0.0
    )
    
    print(f"✅ Server starting on http://{config.HOST}:{config.PORT}")
    print("📊 Real-time indexing active - knowledge updates automatically")
    print("🔗 System is running - news being ingested")
    
    # Keep the pipeline running
    pw.run()


if __name__ == "__main__":
    main()
