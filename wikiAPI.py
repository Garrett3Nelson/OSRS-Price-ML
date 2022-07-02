import requests
import config

from bs4 import BeautifulSoup
BASE_URL = 'https://prices.runescape.wiki/api/v1/osrs/'


def api_request(request_type: str, interval: str = '5m', item_id: int = 0):
    url_options = {
        'timeseries': 'timeseries?timestep={interval}&id={id}'.format(id=item_id, interval=interval),
        'latest': 'latest',
        'mapping': 'mapping',
        'prices': interval  # Summary of all items
    }

    request_url = url_options[request_type]
    
    url = BASE_URL + request_url

    headers = {
        'User-Agent': config.USER_AGENT
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


def pull_timeseries(item_id: int, interval: str = '5m'):
    response = api_request('timeseries', interval, item_id)

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()


def pull_avg(interval: str):
    response = api_request(interval)

    if response.status_code != 200:
        raise requests.exceptions.RequestException
    
    return response.json()['data']


def index_page_list():
    full_list = {
        "Common Trade Index": "/Common_Trade_Index",
        "Rune Index": "/Rune_Index",
        "Log Index": "/Log_Index",
        "Food Index": "/Food_Index",
        "Metal Index": "/Metal_Index",
        "Herb Index": "/Herb_Index",
        "High Trade Volume Index": "/High_Trade_Volume_Index",
        "Alchemical Hydra Index": "/Alchemical_Hydra_Index",
        "Barrows Index": "/Barrows_Index",
        "Bryophyta Index": "/Bryophyta_Index",
        "Callisto Index": "/Callisto_Index",
        "Cerberus Index": "/Cerberus_Index",
        "Chaos Elemental Index": "/Chaos_Elemental_Index",
        "Chaos Fanatic Index": "/Chaos_Fanatic_Index",
        "Commander Zilyana Index": "/Commander_Zilyana_Index",
        "Corporeal Beast Index": "/Corporeal_Beast_Index",
        "Crazy archaeologist Index": "/Crazy_archaeologist_Index",
        "Dagannoth Kings Index": "/Dagannoth_Kings_Index",
        "Deranged Archaeologist Index": "/Deranged_Archaeologist_Index",
        "General Graardor Index": "/General_Graardor_Index",
        "Giant Mole Index": "/Giant_Mole_Index",
        "Grotesque Guardians Index": "/Grotesque_Guardians_Index",
        "Hespori Index": "/Hespori_Index",
        "Kalphite Queen Index": "/Kalphite_Queen_Index",
        "King Black Dragon Index": "/King_Black_Dragon_Index",
        "Kraken Index": "/Kraken_Index",
        "Kree'arra Index": "/Kree%27arra_Index",
        "K'ril Tsutsaroth Index": "/K%27ril_Tsutsaroth_Index",
        "The Mimic Index": "/The_Mimic_Index",
        "Nex Index": "/Nex_Index",
        "The Nightmare Index": "/The_Nightmare_Index",
        "Obor Index": "/Obor_Index",
        "Scorpia Index": "/Scorpia_Index",
        "Skotizo Index": "/Skotizo_Index",
        "Sarachnis Index": "/Sarachnis_Index",
        "Thermonuclear smoke devil Index": "/Thermonuclear_smoke_devil_Index",
        "Venenatis Index": "/Venenatis_Index",
        "Vet'ion Index": "/Vet%27ion_Index",
        "Vorkath Index": "/Vorkath_Index",
        "Zulrah Index": "/Zulrah_Index",
        "Chambers of Xeric Index": "/Chambers_of_Xeric_Index",
        "Theatre of Blood Index": "/Theatre_of_Blood_Index",
        "Construction": "/Construction",
        "Construction flatpacks": "/Construction_flatpacks",
        "Cooking": "/Cooking",
        "Crafting": "/Crafting",
        "Farming": "/Farming",
        "Firemaking": "/Firemaking",
        "Fishing": "/Fishing",
        "Fletching": "/Fletching",
        "Herblore": "/Herblore",
        "Hunter": "/Hunter",
        "Magic": "/Magic",
        "Melee armour": "/Melee_armour",
        "Melee weapons": "/Melee_weapons",
        "Mining": "/Mining",
        "Prayer": "/Prayer",
        "Ranged": "/Ranged",
        "Runecraft": "/Runecraft",
        "Slayer": "/Slayer",
        "Smithing": "/Smithing",
        "Woodcutting": "/Woodcutting",
        "Treasure Trails": "/Treasure_Trails",
        "God Wars Dungeon": "/God_Wars_Dungeon",
        "Minigames": "/Minigames",
        "Combat minigames": "/Combat_minigames",
        "Seasonal": "/Seasonal",
        "Raids": "/Raids",
        "Most traded": "/Most_traded",
        "Most expensive": "/Most_expensive",
        "Alchemy": "/Alchemy",
        "General Store": "/General_Store",
        "Clothes": "/Clothes",
        "Item sets": "/Item_sets",
        "Potions": "/Potions",
        "Miscellaneous": "/Miscellaneous"
    }

    return full_list


def pull_index_page(index_page: str):
    request_options = index_page_list()

    request_url = request_options[index_page]
    url = 'https://oldschool.runescape.wiki/w/RuneScape:Grand_Exchange_Market_Watch/' + request_url + '#a=30'

    headers = {
        'User-Agent': config.USER_AGENT
    }

    return requests.get(url, headers=headers)


def parse_index_page(index_page):  # Pulls item names from the indices
    soup = BeautifulSoup(index_page.text, 'lxml')

    item_names = []
    tables = soup.find_all('table')  # all rows are indicated with <tr> tags
    for table in tables:
        if 'wikitable' in table.get('class'):
            table_rows = table.find_all('tr')
            for row in table_rows:
                columns = row.find_all('td')  # all normal columns are <td> and the headers are <th>

                if columns is None:  # will be none if we're on a header
                    continue

                if len(columns) < 2:  # some hidden <tr> segments are just the one column
                    continue

                item_names.append(columns[1].get_text())  # The first column is an icon, second is the name

    return item_names
