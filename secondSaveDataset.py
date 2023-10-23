import getDataset
import csv
import time

fieldnames = [
        'matchId',
        'queueId',
        'Diff-A',
        'Diff-K',
        'Diff_CS',
        'Diff_FirstBLOOD',
        'Diff_FirstDRAGON',
        'Diff_FirstHERALD',
        'Diff_Firsttower',
        'Diff_Inhibitor',
        'Diff_LV',
        'Diff_WARDkill',
        'Diff_WARDplaced',
        'Diff_jglCS',
        'dragonType',
        'result'
    ]
def saveDataSetToCSV(matchIdSet, fileName, frame):
    with open(fileName, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        i = 0
        for matchId in matchIdSet:
            i += 1
            try:
                if i%2 == 0:
                    dic_data = getDataset.getResult(matchId, frame, 1)
                else:
                    dic_data = getDataset.getResult(matchId, frame, 2)
            except KeyError:
                print("KeyError발생.. 20초 대기 후 재시도.. ")
                time.sleep(20)
                if i%2 == 0:
                    dic_data = getDataset.getResult(matchId, frame, 1)
                else:
                    dic_data = getDataset.getResult(matchId, frame, 2)
            if dic_data == 0:
                time.sleep(1.2)
                continue
            w.writerow(dic_data)
            print(f'{i} : {matchId}의 데이터 추가')
            time.sleep(1.2)

# 데이터 수집하다가 중간에 끊겼을 때 사용 (th에 최종 출력된 인덱스 번호 넣으면 됨)
def append_saveDataSetToCSV(matchIdSet, fileName, frame, th):
    with open(fileName, 'a', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        i = th
        for matchId in matchIdSet:
            i += 1
            try:
                if i%2 == 0:
                    dic_data = getDataset.getResult(matchId, frame, 1)
                else:
                    dic_data = getDataset.getResult(matchId, frame, 2)
            except KeyError:
                print("KeyError발생.. 20초 대기 후 재시도.. ")
                time.sleep(20)
                if i%2 == 0:
                    dic_data = getDataset.getResult(matchId, frame, 1)
                else:
                    dic_data = getDataset.getResult(matchId, frame, 2)
            if dic_data == 0:
                time.sleep(1.2)
                continue
            w.writerow(dic_data)
            print(f'{i} : {matchId}의 데이터 추가')
            time.sleep(1.2)
