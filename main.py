import pprint
import numpy as np
import getAPI
import getLoseDataset
import getMatchId
import csv
#import saveDataset
import pandas as pd
#import secondSaveDataset
import saveLoseDataset
import pandas as pd
import getDatasetConcat
import getPerMinDataset
import etcFunction
import saveWinDataset

pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
    #1st. matchId csv로 저장 (주석 해제)
    # tier = "PLATINUM" # 대문자 풀네임으로 작성
    # ranks = ["I", "II", "III", "IV"]
    # for rank in ranks:
    #     matchId = getMatchId.getMatchIdByTierAndRank(tier, rank, 1, 2)
    #     with open(f'MatchId/{tier}_{rank}.csv', 'w', newline='') as f:
    #         w = csv.writer(f)
    #         w.writerow(matchId)
    
    # 1.1 챌린저, 그마, 마스터 저장
    tier = "GRANDMASTER" # 대문자 풀네임으로 작성
    # matchId = getMatchId.getGrandmasterMatchId()
    # with open(f'MatchId/{tier}_ver2.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(matchId)
    
    # # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)


    # API 2개 사용할 때
    # for rank in ranks:
    #     matchId = pd.read_csv(f'MatchId/{tier}_{rank}.csv')
    #     saveWinDataset.saveDataSetToCSV(matchId, 15, tier)

    # 챌린저, 그마, 마스터 저장
    matchId = pd.read_csv(f'MatchId/{tier}_ver2.csv')
    stopIndex = 7
    matchId = matchId.iloc[:, stopIndex:]
    saveWinDataset.saveDataSetToCSV(matchId, 15, tier, stopIndex)

    # 패배 데이터셋 만들기
    # Chanllenger_ver2 = pd.read_csv('Dataset/win_10/10_Grandmaster.csv')
    # saveLoseDataset.save_dataframe_to_csv(Chanllenger_ver2,'Dataset/lose_10/LvKA_10_Grandmaster.csv')

    # data 중복 제거, 10000개로 슬라이싱 후 저장
    # data1 = pd.read_csv("Dataset/win/Platinum_I.csv")
    # data2 = pd.read_csv("Dataset/win/Platinum_II.csv")
    # data3 = pd.read_csv("Dataset/win/Platinum_III.csv")
    # data4 = pd.read_csv("Dataset/win/Platinum_IV.csv")
    # getDatasetConcat.Win_Lose_DataSet_Create(data1,data2,data3,data4,'Platinum')

    # 5분부터 15분까지의 데이터 저장
    # getPerMinDataset.getResult('KR_6710383118', 15, 1, 'DIAMOND')


    # 게임 내의 participantId와 champion name 가져오기
    # id = 6709531155
    # gameTimelineInfo = getAPI.getGameInfoTimeline(f'KR_{id}')['info']
    # etcFunction.getParticipantId_ChampionName('KR_6709531155')