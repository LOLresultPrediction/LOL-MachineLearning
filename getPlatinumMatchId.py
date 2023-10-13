import time
import getAPI

def getPlatinumMatchId(tier="IV", start_page=1, end_page=20):
    platinumMatchIdSet = set()

    for page in range(start_page, end_page + 1): 
        for entry in getAPI.getPlatinumEntries(tier, page):  
            platinumMatchIdSet.update(getAPI.getMatchId(getAPI.getUserPuuidBySummonerId(entry['summonerId']), 0, 20))
            time.sleep(1)

    return platinumMatchIdSet

if __name__ == "__main__":
    match_ids = getPlatinumMatchId("I", 1, 2)  #플래티넘 1 유저 정보의 1페이지부터 2페이지 가져오기
    print(match_ids)