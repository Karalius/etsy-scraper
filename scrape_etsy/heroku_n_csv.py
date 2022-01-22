import os
import psycopg2
from sqlalchemy import create_engine
from scraper import *
from heroku_credentials import *


def push_to_heroku(df: pd.DataFrame) -> None:
    """
    Functions takes a dataframe as an argument, then connects to a Heroku Postgres database.
    In the database it creates two tables pushes the information into both of them.

    :param df: Takes a pandas dataframe.
    :return: None, data sits on Heroku Postgres database.
    """
    sql_connection = psycopg2.connect(
        database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    cur = sql_connection.cursor()

    cur.execute(
        """
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

    """
    )
    unique_categories = df["category"].unique()

    for i in unique_categories:
        cur.execute(f"INSERT INTO categories (category) VALUES ('{i}');")

    sql_connection.commit()
    sql_connection.close()

    foreign_key_df = (
        pd.DataFrame(df["category"].unique(), columns=["category"])
        .reset_index()
        .rename(columns={"index": "category_id"})
    )
    foreign_key_df["category_id"] = np.arange(1, len(foreign_key_df) + 1)

    items_df = pd.merge(df, foreign_key_df, on="category").drop(columns="category")

    items_df.insert(0, "category_id", items_df.pop("category_id"))
    conn = create_engine(POSTGRES_URI)
    items_df.to_sql(
        "items", conn, method="multi", if_exists="append", chunksize=10000, index=False
    )
    conn.dispose()


def get_csv(path: str) -> None:
    """
    This functions takes a path as an argument as saves the etsy_data.csv file in provided local directory.

    :param path: Provide a path where to save a csv file.
    :return: None, csv file saved in the local directory.
    """
    sql_connection = psycopg2.connect(
        database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT
    )
    cur = sql_connection.cursor()

    s = (
        "SELECT items.id, categories.category, items.title, items.price, items.item_url, items.img_url"
        "FROM items JOIN categories ON categories.id = items.category_id ORDER BY id ASC"
    )

    sql_for_file_output = "COPY ({0}) TO STDOUT WITH CSV HEADER".format(s)
    t_path_n_file = os.path.join(path, "etsy_data.csv")
    with open(t_path_n_file, "w") as f_output:
        cur.copy_expert(sql_for_file_output, f_output)
    sql_connection.close()
