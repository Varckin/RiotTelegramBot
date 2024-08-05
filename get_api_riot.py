import requests
from resources.API_KEY import api_key
import json


def get_id_player(gamename_to_puuid: str = None, puuid_to_gamename: str = None, puuid_to_summonerID: str = None, summonerID_to_puuid: str = None, server: str = None, boollevelsumm: bool = False):
    if gamename_to_puuid:
        name, tag = gamename_to_puuid.split('#')
        url = f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={api_key}'

        response = requests.get(url)
        data = response.json()
        return data['puuid']
    if puuid_to_gamename:
        url = f'https://{server}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid_to_gamename}?api_key={api_key}'

        response = requests.get(url)
        data = response.json()
        return f'{data['gameName']}#{data['tagLine']}'
    if puuid_to_summonerID:
        url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid_to_summonerID}?api_key={api_key}'

        response = requests.get(url)
        data = response.json()

        if boollevelsumm:
            return data['id'], data['summonerLevel']
        else:
            return data['id']
        
    if summonerID_to_puuid:
            url = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/{summonerID_to_puuid}?api_key={api_key}'

            response = requests.get(url)
            data = response.json()

            return data['puuid']
    

def get_ranked_info(summonerID: str, server: str):
    url = f'https://{server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summonerID}?api_key={api_key}'

    response = requests.get(url)
    data = response.json()
    list_rank = []

    if not data:
        return 'Unranked'
    else:
        for dict_rank in data:
            rank = {'queueType': dict_rank['queueType'],
                    'tier': dict_rank['tier'],
                    'rank': dict_rank['rank'],
                    'leaguePoints': dict_rank['leaguePoints'],
                    'wins': dict_rank['wins'],
                    'losses': dict_rank['losses']
                    }
            list_rank.append(rank)
        return list_rank

    
def get_champion_masteries_sum(puuid: str, server: str, count: int = 3):
    url = f'https://{server}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}/top?count={count}&api_key={api_key}'

    response = requests.get(url)
    data = response.json()

    champ_master = []
    if data:
        for masteries in data:
            dict_champ_master = {
                'championId': masteries['championId'],
                'championLevel': masteries['championLevel'],
                'championPoints': masteries['championPoints'],
            }
            champ_master.append(dict_champ_master)

    return champ_master

def get_best_players_region(queue_rank: str, server: str, tier_rank: str):
    url = f'https://{server}.api.riotgames.com/lol/league/v4/{tier_rank}/by-queue/{queue_rank}?api_key={api_key}'

    response = requests.get(url)
    data = response.json()
    entries = sorted(data['entries'], key=lambda x: x['leaguePoints'], reverse=True)

    full_text = ''
    i = 1
    for entry in entries:
        if i == 51:
            break
        else:
            print(i)
        
        text = f'''
{i} Игрок: {get_id_player(puuid_to_gamename=get_id_player(summonerID_to_puuid=entry['summonerId'], server='ru'), server='europe')}
Поинтов: {entry['leaguePoints']}
Вин/Луз: {entry['wins']}/{entry['losses']}

        '''
        i += 1
        full_text += text

    return full_text


def get_info_champ(lang: str, version_game: str, name_champ: str):
    url = f'https://ddragon.leagueoflegends.com/cdn/{version_game}/data/{lang}/champion.json'

    response = requests.get(url)
    data = response.json()
    list_champions = data['data']
    info_champ = list_champions[name_champ]
    dict_info_champ = {
        'name_champion': info_champ['name'],
        'title_champion': info_champ['title'],
        'description_champion': info_champ['blurb'],
        'tag_champion': info_champ['tags'],
        'url_image_champion': f'https://ddragon.leagueoflegends.com/cdn/{version_game}/img/champion/{info_champ['image']['full']}'
    }
    return dict_info_champ


def full_info_player(gamename: str, server: str):
    puuid = get_id_player(gamename_to_puuid=gamename)
    summonerID, summonerLevel = get_id_player(puuid_to_summonerID=puuid, server=server, boollevelsumm=True)

    ranks = get_ranked_info(summonerID, server)
    champion_masteries = get_champion_masteries_sum(puuid, server)

    rank_text = ''
    master_text = ''
    
    if isinstance(ranks, list):
        for rank in ranks:
            text = f'''
Rank: {rank['queueType']}
{rank['tier']} {rank['rank']}
Point: {rank['leaguePoints']}
Win: {rank['wins']} Losses: {rank['losses']}
'''
            rank_text +=text
    else:
        rank_text += ranks
        return rank_text

    if isinstance(champion_masteries, list):
        for masteries in champion_masteries:
            text = f'''
Champion: {get_from_key_to_name_champion(str(masteries['championId']))}
Level masteries: {masteries['championLevel']}
Point masteries: {masteries['championPoints']}
'''
            master_text +=text
    else:
        return master_text

    full_info = f"""
Game name: {gamename} (Level: {summonerLevel})
{rank_text}
Champion masteries:
{master_text}
"""
    return full_info


def get_from_key_to_name_champion(id: str):
    with open('resources/champion_info.json', 'r') as file:
        champ_info = json.load(file)

    for name, champ in champ_info['data'].items():
        if champ['key'] == id:
            return champ['name']
