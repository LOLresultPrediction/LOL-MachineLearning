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


if __name__ == "__main__":
    # 1st. matchId csv로 저장 (2번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = getMatchId.getGrandmasterMatchId()
    # with open('MatchId/GrandmasterMatchId.csv','w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(GrandmasterMatchId)
    
    # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)

    # API 두 개 사용해서 데이터 수집
    GrandmasterMatchId = GrandmasterMatchId.iloc[:, 5962:]
    # print(GrandmasterMatchId)
    secondSaveDataset.append_saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15, 5962)