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
    # saveWinDataset.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/10_win_Grandmaster.csv', 10)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 2049
    # GrandmasterMatchId = GrandmasterMatchId.iloc[:, stopIndex:]
    # saveWinDataset.append_saveDataSetToCSV(GrandmasterMatchId, 'Dataset/10_win_Grandmaster.csv', 10, stopIndex)
    
    # 패배 데이터셋 만들기
    Silver_I = pd.read_csv('Dataset/10_win_Grandmaster.csv')
    saveLoseDataset.save_dataframe_to_csv(Silver_I,'Dataset/10_lose_Grandmaster.csv')