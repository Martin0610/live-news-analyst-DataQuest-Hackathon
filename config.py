import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

# News API Configuration
GNEWS_BASE_URL = "https://gnews.io/api/v4"
NEWS_TOPICS = ["technology", "business", "science"]  # Focus areas
NEWS_LANGUAGE = "en"
NEWS_COUNTRY = "us"
POLLING_INTERVAL = 60  # seconds

# RAG Configuration
EMBEDDING_MODEL = "gemini-embedding-001"  # Gemini embedding model
LLM_MODEL = "gemini-1.5-flash"  # Fast and free!
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8080"))

def validate_config():
    """Validate required configuration"""
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not set in .env file")
    if not GNEWS_API_KEY:
        raise ValueError("GNEWS_API_KEY not set in .env file")
    print("✓ Configuration validated")
