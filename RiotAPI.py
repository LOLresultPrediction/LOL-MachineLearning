import requests
import pprint
import numpy as np

pp = pprint.PrettyPrinter(indent=4)
# 24시간마다 변경해야 함
api_key = 'RGAPI-a09c11c3-9931-48bb-8f87-03b86e9a931f'
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

# 게임 정보 확인
# matchId = 'KR_6709504031'
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['championName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][1]['summonerName'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['kills'])
# pp.pprint(getGameInfo(matchId)['info']['participants'][0]['deaths'])


# --------------------------------------------------------------------10분 후 게임 데이터------------------------------------------------------------------------------------
# 10분 후 게임 데이터 셋
def tempResult(matchId, frame):
    gameInfo = getGameInfoTimeline(matchId)['info']['frames']
    winTeamMember, loseTeamMember = teamClassfication(matchId)
    winTeamValue = {'level' : [], 
                    'minionsKilled' : [], 
                    'jungleMinionsKilled' : [], 
                    'killInfo' : {'killerId' : [], 'assistId' : []}, 
                    'wardCreatorId' : [], 
                    'wardKillerId' : [],
                    'inhibitorBreakerId' : [],
                    'towerBreakerId' : [],
                    'dragonKill' : [],
                    'riftheraldKill' : []}
    loseTeamValue = {'level' : [], 
                     'minionsKilled' : [], 
                     'jungleMinionsKilled' : [], 
                     'killInfo' : {'killerId' : [], 'assistId' : []}, 
                     'wardCreatorId' : [], 
                     'wardKillerId' : [],
                     'inhibitorBreakerId' : [],
                     'towerBreakerId' : [],
                     'dragonKill' : [],
                     'riftheraldKill' : []}
    dataSet = {}
    for i in range(frame):
        events = gameInfo[i]['events']
        for j in range(len(events)):
            # 킬/어시
            if events[j]['type'] == 'CHAMPION_KILL':
                killerId = events[j]['killerId']
                assistId = None
                if len(loseTeamValue['killInfo']['killerId']) + len(winTeamValue['killInfo']['killerId']) == 0:
                    if killerId in winTeamMember:
                        dataSet['Diff_FirstBLOOD'] = "WIN"
                    elif killerId in loseTeamMember:
                        dataSet['Diff_FirstBLOOD'] = "LOSE"
                if 'assistingParticipantIds' in events[j]:
                    assistId = events[j]['assistingParticipantIds']
                if killerId in winTeamMember:
                    winTeamValue['killInfo']['killerId'].append(killerId)
                    winTeamValue['killInfo']['assistId'].append(assistId)
                elif killerId in loseTeamMember:
                    loseTeamValue['killInfo']['killerId'].append(killerId)
                    loseTeamValue['killInfo']['assistId'].append(assistId)
            # 와드 설치
            if  events[j]['type'] == 'WARD_PLACED':
                wardCreatorId = events[j]['creatorId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardCreatorId'].append(wardCreatorId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardCreatorId'].append(wardCreatorId)
            # 와드 파괴
            if  events[j]['type'] == 'WARD_KILL':
                wardKillerId = events[j]['killerId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardKillerId'].append(wardKillerId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardKillerId'].append(wardKillerId)\


            # 구조물 파괴
            if events[j]['type'] == 'BUILDING_KILL':
                # 억제기
                if events[j]['buildingType'] == 'INHIBITOR_BUILDING':
                    buildingKillerId = events[j]['killerId']
                    if buildingKillerId in winTeamMember:
                        winTeamValue['inhibitorBreakerId'].append(buildingKillerId)
                    elif buildingKillerId in loseTeamMember:
                        loseTeamValue['inhibitorBreakerId'].append(buildingKillerId)
                # 타워
                if events[j]['buildingType'] == 'TOWER_BUILDING':
                    buildingKillerId = events[j]['killerId']
                    if buildingKillerId in winTeamMember:
                        winTeamValue['towerBreakerId'].append(buildingKillerId)
                    elif buildingKillerId in loseTeamMember:
                        loseTeamValue['towerBreakerId'].append(buildingKillerId)
            # 엘리트 몬스터 킬
            if events[j]['type'] == 'ELITE_MONSTER_KILL':
                # 드래곤
                if events[j]['monsterType'] == 'DRAGON':
                    mosterKillerId = events[j]['killerId']
                    dragonType = events[j]['monsterSubType']
                    dragonKillTimestamp = events[j]['timestamp']
                    dragonKillInfo = [dragonKillTimestamp, dragonType]
                    if mosterKillerId in winTeamMember:
                        winTeamValue['dragonKill'].append(dragonKillInfo)
                    elif mosterKillerId in loseTeamMember:
                        loseTeamValue['dragonKill'].append(dragonKillInfo)
                if events[j]['monsterType'] == 'RIFTHERALD':
                    mosterKillerId = events[j]['killerId']
                    riftheraldKillTimestamp = events[j]['timestamp']
                    if mosterKillerId in winTeamMember:
                        winTeamValue['riftheraldKill'].append(riftheraldKillTimestamp)
                    elif mosterKillerId in loseTeamMember:
                        loseTeamValue['riftheraldKill'].append(riftheraldKillTimestamp)
    # 레벨, 미니언 킬, 정글몹 킬 구하기
    for i in range(1, 11):
        participantFrames = gameInfo[frame]['participantFrames'][str(i)]
        if i in winTeamMember:
            winTeamValue['level'].append(participantFrames['level'])
            winTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            winTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
        elif i in loseTeamMember:
            loseTeamValue['level'].append(participantFrames['level'])
            loseTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            loseTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
    dataSet['Diff_LV'] = sum(np.array(winTeamValue['level']) - np.array(loseTeamValue['level']))
    dataSet['Diff_CS'] = sum(np.array(winTeamValue['minionsKilled']) - np.array(loseTeamValue['minionsKilled']))
    dataSet['Diff_jglCS'] = sum(np.array(winTeamValue['jungleMinionsKilled']) - np.array(loseTeamValue['jungleMinionsKilled']))
    # 0번 인덱스의 diffKillScore에 관한 어시스트는 diffAssistScore의 0번 인덱스임
    dataSet['Diff-K'] = len(winTeamValue['killInfo']['killerId']) - len(loseTeamValue['killInfo']['killerId'])
    dataSet['Diff-A'] = sum(len(i) for i in winTeamValue['killInfo']['assistId'] if i != None) - sum(len(i) for i in loseTeamValue['killInfo']['assistId'] if i != None)
    dataSet['Diff_WARDplaced'] = len(winTeamValue['wardCreatorId']) - len(loseTeamValue['wardCreatorId'])
    dataSet['Diff_WARDkill'] = len(winTeamValue['wardKillerId']) - len(loseTeamValue['wardKillerId'])
    dataSet['Diff_Inhibitor'] = len(winTeamValue['inhibitorBreakerId']) - len(loseTeamValue['inhibitorBreakerId'])
    dataSet['Diff_Firsttower'] = len(winTeamValue['towerBreakerId']) - len(loseTeamValue['towerBreakerId'])
    # 첫 용을 먹은 팀
    if not loseTeamValue['dragonKill'] and not winTeamValue['dragonKill']:
        dataSet['Diff_FirstDRAGON'] = None
    elif not loseTeamValue['dragonKill']:
        dataSet['Diff_FirstDRAGON'] = 'WIN'
    elif not winTeamValue['dragonKill']:
        dataSet['Diff_FirstDRAGON'] = 'LOSE'
    else:
        if winTeamValue['dragonKill'][0] < loseTeamValue['dragonKill'][0]:
            dataSet['Diff_FirstDRAGON'] = 'WIN'
        else:
            dataSet['Diff_FirstDRAGON'] = 'LOSE'
    # 첫 전령을 먹은 팀
    if not loseTeamValue['riftheraldKill'] and not winTeamValue['riftheraldKill']:
        dataSet['Diff_FirstHERALD'] = None
    elif not loseTeamValue['riftheraldKill']:
        dataSet['Diff_FirstHERALD'] = 'WIN'
    elif not winTeamValue['riftheraldKill']:
        dataSet['Diff_FirstHERALD'] = 'loseTeam'
    else:
        if winTeamValue['riftheraldKill'][0] < loseTeamValue['riftheraldKill'][0]:
            dataSet['Diff_FirstHERALD'] = 'WIN'
        else:
            dataSet['Diff_FirstHERALD'] = 'LOSE'
    # pp.pprint(winTeamValue)
    # pp.pprint(loseTeamValue)
    return dataSet

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
    # if id in winTeamMember:
    #     return winTeamValue
    #     winTeamValue['wardCreatorId'].append(wardCreatorId)
    # elif wardCreatorId in loseTeamMember:
    #     loseTeamValue['wardCreatorId'].append(wardCreatorId)
    return winTeamMember, loseTeamMember

# 처음 오브젝트 획득 한 팀
def whoFirstGet(firstObjectInfo, object):
    if firstObjectInfo[0]['objectives'][object]['first']:
        return firstObjectInfo[0]['win']
    elif firstObjectInfo[1]['objectives'][object]['first']:
        return firstObjectInfo[1]['win']



# 게임 시작 10분 후의 데이터 셋 (타워, 오브젝트 등은 게임 결과 API에서 가져옴)
def getDataSet(matchId, frame):
    # matchId = 'KR_6709504031'
    gameInfo = getGameInfoTimeline(matchId)['info']['frames']
    firstObjectInfo = getGameInfo(matchId)['info']['teams']
    # gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember, loseTeamMember = teamClassfication(matchId)
    dataSet = {}
    winTeamValue = {'level' : [], 
                    'minionsKilled' : [], 
                    'jungleMinionsKilled' : [], 
                    'killInfo' : {'killerId' : [], 'assistId' : []}, 
                    'wardCreatorId' : [], 
                    'wardKillerId' : [],
                    'inhibitorBreakerId' : [],
                    'towerBreakerId' : [],
                    'dragonKill' : []}
    loseTeamValue = {'level' : [], 
                     'minionsKilled' : [], 
                     'jungleMinionsKilled' : [], 
                     'killInfo' : {'killerId' : [], 'assistId' : []}, 
                     'wardCreatorId' : [], 
                     'wardKillerId' : [],
                     'inhibitorBreakerId' : [],
                     'towerBreakerId' : [],
                     'dragonKill' : []}

    # 킬, 어시스트 유저 assistingParticipantId 구하기
    for i in range(frame):
        events = gameInfo[i]['events']
        for j in range(len(events)):
            # 킬/어시
            if events[j]['type'] == 'CHAMPION_KILL':
                killerId = events[j]['killerId']
                assistId = None
                if 'assistingParticipantIds' in events[j]:
                    assistId = events[j]['assistingParticipantIds']
                if killerId in winTeamMember:
                    winTeamValue['killInfo']['killerId'].append(killerId)
                    winTeamValue['killInfo']['assistId'].append(assistId)
                elif killerId in loseTeamMember:
                    loseTeamValue['killInfo']['killerId'].append(killerId)
                    loseTeamValue['killInfo']['assistId'].append(assistId)
            # 와드 설치
            if  events[j]['type'] == 'WARD_PLACED':
                wardCreatorId = events[j]['creatorId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardCreatorId'].append(wardCreatorId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardCreatorId'].append(wardCreatorId)
            # 와드 파괴
            if  events[j]['type'] == 'WARD_KILL':
                wardKillerId = events[j]['killerId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardKillerId'].append(wardKillerId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardKillerId'].append(wardKillerId)
            # 구조물 파괴
            if events[j]['type'] == 'BUILDING_KILL':
                # 억제기
                if events[j]['buildingType'] == 'INHIBITOR_BUILDING':
                    buildingBreakerId = events[j]['killerId']
                    if buildingBreakerId in winTeamMember:
                        winTeamValue['inhibitorBreakerId'].append(buildingBreakerId)
                    elif buildingBreakerId in loseTeamMember:
                        loseTeamValue['inhibitorBreakerId'].append(buildingBreakerId)
                # 타워
                if events[j]['buildingType'] == 'TOWER_BUILDING':
                    buildingBreakerId = events[j]['killerId']
                    timpstamp = events[j]['timestamp']
                    if buildingBreakerId in winTeamMember:
                        winTeamValue['towerBreakerId'].append(timpstamp)
                        winTeamValue['towerBreakerId'].append(buildingBreakerId)
                    elif buildingBreakerId in loseTeamMember:
                        loseTeamValue['towerBreakerId'].append(timpstamp)
                        loseTeamValue['towerBreakerId'].append(buildingBreakerId)

            # 엘리트 몬스터 킬
            if events[j]['type'] == 'ELITE_MONSTER_KILL':
                # 드래곤
                if events[j]['monsterType'] == 'DRAGON':
                    mosterKillerId = events[j]['killerId']
                    dragonType = events[j]['monsterSubType']
                    dragonKillTimestamp = events[j]['timestamp']
                    dragonKillInfo = [dragonKillTimestamp, dragonType]
                    if mosterKillerId in winTeamMember:
                        winTeamValue['dragonKill'].append(dragonKillInfo)
                    elif mosterKillerId in loseTeamMember:
                        loseTeamValue['dragonKill'].append(dragonKillInfo)

    # 레벨, 미니언 킬, 정글몹 킬 구하기
    for i in range(1, 11):
        participantFrames = gameInfo[frame]['participantFrames'][str(i)]
        if i in winTeamMember:
            winTeamValue['level'].append(participantFrames['level'])
            winTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            winTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
        elif i in loseTeamMember:
            loseTeamValue['level'].append(participantFrames['level'])
            loseTeamValue['minionsKilled'].append(participantFrames['minionsKilled'])
            loseTeamValue['jungleMinionsKilled'].append(participantFrames['jungleMinionsKilled'])
    
    dataSet['Diff_LV'] = sum(np.array(winTeamValue['level']) - np.array(loseTeamValue['level']))
    dataSet['Diff_CS'] = sum(np.array(winTeamValue['minionsKilled']) - np.array(loseTeamValue['minionsKilled']))
    dataSet['Diff_jglCS'] = sum(np.array(winTeamValue['jungleMinionsKilled']) - np.array(loseTeamValue['jungleMinionsKilled']))
    # 0번 인덱스의 diffKillScore에 관한 어시스트는 diffAssistScore의 0번 인덱스임
    dataSet['Diff-K'] = len(winTeamValue['killInfo']['killerId']) - len(loseTeamValue['killInfo']['killerId'])
    dataSet['Diff-A'] = sum(len(i) for i in winTeamValue['killInfo']['assistId'] if i != None) - sum(len(i) for i in loseTeamValue['killInfo']['assistId'] if i != None)
    dataSet['Diff_WARDplaced'] = len(winTeamValue['wardCreatorId']) - len(loseTeamValue['wardCreatorId'])
    dataSet['Diff_WARDkill'] = len(winTeamValue['wardKillerId']) - len(loseTeamValue['wardKillerId'])
    dataSet['Diff_FirstDRAGON'] = whoFirstGet(firstObjectInfo, 'dragon')
    dataSet['Diff_Inhibitor'] = whoFirstGet(firstObjectInfo, 'inhibitor')
    dataSet['Diff_FirstHERALD'] = whoFirstGet(firstObjectInfo, 'riftHerald')
    dataSet['Diff_Firsttower'] = whoFirstGet(firstObjectInfo, 'tower')
    dataSet['Diff_FirstBLOOD'] = whoFirstGet(firstObjectInfo, 'champion')
    # dataSet['fistTower'] = whoFirstGet('riftheraldKill', winTeamValue, loseTeamValue)
    # if firstObjectInfo[0]['objectives']['dragon']:
    #     dataSet['fistDragonKill'] = firstObjectInfo[0]['win']
    # elif firstObjectInfo[1]['objectives']['dragon']:
    #     dataSet['fistDragonKill'] = firstObjectInfo[1]['win']
    # print(winTeamValue)
    # print(loseTeamValue)
    
    return dataSet


# pp.pprint(getGameInfo('KR_6708057039')['info']['teams'][0]['objectives'])



# pp.pprint(tempResult('KR_6708057039', 10))
# pp.pprint(getDataSet('KR_6708057039', 10))
# pp.pprint(getGameInfo('KR_6708057039')['info']['participants'][0])
# pp.pprint(getGameInfoTimeline('KR_6709531155').keys())
# pp.pprint(getGameInfoTimeline('KR_6708057039')['info']['frames'][10]['events'])