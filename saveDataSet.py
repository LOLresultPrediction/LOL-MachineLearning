import getDataset
import csv

def saveDataSetToCSV(matchIdSet, fileName, frame):
    fieldnames = getDataset.tempResult('KR_6714278507', 15)
    with open(fileName,'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames.keys())
        w.writeheader()
        for i in matchIdSet:
            dic_data = getDataset.tempResult(i, frame)
            w.writerow(dic_data)
            print(i)