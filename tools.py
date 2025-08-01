import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@tool
def get_latest_news(topic: str = "latest news") -> str:
    """
    Fetches the latest news from RSS feeds based on a topic.
    
    Args:
        topic: The news topic to search for (default: "latest news")
    
    Returns:
        str: Formatted news headlines and summaries.
    """
    try:
        # Use BBC RSS feed as it's more reliable for scraping
        if "san francisco" in topic.lower() or "sf" in topic.lower():
            url = "http://feeds.bbci.co.uk/news/world/us_and_canada/rss.xml"
        else:
            url = "http://feeds.bbci.co.uk/news/rss.xml"
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, verify=False, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item', limit=5)
        
        articles = []
        for item in items:
            title = item.find('title')
            description = item.find('description')
            link = item.find('link')
            
            if title:
                headline = title.text.strip()
                summary = description.text.strip() if description else 'No summary available'
                # Clean up HTML tags from summary
                summary = BeautifulSoup(summary, 'html.parser').get_text()
                
                # Filter articles that might be related to the topic
                if topic.lower() != "latest news":
                    if topic.lower() in headline.lower() or topic.lower() in summary.lower():
                        articles.append(f"• {headline}\n  {summary[:200]}...")
                else:
                    articles.append(f"• {headline}\n  {summary[:200]}...")
        
        if not articles:
            # Fallback: return all articles if no topic match
            for item in items:
                title = item.find('title')
                description = item.find('description')
                if title:
                    headline = title.text.strip()
                    summary = description.text.strip() if description else 'No summary available'
                    summary = BeautifulSoup(summary, 'html.parser').get_text()
                    articles.append(f"• {headline}\n  {summary[:200]}...")
        
        if not articles:
            return f"No news articles found for topic: {topic}"
            
        return f"Latest news about '{topic}':\n\n" + "\n\n".join(articles[:5])
        
    except Exception as e:
        return f"Error fetching news: {str(e)}"