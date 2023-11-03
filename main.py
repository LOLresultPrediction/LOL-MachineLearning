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



pp = pprint.PrettyPrinter(indent=4)


if __name__ == "__main__":
    #1st. matchId csv로 저장 (주석 해제)
<<<<<<< HEAD
    # ChallengerMatchId = getMatchId.getChallengerMatchId()
    # with open('MatchId/ChallengerMatchId_ver2.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(ChallengerMatchId)
=======
    # GoldMatchId = getMatchId.getMatchIdByTierAndRank("GOLD", "I", 1, 2)
    # with open('MatchId/GoldMatchId_I.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(GoldMatchId)
>>>>>>> daa6ae62a1e485b25347e89c2d27519d12668ec0
    
    # # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)
    #print(getAPI.getGameInfo('KR_6714278507'))


    # API 2개 사용할 때
<<<<<<< HEAD
    # ChanllengerMatchId_ver2 = pd.read_csv('MatchId/ChanllengerMatchId_ver2.csv')
    # saveWinDataset.saveDataSetToCSV(ChanllengerMatchId_ver2, 'Dataset/ChanllengerMatchId_ver2.csv', 10)
=======
    # ChanllengerMatchId = pd.read_csv('MatchId/ChanllengerMatchId.csv')
    # secondSaveDataset.saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15)
>>>>>>> daa6ae62a1e485b25347e89c2d27519d12668ec0

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 1869
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, stopIndex:]
    # secondSaveDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, stopIndex)
    
<<<<<<< HEAD
    # 패배 데이터셋 만들기
    Chanllenger_ver2 = pd.read_csv('Dataset/win/Chanllenger_ver2.csv')
    saveLoseDataset.save_dataframe_to_csv(Chanllenger_ver2,'Dataset/lose/Chanllenger_ver2.csv')
=======
    # 패배팀 Dataset 생성
    def save_dataframe_to_csv(dataframe, filename):
        dataframe.to_csv(filename, index=False)
    Loseteam = pd.read_csv("Dataset/win/SilverI.csv")
    df = pd.DataFrame(Loseteam)
    columns_to_drop = [0, 1, 7, 8, 10, 11, 13, 14, 16, 17, 19, 22, 26, 27]
    df = df.drop(df.columns[columns_to_drop], axis=1)
    df = df * -1
    df['dragonType'] = df['dragonType'] * -1
    save_dataframe_to_csv(df,'Dataset/Lose/SilverI.csv')
>>>>>>> daa6ae62a1e485b25347e89c2d27519d12668ec0
