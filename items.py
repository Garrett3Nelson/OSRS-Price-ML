from database import cur, con
from wikiAPI import pull_mapping, pull_avg, index_page_list, pull_index_page, parse_index_page


def populate_items():
    mapping_data = pull_mapping()
    volumes = pull_avg('24h')

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

        cur.execute('''INSERT INTO item_list VALUES ({id}, "{name}", {member}, {trade_lim})'''.format(id=line['id'],
                                                                                                      name=line['name'],
                                                                                                      member=line[
                                                                                                          'members'],
                                                                                                      trade_lim=line[
                                                                                                          'limit']))
        con.commit()


def populate_categories():  # to use the market indices to find related items
    all_indices = index_page_list()

    item_dict = {}
    for index_name, index_href in all_indices.items():
        item_names = parse_index_page(pull_index_page(index_name))

        for item in item_names:
            if item in item_dict.keys():
                item_dict[item].append(index_name)
            else:
                item_dict[item] = [index_name]

    return item_dict


# TODO: Match item names with item_id in the database
# TODO: Create a new table to track all indices for items and populate
if __name__ == '__main__':
    pass
