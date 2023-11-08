import pprint
import getAPI
import numpy as np
pp = pprint.PrettyPrinter(indent=4)

# 승리 팀, 패배 팀 participantId로 나누기
def teamClassfication(matchId):
    gameInfo = getAPI.getGameInfo(matchId)['info']['participants']
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
    

def tempLoadData(frameNum, gameTimelineInfo, winTeamMember, winTeamValue, loseTeamMember, loseTeamValue, dataSet, KillerIdList):
    # 레벨, 미니언 킬, 정글몹 킬 구하기
    print("check")
    for i in range(1, 11):
        participantFrames = gameTimelineInfo['frames'][frameNum]['participantFrames'][str(i)]
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
    dataSet['Diff-K-top'] = KillerIdList.count(1) - KillerIdList.count(6) 
    dataSet['Diff-K-jug'] = KillerIdList.count(2) - KillerIdList.count(7) 
    dataSet['Diff-K-mid'] = KillerIdList.count(3) - KillerIdList.count(8) 
    dataSet['Diff-K-ad'] = KillerIdList.count(4) - KillerIdList.count(9) 
    dataSet['Diff-K-sup'] = KillerIdList.count(5) - KillerIdList.count(10) 
    if 6 in winTeamMember:
        dataSet['Diff-K-top'] *= -1
        dataSet['Diff-K-jug'] *= -1
        dataSet['Diff-K-mid'] *= -1
        dataSet['Diff-K-ad'] *= -1
        dataSet['Diff-K-sup'] *= -1
    for i in range(1, 11):
        if i in winTeamMember:
            if i == 1 or i == 6:
                dataSet['K-WIN-top'] = KillerIdList.count(i)
            if i == 2 or i == 7:
                dataSet['K-WIN-jug'] = KillerIdList.count(i)
            if i == 3 or i == 8:
                dataSet['K-WIN-mid'] = KillerIdList.count(i)
            if i == 4 or i == 9:
                dataSet['K-WIN-ad'] = KillerIdList.count(i)
            if i == 5 or i == 10:
                dataSet['K-WIN-sup'] = KillerIdList.count(i)
        elif i in loseTeamMember:
            if i == 1 or i == 6:
                dataSet['K-LOSE-top'] = KillerIdList.count(i)
            if i == 2 or i == 7:
                dataSet['K-LOSE-jug'] = KillerIdList.count(i)
            if i == 3 or i == 8:
                dataSet['K-LOSE-mid'] = KillerIdList.count(i)
            if i == 4 or i == 9:
                dataSet['K-LOSE-ad'] = KillerIdList.count(i)
            if i == 5 or i == 10:
                dataSet['K-LOSE-sup'] = KillerIdList.count(i)
    dataSet['Diff-A'] = sum(len(i) for i in winTeamValue['killInfo']['assistId'] if i != None) - sum(len(i) for i in loseTeamValue['killInfo']['assistId'] if i != None)
    dataSet['Diff_WARDplaced'] = len(winTeamValue['wardCreatorId']) - len(loseTeamValue['wardCreatorId'])
    dataSet['Diff_WARDkill'] = len(winTeamValue['wardKillerId']) - len(loseTeamValue['wardKillerId'])
    dataSet['Diff_Inhibitor'] = len(winTeamValue['inhibitorBreakerId']) - len(loseTeamValue['inhibitorBreakerId'])
    dataSet['Diff_TOWERkill'] = len(winTeamValue['towerBreakerId']) - len(loseTeamValue['towerBreakerId'])
    dataSet['Diff-ControlWARDplaced'] = dataSet['WIN_controlWARDPlaced'] - dataSet['LOSE_controlWARDPlaced']
    dataSet['result'] = 1

    return dataSet