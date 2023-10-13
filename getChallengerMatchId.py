import time
import getAPI

challengerMatchIdSet = set()

# 챌린저 matchId 가져오기(약 7분 / 3,000 데이터)
def getChallengerMatchId():

    # 챌린저 소환사 Puuid 가져오기(중복제거)
    for entry in getAPI.getChallengerEntries():
        challengerMatchIdSet.update(getAPI.getMatchId(getAPI.getUserPuuidBySummonerId(entry['summonerId']), 0, 20))
        time.sleep(1)

    return challengerMatchIdSet