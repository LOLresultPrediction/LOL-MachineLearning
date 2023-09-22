import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)
api_key = 'RGAPI-8cbea5e9-d29f-4e88-9bab-18310abbc7cd'
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-8cbea5e9-d29f-4e88-9bab-18310abbc7cd"
}

# 유저 puuid 가져오기
def match_v5_get_list_puuid(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?{api_key}"
    return requests.get(url, headers=request_header).json()

pp.pprint(match_v5_get_list_puuid('청파소나타')['puuid'])


# 게임 match_id 찾기
def match_v5_get_list_match_id(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()

# pp.pprint(match_v5_get_list_match_id("P4Ri8HBanEdTxQeT2cQS1MIN8RFQxaSukyHtFScjRLvUlzVMReZn_Rhzgzxr_HpZjxE_ah3fy4xaiA", 0, 10))

# 게임 정보 가져오기
def match_v5_get_match_history(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    
    return requests.get(url, headers=request_header).json()

# pp.pprint(match_v5_get_match_history("KR_6710383118"))


# match_data = match_v5_get_match_history("KR_6710383118")
# pp.pprint(match_data['info']['participants'][0])
