import getDataset
import csv

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
        w = csv.DictWriter(f, fieldnames.keys())
        w.writeheader()
        for i in matchIdSet:
            dic_data = getDataset.tempResult(i, frame)
            w.writerow(dic_data)
            print(i)