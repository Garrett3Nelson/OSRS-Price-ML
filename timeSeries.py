from database import cur, con
from wikiAPI import pull_timeseries


def parse_time_data(itemID : int, data : dict):
    data_dict = sorted(data['data'], key = lambda i: i['timestamp'])

    # data format
    # {"timestamp":1656201300,"avgHighPrice":2,"avgLowPrice":2,"highPriceVolume":5198,"lowPriceVolume":9249},
    # (id integer, timestamp integer, avgHigh integer, avgLow integer, highVol integer, lowVol integer)

    for line in data_dict:
        if line['avgHighPrice'] == None: 
            avgHigh = 0 
        else: avgHigh = line['avgHighPrice']

        if line['avgLowPrice'] == None: 
            avgLow = 0 
        else: avgLow = line['avgLowPrice']

        if line['highPriceVolume'] == None: 
            highVol = 0 
        else: highVol = line['highPriceVolume']

        if line['lowPriceVolume'] == None: 
            lowVol = 0 
        else: lowVol = line['lowPriceVolume']

        if line['timestamp'] == None: 
            timestamp = 0 
        else: timestamp = line['timestamp']

        cur.execute("INSERT INTO timeseries VALUES ({id}, {timestamp}, {avgHigh}, {avgLow}, {highVol}, {lowVol})".format(id=itemID, timestamp=timestamp, avgHigh=avgHigh, avgLow=avgLow, highVol=highVol, lowVol=lowVol))   
        con.commit()

if __name__ == '__main__':
    for row in cur.execute("SELECT id FROM item_list"):
        parse_time_data(row[0], pull_timeseries(row[0]))
    con.close()