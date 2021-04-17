# Scrape-etsy v1.0

This scraper is based on https://www.etsy.com/c/art-and-collectibles. Currently, it can scrape the following keywords:
* prints
* drawing-and-illustration
* painting
* collectibles
* photography
* sculpture
* dolls-and-miniatures
* fiber-arts
* fine-art-ceramics
* mixed-media-and-college
* glass-art
* artist-tradings-cards

From the main scraping function you will receive the following output (```df``` column names):
* Category

* Title

* Price (USD)

* URL to the item

* URL to the image of the item.

## Feature
There is an implemented option to connect to your ```Heroku Postgres Database``` and store the scraped data in format of ```two tables```.
Call a function in order to receive a ```etsy_data.csv``` with merged tables. See more in the 'Usage example' section.

## Installation
```
git clone git@github.com:Karalius/Scrape-etsy.git
pip install -r requirements.txt
cd scrape_etsy
pip install
```

## Usage example
**Scraper with 100 items to scrape:**
```
from scraper import scrape_etsy

df = scrape_etsy(
    ['dolls-and-miniatures', 'photography', 'prints', 'mixed-media-and-collage'],
    100
)
```
How does the ```df``` look like?

![Scraped Dataframe 'df'](https://i.imgur.com/iW0EWHm.jpg)

**Heroku**:

Firstly define your ```Heroku Postgres``` credentials in the ```heroku_credentials.py``` file.

We will use the same ```df```, which is defined above, to push the dataframe to ```Heroku Postgres``` database.
```
from heroku_n_csv import push_to_heroku

push_to_heroku(df)
```

**Get csv to your provided path! In this case, we use the desktop as our location:**
```
from heroku_n_csv import get_csv

get_csv('c:\Users\(username)\Desktop')
```

For the deeper understanding of the functions, please refer to the ```dosctrings``` of the package.

## Notebook

In case you do not want to use this scraper locally, you may use the existing ```scraping_notebook.ipynb``` in this repository.







