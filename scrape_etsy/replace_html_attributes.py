from bs4 import BeautifulSoup
import requests


def replace_attr(html_doc: requests.models.Response, from_attr: str, to_attr: str) -> BeautifulSoup:
    soup = BeautifulSoup(html_doc.content, 'html.parser')
    tags = soup(attrs={from_attr: True})

    # Replace tags with new tag
    for tag in tags:
        tag[to_attr] = tag[from_attr]
        del tag[from_attr]

    return soup
