import logging
from typing import Optional
from trafilatura import fetch_url, extract
from models import NewsArticle
from curl_cffi import requests
from exceptions import DownloadException
from bs4 import BeautifulSoup

'''
- For each NewsArticle
    - download the html page; if cannot download -> throw proper exception and update metric
    - if the image_url is not found in the db -> extract it from the downloaded html
    - extract the main content using trafilatura.extract
    - return
    
'''

logger = logging.getLogger(__name__)
class Extractor:
    def __init__(self):
        pass

    def download_page(self, url):
        downloaded = fetch_url(url)
        downloaded = requests.get(url, impersonate="chrome120")

        if not downloaded or not downloaded.text:
            logger.error(f"Failed to download page: {url}")
            raise DownloadException(url)
            # throw exception; update mertics
        return downloaded.text

    def extract_from_url(self, url):
        """ TestOnly: Extract content and main image from a given URL without using the NewsArticle model. """
        try:
            downloaded_html = self.download_page(url)
            main_image = self.extract_main_image(downloaded_html, NewsArticle(link=url))
            content = self.extract_content(downloaded_html, NewsArticle(link=url))
            return content, main_image

        except DownloadException:
            logger.error(f"Failed to download page: {url}")
            return None, None

    def extract(self, article: NewsArticle):
        url = article.link
        try:
            downloaded_html = self.download_page(url)
            main_image = self.extract_main_image(downloaded_html, article)
            content = self.extract_content(downloaded_html, article)
            return content, main_image

        except DownloadException:
            article.retry_count += 1
            logger.error(f"Failed to download page: {url}")
            return None, None

        

    def extract_main_image(self, html_content: str, article: NewsArticle):
        # Simple heuristic to find the main image from the HTML content
        # In real scenarios, you might want to use more sophisticated methods
        if article.image_url and article.image_url != "":
            return None  # Image URL already exists

        soup = BeautifulSoup(html_content, 'html.parser')
        # Look for og:image meta tag
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            article.image_url = og_image["content"]
            return article.image_url

        # Fallback: find the first <img> tag in the content
        first_img = soup.find("img")
        if first_img and first_img.get("src"):
            article.image_url = first_img["src"]
            return article.image_url

        return None

    def extract_content(self, downloaded_html: str, article: NewsArticle):
        content = extract(downloaded_html)
        if content:
            article.content = content
        return content
