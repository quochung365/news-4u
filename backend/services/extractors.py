from trafilatura import fetch_url, extract
from models import NewsArticle
from curl_cffi import requests
'''
- For each NewsArticle
    - download the html page; if cannot download -> throw proper exception and update metric
    - if the image_url is not found in the db -> extract it from the downloaded html
    - extract the main content using trafilatura.extract
    - return
'''
class Extractor:
    def __init__(self):
        downloaded_html = None

        pass

    def download_page(self, url):
        downloaded = fetch_url(url)
        downloaded = requests.get(url, impersonate="chrome120")


        if not downloaded:
            # throw exception; update mertics
            log.error


        self.downloaded_url = downloaded


    def extract(self, article: NewsArticle):
        
        return extract(fetch_url(url))

    def extract_with_comments(self, url: str) -> str:
        return extract(fetch_url(url), with_comments=True)

    def has_main_image(article: NewsArticle):
        return article.image_url != None
