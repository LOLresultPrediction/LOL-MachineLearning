import requests
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)
# 24시간마다 변경해야 함
api_key = 'RGAPI-60b643c9-a962-4629-a99c-84c1c3342849'
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
def getMatchId(puuid, start, count):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start={start}&count={count}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(getMatchId("P4Ri8HBanEdTxQeT2cQS1MIN8RFQxaSukyHtFScjRLvUlzVMReZn_Rhzgzxr_HpZjxE_ah3fy4xaiA", 0, 10))

# 게임 정보 가져오기
def getGameInfo(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}"
    return requests.get(url, headers=request_header).json()
# pp.pprint(getGameInfo("KR_6710383118"))

# 타임라인으로 게임 정보 가져오기
def getGameInfoTimeline(matchId):
    url = f"https://asia.api.riotgames.com/lol/match/v5/matches/{matchId}/timeline"
    return requests.get(url, headers=request_header).json()

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames'])

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames']['1']['level'])


# for i in range(1, 11):
#     pp.pprint(getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['participantFrames'][str(i)]['totalGold'])

# pp.pprint(getGameInfoTimeline('KR_6709504031')['info'].keys())


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

# nickName의 start번째 경기부터 count개 경기의 팀 KDA 합 가져오기  (gameKDA{}에 넣을 때 역으로 반전됨)
# 리턴값 == {게임코드 : {우리 팀}, {상대팀}}
def getTeamKDARecord(nickName, start, count):
    userName = getUserPuuid(nickName)
    matchIdList = getMatchId(userName, start, count)
    gameKDA = {}
    for i in matchIdList:
        gameKDA[i] = getTeamKDA(i)
    return gameKDA

# pp.pprint(getTeamKDARecord("청파소나타", 0, 5))
# print(getTeamKDA('KR_6709504031'))


# 게임 정보 확인
# matchId = 'KR_6709504031'
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['championName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['summonerName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['kills'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['deaths'])




# --------------------------------------------------------------------10분 후 게임 데이터------------------------------------------------------------------------------------

# 승리 팀, 패배 팀 participantId로 나누기
def teamClassfication(matchId):
    gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember = []
    loseTeamMember = []
    for i in range(1, 11):
        if gameInfo[i-1]['win'] == True:
            winTeamMember.append(gameInfo[i-1]['participantId'])
        elif gameInfo[i-1]['win'] == False:
            loseTeamMember.append(gameInfo[i-1]['participantId'])

    return winTeamMember, loseTeamMember


# 게임 시작 10분 후의 데이터 셋 (탑, 정글, 미드, 원딜, 서폿)
def getDataSet(matchId, frame):
    # matchId = 'KR_6709504031'
    gameInfo = getGameInfoTimeline(matchId)['info']['frames']
    # gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember, loseTeamMember = teamClassfication(matchId)
    dataSet = {}
    winTeam = {'level' : [], 'minionsKilled' : [], 'jungleMinionsKilled' : [], 'killInfo' : {'killerId' : [], 'assistId' : []}}
    loseTeam = {'level' : [], 'minionsKilled' : [], 'jungleMinionsKilled' : [], 'killInfo' : {'killerId' : [], 'assistId' : []}}

    # 킬, 어시스트 유저 assistingParticipantId 구하기
    for i in range(frame):
        events = gameInfo[i]['events']
        for j in range(len(events)):
            if 'CHAMPION_KILL' in events[j]['type']:
                killerId = events[j]['killerId']
                assistId = None
                if 'assistingParticipantIds' in events[j]:
                    assistId = events[j]['assistingParticipantIds']
                if killerId in winTeamMember:
                    winTeam['killInfo']['killerId'].append(killerId)
                    winTeam['killInfo']['assistId'].append(assistId)
                elif killerId in loseTeamMember:
                    loseTeam['killInfo']['killerId'].append(killerId)
                    loseTeam['killInfo']['assistId'].append(assistId)
                    
    # level, minionsKill, jungleMinionsKill 구하기
    for i in range(1, 11):
        participantFrames = gameInfo[frame]['participantFrames'][str(i)]
        if i in winTeamMember:
            winTeam['level'].append(participantFrames['level'])
            winTeam['minionsKilled'].append(participantFrames['minionsKilled'])
            winTeam['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
        elif i in loseTeamMember:
            loseTeam['level'].append(participantFrames['level'])
            loseTeam['minionsKilled'].append(participantFrames['minionsKilled'])
            loseTeam['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
    dataSet['diffLevel'] = np.array(winTeam['level']) - np.array(loseTeam['level'])
    dataSet['diffMinionsKilled'] = np.array(winTeam['minionsKilled']) - np.array(loseTeam['minionsKilled'])
    dataSet['diffJungleMinionsKilled'] = np.array(winTeam['jungleMinionsKilled']) - np.array(loseTeam['jungleMinionsKilled'])
    dataSet['diffKillScore'] = len(winTeam['killInfo']['killerId']) - len(loseTeam['killInfo']['killerId'])
    # winTeamAssist = sum(len(i) for i in winTeam['killInfo']['assistId'] if i != None)
    # loseTeamAssist = sum(len(i) for i in winTeam['killInfo']['assistId'] if i != None)
    dataSet['diffAssistScore'] = sum(len(i) for i in winTeam['killInfo']['assistId'] if i != None) - sum(len(i) for i in loseTeam['killInfo']['assistId'] if i != None)
    print('winTeam : ', winTeam)
    print('loseTeam : ', loseTeam)
    return dataSet




print(getDataSet('KR_6710383118', 10))


# [0]['participantId']
# teamId[1]['win']
# pp.pprint(teamId)


# gameInfo = getGameInfo('KR_6709531155')['info']['participants']
# killInfo = {}
# for i in range(11):
#     event = getGameInfoTimeline('KR_6710383118')['info']['frames'][i]['events']
#     for j in range(len(event)):
#         if 'CHAMPION_KILL' in event[j]['type']:
#             timeStamp = event[j]['timestamp']
#             assistingParticipantIds = None
#             if 'assistingParticipantIds' in event[j]:
#                 assistingParticipantIds = event[j]['assistingParticipantIds']
#             killerId = event[j]['killerId']
#             killInfo[timeStamp, killerId] = assistingParticipantIds

#             # print(assistingParticipantIds)
# print(killInfo)

            # if gameInfo[killerId]
    # if 'killerId' in event:
    #     pp.pprint(event['killerId'].keys())

# event = getGameInfoTimeline('KR_6709504031')['info']['frames'][10]['events']
# pp.pprint(event[10])