from database import cur, con
from wikiAPI import pull_timeseries
from datetime import datetime


def parse_time_data(item_id: int, data: list):
    # data format
    # {"timestamp":1656201300,"avgHighPrice":2,"avgLowPrice":2,"highPriceVolume":5198,"lowPriceVolume":9249},
    # (id integer, timestamp integer, avgHigh integer, avgLow integer, highVol integer, lowVol integer)

    for line in data:
        timestamp = line['timestamp']

        if line['avgHighPrice'] is None:
            avg_high = 0
        else:
            avg_high = line['avgHighPrice']

        if line['avgLowPrice'] is None:
            avg_low = 0
        else:
            avg_low = line['avgLowPrice']

        if line['highPriceVolume'] is None:
            high_vol = 0
        else:
            high_vol = line['highPriceVolume']

        if line['lowPriceVolume'] is None:
            low_vol = 0
        else:
            low_vol = line['lowPriceVolume']

        cur.execute(
            "INSERT INTO timeseries VALUES ({id}, {timestamp}, {avgHigh}, {avgLow}, {highVol}, {lowVol})".format(
                id=item_id, timestamp=timestamp, avgHigh=avg_high, avgLow=avg_low, highVol=high_vol, lowVol=low_vol))
        con.commit()


def get_last_timestamps():
    latest = cur.execute('SELECT id, max(timestamp) FROM timeseries GROUP BY id').fetchall()
    return {k: v for (k, v) in latest}


def snip_data(last_timestamp: int, data: dict):
    data_dict = sorted(data['data'], key=lambda i: i['timestamp'])

    for time, line in enumerate(data_dict):
        if line['timestamp'] is not None:
            if line['timestamp'] > last_timestamp:
                # print('Old len {old}, new len {new}'.format(old=len(data_dict), new=len(data_dict[i:])))
                return data_dict[time:]


if __name__ == '__main__':
    print("({}) Starting timeseries script".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    last_timestamps = get_last_timestamps()
    rows = cur.execute('SELECT id FROM item_list').fetchall()
    # print('Timeseries for {} items'.format(len(rows)))

    for row in rows:
        # print('Parsing for {}'.format(row[0]))
        if row[0] in last_timestamps.keys():
            new_data = snip_data(last_timestamps[row[0]], pull_timeseries(row[0]))
        else:
            data = pull_timeseries(row[0])
            new_data = sorted(data['data'], key=lambda i: i['timestamp'])

        if new_data is None:
            continue
        parse_time_data(row[0], new_data)

    con.close()
    print("({}) Completed timeseries script".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
