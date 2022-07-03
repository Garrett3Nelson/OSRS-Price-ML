from database import cur, con
from wikiAPI import pull_mapping, pull_avg, index_page_list, pull_index_page, parse_index_page


def populate_items():
    mapping_data = pull_mapping()
    volumes = pull_avg('24h')

    existing = [x for (x,) in cur.execute("SELECT name FROM item_list").fetchall()]
    for line in mapping_data:
        if 'limit' not in line.keys():
            continue

        if line['name'] in existing:
            continue

        if str(line['id']) not in volumes.keys():
            print('{} not in volume data'.format(line['id']))
            continue

        item_volume = volumes[str(line['id'])]
        trade_volume = int(item_volume['lowPriceVolume']) + int(item_volume['highPriceVolume'])

        if trade_volume < line['limit']:  # Based on the arbitrary limit of trading at least 1x trade limit per day
            print('{} does not have enough volume to add'.format(line['name']))
            continue

        cur.execute('''INSERT INTO item_list VALUES ({id}, "{name}", {member}, {trade_lim})'''.format(id=line['id'],
                                                                                                      name=line['name'],
                                                                                                      member=line[
                                                                                                          'members'],
                                                                                                      trade_lim=line[
                                                                                                          'limit']))
    con.commit()


def populate_categories():  # to use the market indices to find related items
    all_indices = index_page_list()

    for index_name, index_href in all_indices.items():
        item_names = parse_index_page(pull_index_page(index_name))

        for item in item_names:
            # chose not to put a check for existing item in item_list so it doesn't need re-running if I add more items
            cur.execute('''INSERT INTO categories VALUES ("{item_name}", "{category}")'''.format(item_name=item,
                                                                                                 category=index_name))

    con.commit()
