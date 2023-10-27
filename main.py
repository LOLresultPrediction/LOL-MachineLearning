import pprint
import numpy as np
import getAPI
import getLoseDataset
import getMatchId
import csv
import pandas as pd
import saveWinDataset
import saveLoseDataset
import saveLoseDataset

pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
    #1st. matchId csv로 저장 (주석 해제)
    # SilverMatchId = getMatchId.getMatchIdByTierAndRank("SILVER", "IV", 1, 2)
    # with open('MatchId/SilverMatchId_IV.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(SilverMatchId)
    
    # # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)
    #print(getAPI.getGameInfo('KR_6714278507'))


    # API 2개 사용할 때
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # secondSaveDataset.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 1869
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, stopIndex:]
    # secondSaveDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, stopIndex)
    
    Grandmaster = pd.read_csv('Dataset/win/Grandmaster.csv')
    saveLoseDataset.save_dataframe_to_csv(Grandmaster,'Dataset/lose/Grandmaster.csv')