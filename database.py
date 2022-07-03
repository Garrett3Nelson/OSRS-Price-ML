import sqlite3
from config import DB_NAME


def setup_connection():
    global con, cur
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE item_list (id integer, name text, member integer, trade_lim integer)")
    cur.execute("CREATE TABLE timeseries (id integer, timestamp integer, avgHigh integer, avgLow integer, "
                "highVol integer, lowVol integer)")
    cur.execute("CREATE TABLE categories (name text, category text)")
    con.commit()


if __name__ == "__main__":
    setup_connection()
    create_tables()
    con.close()
else:
    setup_connection()
