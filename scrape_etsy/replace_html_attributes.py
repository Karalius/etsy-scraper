from bs4 import BeautifulSoup
import requests


def replace_attr(
    html_doc: requests.models.Response, from_attr: str, to_attr: str
) -> BeautifulSoup:
    """
    Function takes the arguments explained below and returns edited html page with new tags

    :param html_doc: takes a response page, for example: requests.get(url)
    :param from_attr: give a tag name which meant to be changed, for example: 'data-src'
    :param to_attr: give a tag name which should replace from_attr, for example: 'src'
    :return: returns response page with new tag name in the html
    """

    soup = BeautifulSoup(html_doc.content, "html.parser")
    tags = soup(attrs={from_attr: True})

    # Replace tags with new tag
    for tag in tags:
        tag[to_attr] = tag[from_attr]
        del tag[from_attr]

    return soup
