import requests
from lxml.html import fromstring
from typing import Set


def get_proxies() -> Set:
    """
    This function fetches html from the www.us-proxy.org website and iterates through it.
    While iterating it collects IP addresses and ports, then joins them to form a string.

    :return: a set of strings containing proxies based in the US.
    """
    url = 'https://www.us-proxy.org/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()

    # Form a string from IP address and port, then add to the set
    for i in parser.xpath('//tbody/tr')[:60]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)

    return proxies
