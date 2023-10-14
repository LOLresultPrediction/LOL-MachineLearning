import pprint
import numpy as np
import getAPI
import getDataset
import getMatchId
import csv
import saveDataSet

pp = pprint.PrettyPrinter(indent=4)



# pp.pprint(getGameInfo('KR_6708057039')['info']['teams'][0]['objectives'])

'''
'KR_6710383118', 1. 브라이어(5/14/5)
'KR_6709906475', 2. 브라이어(7/9/1)
'KR_6709583655', 3. 브라이어(0/0/0)
'KR_6709531155', 4. 나피리(8/9/2)
'KR_6709504031', 5. 라이즈
'KR_6708057039', 6. 브라이어(0/9/0)
'KR_6708035868',
'KR_6707425375',
'KR_6707289771',
'KR_6704954051']
'''
if __name__ == "__main__":
    # 챌린저 매치 ID 가져오기
    # print(len(getMatchId.getChallengerMatchId()))


    chanllengerMatchId = ["KR_6744942072",
    "KR_6736181136",
    "KR_6736161812",
    "KR_6736141671",
    "KR_6731035930",
    "KR_6730988464",
    "KR_6730964771",
    "KR_6725142042",
    "KR_6725118502",
    "KR_6725110264",
    "KR_6725094605",
    "KR_6721548861",
    "KR_6721532590",
    "KR_6718691525",
    "KR_6718685608",
    "KR_6717456435",
    "KR_6717394821",
    "KR_6716115458",
    "KR_6716019516",
    "KR_6714278507"]
    saveDataSet.saveDataSetToCSV(chanllengerMatchId, 'chanllenger.csv', 15)
    # for i in chanllengerMatchId:
    #     saveDataSet.saveDataSetToCSV(dic_data, f"Challenger.csv")
    #     print(i)
    # fieldnames = getDataset.tempResult('KR_6714278507', 15)
    # # print(len(dic_data.keys()))
    # with open('challenger.csv','w', newline='') as f:
    #     w = csv.DictWriter(f, fieldnames.keys())
    #     w.writeheader()
    #     for i in chanllengerMatchId:
    #         dic_data = getDataset.tempResult(i, 15)
    #         w.writerow(dic_data)
    #         print(i)
    # print(dic_data)

    # gameTimelineInfo = getAPI.getGameInfoTimeline('KR_6708057039')
    # gameInfo = getAPI.getGameInfo('KR_6709906475')
    # for i in range(10):
    #     pp.pprint(gameInfo['info']['participants'][i]['participantId'])
    #     pp.pprint(gameInfo['info']['participants'][i]['summonerName'])
    #     pp.pprint(gameInfo['info']['participants'][i]['championName'])
    # pp.pprint(gameInfo['info']['teams'][1]['objectives'])

    # pp.pprint(getDataset.getDataSet('KR_6708057039', 15))
    # pp.pprint(getAPI.getGameInfo('KR_6708057039')['info']['teams'])