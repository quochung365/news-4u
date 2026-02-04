url = [
    'https://vnexpress.net/sieu-tau-san-bay-13-ty-usd-gap-nhieu-trac-tro-cua-my-5011913.html',
    'https://vnexpress.net/ong-medvedev-ca-ngoi-ong-trump-5012568.html/',
    'https://techcrunch.com/2026/02/01/why-tethers-ceo-is-everywhere-right-now/'
]


def get_slug(url) -> str:
    url_parts = url.split('/')
    if len(url_parts) < 0:
        return ''
    if url_parts[-1] == '':
        return url_parts[-2].replace('.html', '')



    return url_parts[-1].replace('.html', '')

for u in url:
    print(get_slug(u))
  