import feedparser
from bs4 import BeautifulSoup

feed = feedparser.parse('https://techcrunch.com/feed/')
for entry in feed.entries:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Summary: {entry.summary}")
    print(f"Published: {entry.published}")
    print(f"Published: {entry.description}")
    print("-----")


# print(len(feed.entries))  # Number of entries parsed
# print(feed.bozo)  # Should be 0 if no parsing errors occurred
# # print(feed.feed.title)  # Title of the feed
# print(feed.headers)  # Description of the feed
# print(feed.feed.link)   # Link to the feed
# print(feed.feed.description)   # Description of the feed
# print(feed.feed.updated)   # Last updated time of the feed
# print(feed.feed.description_detail)


# {'title': 'TechCrunch', 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://techcrunch.com/feed/', 'value': 'TechCrunch'}, 'links': [{'href': 'https://techcrunch.com/feed/', 'rel': 'self', 'type': 'application/rss+xml'}, {'rel': 'alternate', 'type': 'text/html', 'href': 'https://techcrunch.com/'}], 'link': 'https://techcrunch.com/', 'subtitle': 'Startup and Technology News', 'subtitle_detail': {'type': 'text/html', 'language': None, 'base': 'https://techcrunch.com/feed/', 'value': 'Startup and Technology News'}, 'updated': 'Sat, 31 Jan 2026 18:10:22 +0000', 'updated_parsed': time.struct_time(tm_year=2026, tm_mon=1, tm_mday=31, tm_hour=18, tm_min=10, tm_sec=22, tm_wday=5, tm_yday=31, tm_isdst=0), 'language': 'en-US', 'sy_updateperiod': 'hourly', 'sy_updatefrequency': '1', 'generator_detail': {'name': 'https://wordpress.org/?v=6.9'}, 'generator': 'https://wordpress.org/?v=6.9', 'image': {'href': 'https://techcrunch.com/wp-content/uploads/2015/02/cropped-cropped-favicon-gradient.png?w=32', 'title': 'TechCrunch', 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'https://techcrunch.com/feed/', 'value': 'TechCrunch'}, 'links': [{'rel': 'alternate', 'type': 'text/html', 'href': 'https://techcrunch.com/'}], 'link': 'https://techcrunch.com/', 'width': 32, 'height': 32}}