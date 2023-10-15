import getDataset
import csv
import time


def saveDataSetToCSV(matchIdSet, fileName, frame):
    fieldnames = [
        'matchId',
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
    with open(fileName,'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        i = 0
        for matchId in matchIdSet:
            i += 1
            dic_data = getDataset.getResult(matchId, frame)
            if dic_data == 0:
                continue
            w.writerow(dic_data)
            print(f'{i} : {matchId}의 데이터 추가')
            time.sleep(3)
