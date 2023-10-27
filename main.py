import pprint
import numpy as np
import getAPI
import getLoseDataset
import getMatchId
import csv
import saveDataset
import pandas as pd
import saveWinDataset
import saveLoseDataset

pp = pprint.PrettyPrinter(indent=4)


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
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveWinDataset.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 1869
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, stopIndex:]
    # saveWinDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, stopIndex)

    # 패배 데이터셋 수집
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveLoseDataset.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/lose/Grandmaster.csv', 15)

    gameinfo = getAPI.getGameInfo('KR_6710383118')
    pp.pprint(gameinfo['info']['teams'])