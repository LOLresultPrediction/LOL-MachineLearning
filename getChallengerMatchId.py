import requests
import time
import getAPI

challengerPuuidList = []
challengerMatchIdSet = set()

# 챌린저 소환사 정보 가져오기
def getChallengerEntries():
    url = f"https://kr.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key{RiotAPI.api_key}"
    return requests.get(url, headers=getAPI.request_header).json()['entries']

# 챌린저 소환사 Puuid 가져오기
for entry in getChallengerEntries():
    challengerPuuidList.append(getAPI.getUserPuuidBySummonerId(entry['summonerId']))

    # Riot API는 120분 / 100개 요청까지 허용하기 때문에 120÷100=1.2에 오차 0.1을 더해 1.3초마다 요청을 수행하도록 함
    time.sleep(1.3)

# 챌린저 matchId 가져오기(중복제거)
for puuid in challengerPuuidList:
    challengerMatchIdSet.update(getAPI.getMatchId(puuid, 0, 20))
    time.sleep(1.3)

print(len(challengerMatchIdSet))
