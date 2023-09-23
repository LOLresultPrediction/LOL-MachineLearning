import requests
import pprint

pp = pprint.PrettyPrinter(indent=4)
# 24시간마다 변경해야 함
# 24일 10시 20분까지
api_key = 'RGAPI-f28f216c-c0e5-49ea-8404-17b17f631d87'
request_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

# 유저 puuid 가져오기
def get_userPuuid(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?{api_key}"
    return requests.get(url, headers=request_header).json()['puuid']

# print(get_userPuuid('청파소나타')['puuid'])


# 게임 match_id 찾기
def get_gameId(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()

# pp.pprint(match_v5_get_list_match_id("P4Ri8HBanEdTxQeT2cQS1MIN8RFQxaSukyHtFScjRLvUlzVMReZn_Rhzgzxr_HpZjxE_ah3fy4xaiA", 0, 10))

# 게임 정보 가져오기
def get_gameInfo(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    return requests.get(url, headers=request_header).json()

# pp.pprint(get_gameInfo("KR_6710383118"))

# KDA 가져오기
def get_teamKDA(matchId):
    matchInfo = get_gameInfo(matchId)
    teamKDA = {'kills' : 0, 'deaths' : 0, 'assists' : 0}
    # for i in range(5):
    #     teamKDA['kills'] += matchInfo['info']['participants'][i]['kills']
    #     teamKDA['deaths'] += matchInfo['info']['participants'][i]['deaths']
    #     teamKDA['assists'] += matchInfo['info']['participants'][i]['assists']
    # return teamKDA

def get_userKDARecord(nickName, start, count):
    userName = get_userPuuid(nickName)
    gameIdList = get_gameId(userName, start, count)
    for i in gameIdList:
        gameKDA = get_teamKDA(i)
        print(gameKDA)

matchInfo = get_gameInfo("KR_6710383118")
print(matchInfo['info']['participants'][0]['kills'])

# get_userKDARecord("청파소나타", 0, 5)
