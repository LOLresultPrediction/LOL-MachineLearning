import pandas as pd

def Win_Lose_DataSet_Create(data1,data2,data3,data4, filename):
    
    def save_win_dataframe_to_csv(dataframe, filename):
        df = pd.DataFrame(dataframe)
        df.to_csv(filename, index=False)
        
    def save_lose_dataframe_to_csv(dataframe, filename):
        df = pd.DataFrame(dataframe)
        columns_to_exclude_index = [0, 1, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 26, 34]  
        columns_to_multiply_by_minus_1_index = [col_idx for col_idx in range(len(df.columns)) if col_idx not in columns_to_exclude_index]
        df.iloc[:, columns_to_multiply_by_minus_1_index] = df.iloc[:, columns_to_multiply_by_minus_1_index] * -1
        df.to_csv(filename, index=False)
        
    #승리팀 DataSet 만드는 코드
    #1. 우선 승리팀의 티어(1~4)를 read한다.
  
    #티어별로 2600개씩 슬라이싱 -> 나중에 data1~data4 까지 병합한 이후에 중복제거 하면 10000개로 하면 부족할수있으므로 2600개씩 10400개 수집
    data1 = data1.drop(data1.index[2600:])
    data2 = data2.drop(data2.index[2600:])
    data3 = data3.drop(data3.index[2600:])
    data4 = data4.drop(data4.index[2600:])

    #데이터 병합하는 과정 및 중복검사 및 제거 keep='first'로 하면 중복되는 값이 있을 경우 처음꺼는 살리고 이후 중복값은 제거 하는 것.
    windata = pd.concat([data1,data2,data3,data4])
    windata = windata.drop_duplicates(subset=['matchId'], keep='first')
    windata = windata.iloc[:10000] # 10400개에서 중복제거하고 10000개로 슬라이싱
    compare = windata[windata['matchId'].duplicated(keep=False)] # 중복이 있는지 확인해주는 로직
    save_win_dataframe_to_csv(windata,f"Dataset/win/{filename}_win.csv")
    print(windata)
    print(compare['matchId'])



    #패배팀 DataSet 생성
    losedata = pd.read_csv("Dataset/win/Platinum_win.csv") # 승리팀 10000개 DataSet을 그대로 가져와서 거기에 -1만 곱해주면 끝.
    save_lose_dataframe_to_csv(losedata, f"Dataset/lose/{filename}_lose.csv") #-1 곱해주고 저장해주는 함수

