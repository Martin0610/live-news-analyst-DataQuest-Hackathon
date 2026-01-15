import pathway as pw
import requests
import time
from datetime import datetime
from typing import Any
import config


class GNewsConnector(pw.io.python.ConnectorSubject):
    """Custom Pathway connector for GNews API streaming"""
    
    def __init__(self, api_key: str, topics: list[str], polling_interval: int = 60):
        super().__init__()
        self.api_key = api_key
        self.topics = topics
        self.polling_interval = polling_interval
        self.seen_urls = set()
        
    def run(self):
        """Main streaming loop - continuously fetch and emit news"""
        print(f"🔴 Starting GNews stream (polling every {self.polling_interval}s)")
        consecutive_errors = 0
        max_consecutive_errors = 5
        
        while True:
            try:
                new_articles_count = 0
                
                for topic in self.topics:
                    articles = self._fetch_news(topic)
                    
                    for article in articles:
                        url = article.get("url")
                        
                        # Only emit new articles
                        if url and url not in self.seen_urls:
                            self.seen_urls.add(url)
                            new_articles_count += 1
                            
                            # Emit to Pathway table
                            self.next(
                                title=article.get("title", ""),
                                content=article.get("content", ""),
                                description=article.get("description", ""),
                                url=url,
                                source=article.get("source", {}).get("name", "Unknown"),
                                published_at=article.get("publishedAt", ""),
                                topic=topic,
                                fetched_at=datetime.now().isoformat()
                            )
                            
                            print(f"📰 New article: {article.get('title')[:60]}...")
                
                if new_articles_count == 0:
                    print(f"ℹ️  No new articles (checked {len(self.topics)} topics)")
                else:
                    print(f"✅ Ingested {new_articles_count} new articles")
                
                consecutive_errors = 0  # Reset error counter on success
                time.sleep(self.polling_interval)
                
            except Exception as e:
                consecutive_errors += 1
                print(f"⚠️  Error fetching news ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"❌ Too many consecutive errors. Stopping connector.")
                    break
                
                # Exponential backoff
                backoff_time = min(60, 10 * (2 ** (consecutive_errors - 1)))
                print(f"   Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
    
    def _fetch_news(self, topic: str) -> list[dict[str, Any]]:
        """Fetch news from GNews API"""
        url = f"{config.GNEWS_BASE_URL}/top-headlines"
        params = {
            "apikey": self.api_key,
            "topic": topic,
            "lang": config.NEWS_LANGUAGE,
            "country": config.NEWS_COUNTRY,
            "max": 10
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "errors" in data:
                print(f"⚠️  GNews API error: {data['errors']}")
                return []
            
            articles = data.get("articles", [])
            return articles
            
        except requests.exceptions.Timeout:
            print(f"⚠️  API request timeout for topic: {topic}")
            return []
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print(f"⚠️  Rate limit exceeded. Consider increasing POLLING_INTERVAL")
            else:
                print(f"⚠️  HTTP error {e.response.status_code}: {e}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"⚠️  API request failed for topic {topic}: {e}")
            return []
        except Exception as e:
            print(f"⚠️  Unexpected error parsing response: {e}")
            return []


def create_news_stream() -> pw.Table:
    """Create a Pathway streaming table from GNews"""
    
    connector = GNewsConnector(
        api_key=config.GNEWS_API_KEY,
        topics=config.NEWS_TOPICS,
        polling_interval=config.POLLING_INTERVAL
    )
    
    # Define schema
    class NewsSchema(pw.Schema):
        title: str
        content: str
        description: str
        url: str
        source: str
        published_at: str
        topic: str
        fetched_at: str
    
    # Create streaming table
    news_table = pw.io.python.read(
        connector,
        schema=NewsSchema,
        autocommit_duration_ms=1000  # Commit every second
    )
    
    return news_table
