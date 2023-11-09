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
import getDatasetTemp
import etcFunction

pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
    
    #1st. matchId csv로 저장 (주석 해제)
    # ChallengerMatchId = getMatchId.getChallengerMatchId()
    # with open('MatchId/ChallengerMatchId_ver2.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(ChallengerMatchId)

    
    # # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)


    # API 2개 사용할 때
    # ChanllengerMatchId_ver2 = pd.read_csv('MatchId/ChanllengerMatchId_ver2.csv')
    # saveWinDataset.saveDataSetToCSV(ChanllengerMatchId_ver2, 'Dataset/ChanllengerMatchId_ver2.csv', 10)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 1869
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, stopIndex:]
    # secondSaveDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, stopIndex)
    
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
    # getDatasetTemp.getResult('KR_6710383118', 15, 1)

    # 게임 내의 participantId와 champion name 가져오기
    # id = 6709531155
    # gameTimelineInfo = getAPI.getGameInfoTimeline(f'KR_{id}')['info']
    # etcFunction.getParticipantId_ChampionName('KR_6709531155')
    # for i in range(0, 30):
    #     participantFrames = gameTimelineInfo['frames'][i]['participantFrames']['2']
    #     print(i, ' ', participantFrames['minionsKilled'])
    
    getDatasetTemp.getResult("KR_6709531155",10,2,'Bronze')
    