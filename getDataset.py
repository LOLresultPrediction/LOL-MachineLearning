import pprint
import numpy as np
import getAPI
import etcFunction as ef
pp = pprint.PrettyPrinter(indent=4)

'''
게임 시작 10분 후의 데이터 셋 (타워, 오브젝트 등은 게임 결과 API에서 가져옴)
timestamp 100,000 = 100초
'''
def getDataSet(matchId, frame):
    # matchId = 'KR_6709504031'
    gameInfo = getAPI.getGameInfoTimeline(matchId)['info']['frames']
    firstObjectInfo = getAPI.getGameInfo(matchId)['info']['teams']
    # gameInfo = getGameInfo(matchId)['info']['participants']
    winTeamMember, loseTeamMember = ef.teamClassfication(matchId)
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
                    # mosterKillerId = events[j]['killerId']
                    dragonKillTimestamp = events[j]['timestamp']
                    dragonType = None
                    if dragonKillTimestamp <= (frame*60000):
                        dragonType = events[j]['monsterSubType']
                        dataSet['DragonKind'] = dragonType
                        # dragonKillInfo = dragonType
                        # if mosterKillerId in winTeamMember:
                        #     winTeamValue['dragonKill'].append(dragonKillInfo)
                        # elif mosterKillerId in loseTeamMember:
                        #     loseTeamValue['dragonKill'].append(dragonKillInfo)

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
    dataSet['Diff_FirstDRAGON'] = ef.whoFirstGet(firstObjectInfo, 'dragon')
    dataSet['Diff_Inhibitor'] = ef.whoFirstGet(firstObjectInfo, 'inhibitor')
    dataSet['Diff_FirstHERALD'] = ef.whoFirstGet(firstObjectInfo, 'riftHerald')
    dataSet['Diff_Firsttower'] = ef.whoFirstGet(firstObjectInfo, 'tower')
    dataSet['Diff_FirstBLOOD'] = ef.whoFirstGet(firstObjectInfo, 'champion')

    # print(dragonKillInfo)
    # print(winTeamValue)
    # print(loseTeamValue)
    
    return dataSet