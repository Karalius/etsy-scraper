from fake_useragent import UserAgent
import pandas as pd
import numpy as np
import math
import time
from get_proxies import *
from replace_html_attributes import *


def scrape_etsy(keywords: list, items_to_scrape: int) -> pd.DataFrame:
    """
    This function scrapes www.etsy.com for the provided number of items for each of the keywords.
    It features rotating user-agents mirroring real agent, also rotating US proxies to avoid suspicion (bans).
    This function returns pandas dataframe with the collected information and requires items to scrape.

    :param keywords: list of keywords to scrape. Available keywords: painting, photography, prints.
    Constrain: up to 3 keywords in the list! Example: ['painting', 'photography', 'prints']
    :param items_to_scrape: integer of items to scrape for each keyword.
    For example: 3000 - every keyword in the keywords list will be scraped for 3000 items.
    :return: pandas dataframe from the scraped information.
    """

    average_items_per_page = 35
    pages_to_scrape = math.ceil(items_to_scrape / average_items_per_page)
    df_list = []
    # Define global to avoid error with local referencing
    global page
    # Define fake user agent
    ua = UserAgent(use_cache_server=False)
    for key in keywords:

        titles, prices, item_urls, img_urls = ([] for i in range(4))
        adj_keyword = key.lower()
        # Get new set of proxies for each keyword
        proxies_set = get_proxies()

        for page_no in range(1, pages_to_scrape + 1):
            proxies_to_iter = proxies_set

            for proxy in proxies_to_iter.copy():
                # Test if proxy works and get page html
                try:
                    headers = {
                        'authority': 'www.etsy.com',
                        'sec-ch-ua': '^\\^Google',
                        'sec-ch-ua-mobile': '?0',
                        'upgrade-insecure-requests': '1',
                        'user-agent': str(ua.random),
                        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'sec-fetch-site': 'same-origin',
                        'sec-fetch-mode': 'navigate',
                        'sec-fetch-user': '?1',
                        'sec-fetch-dest': 'document',
                        'referer': f'https://www.etsy.com/c/art-and-collectibles/{adj_keyword}?explicit=1&ship_to=US&ref=pagination&page={page_no - 1}',
                        'accept-language': 'en-US,en;q=0.9',
                    }
                    params = (
                        ('explicit', '1'),
                        ('ref', 'pagination'),
                        ('page', f'{page_no}'),
                    )
                    page = requests.get(
                        f"https://www.etsy.com/c/art-and-collectibles/{adj_keyword}?explicit=1&ship_to=US&ref=pagination&page={page_no}",
                        headers=headers,
                        params=params,
                        proxies={"http": str(proxy), "https": str(proxy)}
                    )
                except requests.exceptions.RequestException as e:
                    # Remove timed out proxy from the set
                    proxies_to_iter.discard(proxy)
                    continue
                else:
                    break

            soup = BeautifulSoup(page.content, 'html.parser')

            # Replace data-src to src attributes to stay consistent
            soup = replace_attr(page, 'data-src', 'src')

            for value in soup.find_all('div', class_=['js-merch-stash-check-listing']):
                # Discard trees with discount price
                if value.find(class_='strike-through'):
                    value.unwrap()

                # Extract and append to lists information on each item
                titles.extend(
                    [title.get('title') for title in value.find_all('a')]
                )
                prices.extend(
                    [float(price.get_text().replace(',', '')) for price in value.find_all(
                        'span', class_='currency-value')]
                )

                item_urls.extend(
                    [link.get('href') for link in value.find_all('a')]
                )
                img_urls.extend(
                    [pic.img['src'] for pic in value.find_all('div', class_='height-placeholder')]
                )

            #  Sleep anywhere from 0.4s to 1.2s
            time.sleep(np.random.uniform(0.4, 1.2))

        # Append dataframes of each keyword and limit length to items_to_scrape
        df_list.append(pd.DataFrame({
            'category': adj_keyword[:items_to_scrape],
            'title': titles[:items_to_scrape],
            'price': prices[:items_to_scrape],
            'item_url': item_urls[:items_to_scrape],
            'img_url': img_urls[:items_to_scrape]
        }))

    return pd.concat(df_list, ignore_index=True)
