import requests
from lxml.html import fromstring
from typing import Set


def get_proxies() -> Set:
    url = 'https://www.us-proxy.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()

    # Extract proxy string and add to the set
    for i in parser.xpath('//tbody/tr')[:60]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)

    # Up to 10 US proxies in the set
    return proxies
