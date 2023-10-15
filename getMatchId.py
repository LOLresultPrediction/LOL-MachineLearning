import time
import getAPI

# KeyError: 'puuid' 발생 시 time.sleep(n)값 증가

# 챌린저 matchId 가져오기(약 6분 / 3,000 데이터)
def getChallengerMatchId():
    challengerMatchIdSet = set()
    # 챌린저 소환사 Puuid 가져오기(중복제거)
    for entry in getAPI.getChallengerEntries():
        print("챌린저 matchId 가져오는 중 ... ")
        challengerMatchIdSet.update(getAPI.getMatchId(getAPI.getUserPuuidBySummonerId(entry['summonerId']), 0, 20))
        time.sleep(0.7)
    return challengerMatchIdSet

# 그랜드마스터 matchId 가져오기(약 14분 / 8,000 데이터)
def getGrandmasterMatchId():
    grandmasterMatchIdSet = set()

    # 그랜드마스터 소환사 Puuid 가져오기(중복제거)
    for entry in getAPI.getGrandmasterEntries():
        grandmasterMatchIdSet.update(getAPI.getMatchId(getAPI.getUserPuuidBySummonerId(entry['summonerId']), 0, 20))
        time.sleep(0.7)

    return grandmasterMatchIdSet

# 마스터 matchId 가져오기(약 30분(?) / 11,000 데이터)
def getMasterMatchId():
    masterMatchIdSet = set()

    # 마스터 소환사 Puuid 가져오기(중복제거)
    for entry in getAPI.getMasterEntries():
        masterMatchIdSet.update(getAPI.getMatchId(getAPI.getUserPuuidBySummonerId(entry['summonerId']), 0, 20))
        time.sleep(0.7)

    return masterMatchIdSet