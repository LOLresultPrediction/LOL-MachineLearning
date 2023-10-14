import getDataset
import csv

def saveDataSetToCSV(matchId, frame):
    dataset = getDataset.tempResult(matchId, frame) 
    dataset['matchId'] = matchId #매치 아이디 값을 불러오기 위한 작업
    csv_file_name = f"{matchId}_frame{frame}_data.csv"

    #딕셔너리 키, 값 형태로 엑셀에 불러옴. (키값이 엑셀의 행이되고 열이 딕셔나리의 값이 오게된다.)
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

    # 저장하는 로직
    with open(csv_file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(dataset)