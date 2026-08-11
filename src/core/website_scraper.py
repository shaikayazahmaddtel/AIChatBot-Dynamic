"""
Website Scraper for Dynamic Content Extraction
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Set
import time

class WebsiteScraper:
    def __init__(self):
        self.visited_urls: Set[str] = set()
        self.content: List[str] = []
    
    def scrape_website(self, url: str, max_pages: int = 50) -> str:
        """Scrape website content"""
        try:
            self.visited_urls.clear()
            self.content.clear()
            
            base_domain = urlparse(url).netloc
            self._scrape_page(url, base_domain, max_pages)
            
            return "\n\n".join(self.content)
        except Exception as e:
            print(f"Scraping error: {e}")
            return ""
    
    def _scrape_page(self, url: str, base_domain: str, max_pages: int):
        """Recursively scrape pages"""
        if len(self.visited_urls) >= max_pages or url in self.visited_urls:
            return
        
        self.visited_urls.add(url)
        
        try:
            response = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; ChatbotBot/1.0)'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header']):
                element.decompose()
            
            # Extract main content
            main_content = soup.find('main') or soup.find('article') or soup.body
            if main_content:
                text = main_content.get_text(separator='\n', strip=True)
                self.content.append(f"URL: {url}\n{text}")
            
            # Find and follow links
            for link in soup.find_all('a', href=True):
                href = urljoin(url, link['href'])
                if urlparse(href).netloc == base_domain:
                    if len(self.visited_urls) < max_pages:
                        time.sleep(0.1)  # Be respectful
                        self._scrape_page(href, base_domain, max_pages)
                        
        except Exception as e:
            print(f"Error scraping {url}: {e}")
