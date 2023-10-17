import pprint
import numpy as np
import getAPI
import getDataset
import getMatchId
import csv
import saveDataSet
import pandas as pd
import secondSaveDataset

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

# chanllengerMatchId = ["KR_6744942072",
#     "KR_6736181136",
#     "KR_6736161812",
#     "KR_6736141671",
#     "KR_6731035930",
#     "KR_6730988464",
#     "KR_6730964771",
#     "KR_6725142042",
#     "KR_6725118502",
#     "KR_6725110264",
#     "KR_6725094605",
#     "KR_6721548861",
#     "KR_6721532590",
#     "KR_6718691525",
#     "KR_6718685608",
#     "KR_6717456435",
#     "KR_6717394821",
#     "KR_6716115458",
#     "KR_6716019516",
#     "KR_6714278507"]

if __name__ == "__main__":
    # 1st. matchId csv로 저장 (2번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = getMatchId.getGrandmasterMatchId()
    # with open('MatchId/GrandmasterMatchId.csv','w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(GrandmasterMatchId)
    
    # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)



    # API 2개 사용할 때
    ChanllengerMatchId = pd.read_csv('MatchId/ChanllengerMatchId.csv')
    secondSaveDataset.saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, 1869:]
    # secondSaveDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, 1869)