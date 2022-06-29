import sqlite3
from config import DB_NAME
from wikiAPI import pull_mapping, pull_avg


def setup_connection():
    global con, cur
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()


def create_tables():
    cur.execute("CREATE TABLE item_list (id integer, name text, member integer, trade_lim integer)")
    cur.execute("CREATE TABLE timeseries (id integer, timestamp integer, avgHigh integer, avgLow integer, "
                "highVol integer, lowVol integer)")
    con.commit()


def populate_items():
    mapping_data = pull_mapping()
    volumes = pull_avg('1h')

    for line in mapping_data:
        if 'limit' not in line.keys():
            continue

        if str(line['id']) not in volumes.keys():
            print('{} not in volume data'.format(line['id']))
            continue

        item_volume = volumes[str(line['id'])]
        trade_volume = int(item_volume['lowPriceVolume']) + int(item_volume['highPriceVolume'])

        if trade_volume < line['limit']:
            print('{} does not have enough volume to add'.format(line['name']))
            continue

        cur.execute('''INSERT INTO item_list VALUES ({id}, "{name}", {member}, {trade_lim})'''.format(id=line['id'], name=line['name'], member=line['members'], trade_lim=line['limit']))   
        con.commit()


if __name__ == "__main__":
    setup_connection()
    create_tables()
    populate_items()
    con.close()
else:
    setup_connection()
