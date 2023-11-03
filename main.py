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
    # GoldMatchId = getMatchId.getMatchIdByTierAndRank("GOLD", "I", 1, 2)
    # with open('MatchId/GoldMatchId_I.csv', 'w', newline='') as f:
    #     w = csv.writer(f)
    #     w.writerow(GoldMatchId)
    
    # # 2nd. 불러온 matchId로 데이터셋 csv로 저장 (1번 코드 주석 처리하고 돌리기)
    # GrandmasterMatchId = pd.read_csv('MatchId/GrandmasterMatchId.csv')
    # saveDataSet.saveDataSetToCSV(GrandmasterMatchId, 'Dataset/Grandmaster.csv', 15)
    #print(getAPI.getGameInfo('KR_6714278507'))


    # API 2개 사용할 때
    # ChanllengerMatchId = pd.read_csv('MatchId/ChanllengerMatchId.csv')
    # secondSaveDataset.saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15)

    # 데이터 수집 중단되면 중단된 matchId의 인덱스 번호 넣고 이어서 수집
    # stopIndex = 1869
    # ChanllengerMatchId = ChanllengerMatchId.iloc[:, stopIndex:]
    # secondSaveDataset.append_saveDataSetToCSV(ChanllengerMatchId, 'Dataset/Chanllenger.csv', 15, stopIndex)
    
    # 패배팀 Dataset 생성
    import pandas as pd
    
    dataframe = pd.read_csv("Dataset/win/Gold_I.csv")
    
    saveLoseDataset.save_dataframe_to_csv(dataframe,"Dataset/lose/Gold_I_lose.csv")

# def process_and_save_dataframe(input_filename, output_filename):
#     Loseteam = pd.read_csv(input_filename)
#     df = pd.DataFrame(Loseteam)

#     columns_to_exclude_index = [0, 1, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 26, 34]
#     columns_to_multiply_by_minus_1_index = [col_idx for col_idx in range(len(df.columns)) if col_idx not in columns_to_exclude_index]
#     df.iloc[:, columns_to_multiply_by_minus_1_index] = df.iloc[:, columns_to_multiply_by_minus_1_index] * -1

#     df.to_csv(output_filename, index=False)

# process_and_save_dataframe("Dataset/win/Silver_I.csv", "Dataset/lose/Silver_I_lose_new.csv")
    
