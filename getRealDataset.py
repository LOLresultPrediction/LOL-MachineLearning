import pprint
import numpy as np
import getAPI
import etcFunction as ef
pp = pprint.PrettyPrinter(indent=4)


# 10분 후 게임 데이터 셋
def tempResult(matchId, frame):
    gameInfo = getAPI.getGameInfoTimeline(matchId)['info']['frames']
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
    print(winTeamValue['towerBreakerId'])
    print(loseTeamValue['towerBreakerId'])
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