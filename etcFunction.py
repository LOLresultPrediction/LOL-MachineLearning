import pprint
import getAPI
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