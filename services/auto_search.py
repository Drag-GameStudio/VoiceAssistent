from .base import BaseService, classproperty
from ddgs import DDGS
from bs4 import BeautifulSoup
import requests

class AutoSearch(BaseService):

    def fast_search(self, query, max_results=5):
        try:
            with DDGS() as ddgs:
                results = [r for r in ddgs.text(query, max_results=max_results)]
            return {"status": "success", "data": results}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_page_content(self, url: str):
        """Заходит по ссылке и вытаскивает чистый текст."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Удаляем мусор: скрипты, стили, навигацию и футеры
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()
            
            # Собираем текст из заголовков и абзацев
            paragraphs = soup.find_all(['h1', 'h2', 'p'])
            text = "\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 20])
            
            return text[:2000]  # Ограничиваем объем для ассистента
        except Exception as e:
            return f"Ошибка при чтении страницы: {e}"

    def handle(self, query: str = None, link: str = None):
        if query is not None:
            print(query)
            result = self.fast_search(str(query))
        if link is not None:
            print(link)
            result = self.get_page_content(link)
        return result

    @classproperty
    def info(cls):
        return """
            This module can search any info in internet. use it if you need actual info
            requare key argument: 
            query - it is query that will be searching but it is requere only if you dont have link
            link - it is link if you want to see siteit is requere only if you dont have query
        """
    
    