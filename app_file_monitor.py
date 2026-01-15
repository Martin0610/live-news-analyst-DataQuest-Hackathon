"""
Alternative implementation: Monitor a local folder for new documents
Useful for testing real-time behavior without API rate limits
"""

import pathway as pw
from pathway.xpacks.llm import embedders, llms
from pathway.xpacks.llm.vector_store import VectorStoreServer
import config


def main():
    """RAG pipeline with file monitoring"""
    
    config.validate_config()
    
    print("🚀 Starting File Monitor RAG Pipeline")
    print("📁 Monitoring: ./data/ folder")
    print("   Add/modify/delete files to see real-time updates!")
    
    # Step 1: Monitor folder for changes
    documents = pw.io.fs.read(
        path="./data",
        format="binary",
        mode="streaming",  # Real-time monitoring
        with_metadata=True
    )
    
    # Step 2: Parse documents (supports txt, pdf, docx, etc.)
    parsed = documents.select(
        data=pw.apply(lambda x: x.decode('utf-8', errors='ignore'), documents.data),
        metadata=documents._metadata
    )
    
    # Step 3: Create embeddings
    embedder = embedders.OpenAIEmbedder(
        api_key=config.OPENAI_API_KEY,
        model=config.EMBEDDING_MODEL
    )
    
    embedded = parsed + parsed.select(
        vector=embedder.apply(text=parsed.data)
    )
    
    # Step 4: Create LLM
    llm = llms.OpenAIChat(
        api_key=config.OPENAI_API_KEY,
        model=config.LLM_MODEL,
        temperature=0.0
    )
    
    # Step 5: Serve RAG endpoint
    server = VectorStoreServer(
        host=config.HOST,
        port=config.PORT,
        embedder=embedder,
        llm=llm
    )
    
    server.run_server(
        documents=embedded,
        with_cache=True
    )
    
    print(f"✅ Server running on http://{config.HOST}:{config.PORT}")
    print("\n📝 To test real-time updates:")
    print("   1. Add a new .txt file to ./data/")
    print("   2. Query about its content")
    print("   3. Modify the file")
    print("   4. Query again - answer updates instantly!")


if __name__ == "__main__":
    main()
