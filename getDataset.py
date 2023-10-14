import pprint
import numpy as np
import getAPI
import etcFunction as ef
pp = pprint.PrettyPrinter(indent=4)

'''
포블 데이터 추가
드래곤 타입 추가
'WIN' -> int형으로 바꾸기
1분 30초 이전에 킬이 발생했는지 = bool

'''

# 15분 후 게임 데이터 셋
def tempResult(matchId, frame):
    gameTimelineInfo = getAPI.getGameInfoTimeline(matchId)['info']['frames']
    gameInfo = getAPI.getGameInfo(matchId)['info']['teams']

    winTeamMember, loseTeamMember = ef.teamClassfication(matchId)
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
    dataSet['matchId'] = matchId
    dataSet['Diff_FirstBLOOD'] = None
    dataSet['Diff_FirstDRAGON'] = None
    dataSet['Diff_FirstHERALD'] = None
    dataSet['Diff_Firsttower'] = None
    dataSet['dragonType'] = None
    # frame을 '분' 단위로 치환하기 위해 +1
    for i in range(frame+1):
        events = gameTimelineInfo[i]['events']
        for j in range(len(events)):
            # 킬/어시
            if events[j]['type'] == 'CHAMPION_KILL':
                for k in range(2):
                    if gameInfo[k]['win']:
                        dataSet['Diff_FirstBLOOD'] = 1 if gameInfo[k]['objectives']['champion']['first'] else -1
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
            # 자이라의 식물도 와드로 식별됨.. 아마?
            if events[j]['type'] == 'WARD_PLACED':
                wardCreatorId = events[j]['creatorId']
                if wardCreatorId in winTeamMember:
                    winTeamValue['wardCreatorId'].append(wardCreatorId)
                elif wardCreatorId in loseTeamMember:
                    loseTeamValue['wardCreatorId'].append(wardCreatorId)
            # 와드 파괴
            if events[j]['type'] == 'WARD_KILL':
                wardKillerId = events[j]['killerId']
                if wardKillerId in winTeamMember:
                    winTeamValue['wardKillerId'].append(wardKillerId)
                elif wardKillerId in loseTeamMember:
                    loseTeamValue['wardKillerId'].append(wardKillerId)


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
                    for k in range(2):
                        if gameInfo[k]['win']:
                            dataSet['Diff_Firsttower'] = 1 if gameInfo[k]['objectives']['tower']['first'] else -1
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
                    if dataSet['dragonType'] == None:
                        dataSet['dragonType'] = events[j]['monsterSubType']
                    for k in range(2):
                        if gameInfo[k]['win']:
                            dataSet['Diff_FirstDRAGON'] = 1 if gameInfo[k]['objectives']['dragon']['first'] else -1
                # 전령
                if events[j]['monsterType'] == 'RIFTHERALD':
                    for k in range(2):
                        if gameInfo[k]['win']:
                            dataSet['Diff_FirstHERALD'] = 1 if gameInfo[k]['objectives']['riftHerald']['first'] else -1
    # 레벨, 미니언 킬, 정글몹 킬 구하기
    for i in range(1, 11):
        participantFrames = gameTimelineInfo[frame]['participantFrames'][str(i)]
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
    # print(winTeamValue['wardCreatorId'])
    # print(loseTeamValue['wardCreatorId'])
    dataSet['Diff_WARDkill'] = len(winTeamValue['wardKillerId']) - len(loseTeamValue['wardKillerId'])
    dataSet['Diff_Inhibitor'] = len(winTeamValue['inhibitorBreakerId']) - len(loseTeamValue['inhibitorBreakerId'])
    dataSet['result'] = 1
    # pp.pprint(winTeamValue)
    # pp.pprint(loseTeamValue)
    
    return dataSet