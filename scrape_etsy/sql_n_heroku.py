import os
import psycopg2
from sqlalchemy import create_engine
from main_scrape import *
from heroku_credentials import *


def push_to_heroku(df: pd.DataFrame) -> None:
    # Heroku connection
    sql_connection = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    # Connect to DB
    cur = sql_connection.cursor()

    # Create two SQL tables
    cur.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id serial PRIMARY KEY,
        category varchar(250)
    );

    CREATE TABLE IF NOT EXISTS items (
        id serial PRIMARY KEY,
        category_id int,
        title varchar(250),
        price float(2),
        item_url varchar(500),
        img_url varchar(500),
        FOREIGN KEY (category_id) REFERENCES categories(id)
    );

    ''')
    # Get array of unique category names
    unique_categories = df['category'].unique()

    # Insert unique category names to the categories table
    for i in unique_categories:
        cur.execute(f"INSERT INTO categories (category) VALUES ('{i}');")

    # Commit and close connection
    sql_connection.commit()
    sql_connection.close()

    # Create category id for each category
    foreign_key_df = pd.DataFrame(df['category'].unique(), columns=['category']).reset_index().rename(
        columns={'index': 'category_id'})
    foreign_key_df['category_id'] = np.arange(1, len(foreign_key_df) + 1)

    # Make a dataframe only with category id
    items_df = pd.merge(
        df,
        foreign_key_df,
        on='category'
    ).drop(columns='category')

    # Put category id as first column
    items_df.insert(0, 'category_id', items_df.pop('category_id'))

    # Connect to Heroku Postgres
    conn = create_engine(POSTGRES_URI)

    # Push items df to Heroku DB
    items_df.to_sql('items', conn, method='multi', if_exists='append', chunksize=10000, index=False)

    conn.dispose()


def get_csv(path: str) -> None:
    # Heroku connection
    sql_connection = psycopg2.connect(
        database=DATABASE,
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT
    )
    # Connect to DB
    cur = sql_connection.cursor()

    # Join tables on category id
    s = "SELECT items.id, categories.category, items.title, items.price, items.item_url, items.img_url" \
        "FROM items JOIN categories ON categories.id = items.category_id ORDER BY id ASC"

    # COPY function on the SQL we created above.
    sql_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)

    # Set up a variable to store our file path and name
    t_path_n_file = os.path.join(path, "etsy_data.csv")

    # Create and save csv of etsy data
    with open(t_path_n_file, 'w') as f_output:
        cur.copy_expert(sql_for_file_output, f_output)

    sql_connection.close()

