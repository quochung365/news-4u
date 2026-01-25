# summarize it in 30-100 words (you can use bullet points if needed, but prioritize non-bullet points). Try to make it as concise as possible
import trafilatura
import time
import logging
import httpx


logging.basicConfig(level=logging.DEBUG)
def get_news(url):
    # Step 1: Extract content using trafilatura
    start_time = time.time()

    downloaded = trafilatura.fetch_url(url)

    article_text = trafilatura.extract(downloaded, with_metadata=True)
    trafilatura.load_download_buffer()
    

    with open('./out', 'w+') as f:
        f.write("MAIN_CONTENT\n")
        f.write(f"{article_text}\n")
    with open('./downloaded', 'w+') as f:
        f.write("MAIN_CONTENT\n")
        f.write(f"{downloaded}\n")

    # Operations on the file_object (read, write, etc.)
        pass

    if not article_text:
        return "Could not extract text from the provided URL."

    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")

    return article_text

if __name__ == "__main__":
    # input_url = input("Enter the URL of the article: ")
    # get_news(input_url)
    from curl_cffi import requests
    url = 'https://vnexpress.net/hlv-tuyen-thai-lan-cau-thu-cua-chung-toi-co-tiem-nang-hon-viet-nam-5009773.html'

    # 'impersonate' makes the TLS handshake look exactly like Chrome
    r = requests.get(url, impersonate="chrome120")

    print(r.status_code)

    article_text = trafilatura.extract(r.content)
    with open('./out', 'w+') as f:
        f.write("MAIN_CONTENT\n")
        f.write(f"{article_text}\n")

    # url = 'https://www.kxan.com/news/texas-politics/crockett-vs-talarico-democratic-us-senate-candidates-set-to-debate-on-saturday/'

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Language': 'en-US,en;q=0.9',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Connection': 'keep-alive',
    #     'Upgrade-Insecure-Requests': '1',
    #     'Sec-Fetch-Dest': 'document',
    #     'Sec-Fetch-Mode': 'navigate',
    #     'Sec-Fetch-Site': 'none',
    #     'Sec-Fetch-User': '?1',
    #     'Cache-Control': 'max-age=0',
    # }

    # with httpx.Client(http2=True) as client:
    #     r = client.get(url, headers=headers)
    #     print(r.status_code)