# Scrape Etsy

![Scraper Etsy](https://i.imgur.com/MuGjvmF.png)

This scraper works on [Etsy](https://www.etsy.com/c/art-and-collectibles) E-Commerce shop. Currently, it can scrape the following keywords:

![Keywords](https://i.imgur.com/zGYu5UI.jpg)

## Features
There is an implemented option to connect to your ```Heroku Postgres Database``` and store the scraped data in format of ```two tables```.
Call a function in order to receive a ```etsy_data.csv``` with merged tables. See more in the 'Usage example' section.

## Installation
```
git clone git@github.com:Karalius/Scrape-etsy.git
pip install -r requirements.txt
cd scrape_etsy
pip install
```

## Example
**Scraper with 400 items to scrape:**
```python
from scraper import scrape_etsy

df = scrape_etsy(
    ['dolls-and-miniatures', 'photography', 'prints', 'mixed-media-and-collage'], 400
)
```
How does the ```df``` look like?

![Scraped Dataframe 'df'](https://i.imgur.com/iW0EWHm.jpg)

**Heroku**:

Firstly define your ```Heroku Postgres``` credentials in the ```scrape_etsy/heroku_credentials.py``` file.

We will use the same ```df```, which is defined above, to push the dataframe to ```Heroku Postgres``` database.
```python
from heroku_n_csv import push_to_heroku

push_to_heroku(df)
```

**Get csv to your provided path! In this case, we use the desktop as our location:**
```python
from heroku_n_csv import get_csv

get_csv('c:\Users\(username)\Desktop')
```

For the deeper understanding of the functions, please refer to the ```dosctrings``` of the package.

## Notebook

In case you do not want to use this scraper locally, you may use the existing ```scraping_notebook.ipynb``` in this repository.







