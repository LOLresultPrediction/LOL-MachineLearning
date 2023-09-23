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
def getUserPuuid(summonerName):
    url = f"https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?{api_key}"
    return requests.get(url, headers=request_header).json()['puuid']
# print(get_userPuuid('청파소나타')['puuid'])


# 게임 match_id 찾기
def getGameId(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(getGameId("P4Ri8HBanEdTxQeT2cQS1MIN8RFQxaSukyHtFScjRLvUlzVMReZn_Rhzgzxr_HpZjxE_ah3fy4xaiA", 0, 10))

# 게임 정보 가져오기
def getGameInfo(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(get_gameInfo("KR_6710383118"))

# 타임라인으로 게임 정보 가져오기
def getGameInfoTimeline(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"
    return requests.get(url, headers=request_header).json()

# KDA 가져오기
def getTeamKDA(matchId):
    gameInfo = getGameInfo(matchId)
    gameResult = {'win' : bool, 'lose' : bool}
    gameResult['win'] = {'kills' : 0, 'deaths' : 0, 'assists' : 0}
    gameResult['lose'] = {'kills' : 0, 'deaths' : 0, 'assists' : 0}
    diffScore = {'diffKillScore' : 0, 'diffDeathScore' : 0, 'diffAssistScore' : 0}
    # i번째 플레이어 (블루팀이 먼저 출력)
    for i in range(10):
        # 이긴 팀
        if gameInfo['info']['participants'][i]['win'] == True:
            gameResult['win']['kills'] += gameInfo['info']['participants'][i]['kills']
            gameResult['win']['deaths'] += gameInfo['info']['participants'][i]['deaths']
            gameResult['win']['assists'] += gameInfo['info']['participants'][i]['assists']
        # 진 팀
        if gameInfo['info']['participants'][i]['win'] == False:
            gameResult['lose']['kills'] += gameInfo['info']['participants'][i]['kills']
            gameResult['lose']['deaths'] += gameInfo['info']['participants'][i]['deaths']
            gameResult['lose']['assists'] += gameInfo['info']['participants'][i]['assists']
    return gameResult
# pp.pprint(getGameInfo('KR_6709504031')['info']['participants'][0]['championName'])
# for i in range(10):
#     print(getGameInfo('KR_6709504031')['info']['participants'][i]['win'])

# nickName의 start번째 경기부터 count개 경기의 팀 KDA 합 가져오기  (gameKDA{}에 넣을 때 역으로 반전됨)
# 리턴값 == {게임코드 : {우리 팀}, {상대팀}}
def getTeamKDARecord(nickName, start, count):
    userName = getUserPuuid(nickName)
    gameIdList = getGameId(userName, start, count)
    gameKDA = {}
    for i in gameIdList:
        gameKDA[i] = getTeamKDA(i)
    return gameKDA

# pp.pprint(getTeamKDARecord("청파소나타", 0, 5))
print(getTeamKDA('KR_6709504031'))
