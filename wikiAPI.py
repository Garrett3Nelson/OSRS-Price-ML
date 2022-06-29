import requests
import config

BASE_URL = 'https://prices.runescape.wiki/api/v1/osrs/'

def api_request(request_type : str, itemID : int = 0):
    url_options = {
        'timeseries' : 'timeseries?timestep=5m&id={}'.format(itemID),
        'timeseries_1h' : 'timeseries?timestep=1h&id={}'.format(itemID),
        'latest' : 'latest',
        'mapping' : 'mapping',
        '5m' : '5m',
        '1h' : '1h'
    }

    request_url = url_options[request_type]
    
    url = BASE_URL + request_url

    headers = {
        'User-Agent': config.USER_AGENT,
    }

    return requests.get(url, headers=headers)


def pull_latest():
    response = api_request('latest')

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()


def pull_mapping():
    response = api_request('mapping')

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()


def pull_timeseries(itemID):
    response = api_request('timeseries', itemID)

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()


def pull_avg(interval : str):
    if interval not in ['1h', '5m']:
        print('Incorrect argument')
        return
    
    response = api_request(interval)

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()['data']
