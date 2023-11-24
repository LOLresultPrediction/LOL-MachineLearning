import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score # 정확도 함수
from catboost import CatBoostClassifier
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
import csv
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

rf = RandomForestClassifier(n_estimators=100, max_depth=10, max_leaf_nodes=100, random_state = 10)
lgbm = LGBMClassifier(n_estimators=100, max_depth=10, verbosity=0, min_data_in_leaf=30, random_state=10)
cat = CatBoostClassifier(iterations=100, depth=10, learning_rate=1, random_state=10)
et = ExtraTreesClassifier(n_estimators=100, random_state = 10)

tier = 'IRON'
result = {}
for min in range(5, 16):
    resultFilePath = f'Dataset/perMinuteDataset/result/{tier}.csv'
    df = pd.read_csv(f'Dataset/perMinuteDataset/{min}min/{tier}.csv')
    win_df = df[['Diff_FirstBLOOD', 'Diff_FirstDRAGON',
        'Diff_FirstHERALD', 'Diff_Firsttower', 'dragonType', 'WIN_invadeKill', 'WIN_invadeDeath','WIN_controlWARDPlaced', 
        'WIN_Kill_top', 'WIN_Kill_jgl', 'WIN_Kill_mid', 'WIN_Kill_ad', 'WIN_Kill_sup',
        'WIN_Death_top', 'WIN_Death_jgl', 'WIN_Death_mid', 'WIN_Death_ad', 'WIN_Death_sup', 
        'WIN_Asisst_top', 'WIN_Asisst_jgl', 'WIN_Asisst_mid', 'WIN_Asisst_ad', 'WIN_Asisst_sup',
        'WIN_LV_top', 'WIN_LV_jgl', 'WIN_LV_mid', 'WIN_LV_ad', 'WIN_LV_sup',
        'WIN_CS_top', 'WIN_CS_jgl', 'WIN_CS_mid', 'WIN_CS_ad', 'WIN_CS_sup',
        'WIN_jglCS_top', 'WIN_jglCS_jgl', 'WIN_jglCS_mid', 'WIN_jglCS_ad', 'WIN_jglCS_sup',
        'WIN_GOLD_top', 'WIN_GOLD_jgl', 'WIN_GOLD_mid', 'WIN_GOLD_ad', 'WIN_GOLD_sup',
        'WIN_WARDkill', 'WIN_Inhibitor','WIN_TOWERkill', 'WIN_WARDplaced']]
    lose_df = df[['Diff_FirstBLOOD', 'Diff_FirstDRAGON',
        'Diff_FirstHERALD', 'Diff_Firsttower', 'dragonType',
        'LOSE_invadeDeath', 'LOSE_invadeKill',
        'LOSE_controlWARDPlaced',
        'LOSE_Kill_top', 'LOSE_Kill_jgl', 'LOSE_Kill_mid', 'LOSE_Kill_ad', 'LOSE_Kill_sup',
        'LOSE_Death_top', 'LOSE_Death_jgl',
        'LOSE_Death_mid', 'LOSE_Death_ad', 'LOSE_Death_sup',
        'LOSE_Asisst_top', 'LOSE_Asisst_jgl', 'LOSE_Asisst_mid',
        'LOSE_Asisst_ad', 'LOSE_Asisst_sup',
        'LOSE_LV_top', 'LOSE_LV_jgl',
        'LOSE_LV_mid', 'LOSE_LV_ad', 'LOSE_LV_sup',
        'LOSE_CS_top', 'LOSE_CS_jgl',
        'LOSE_CS_mid', 'LOSE_CS_ad', 'LOSE_CS_sup',
        'LOSE_jglCS_top', 'LOSE_jglCS_jgl', 'LOSE_jglCS_mid', 'LOSE_jglCS_ad', 'LOSE_jglCS_sup',
        'LOSE_GOLD_top', 'LOSE_GOLD_jgl',
        'LOSE_GOLD_mid', 'LOSE_GOLD_ad', 'LOSE_GOLD_sup',
        'LOSE_WARDkill', 'LOSE_Inhibitor',
        'LOSE_TOWERkill', 'LOSE_WARDplaced']]
    colName = 'WIN'
    win_df = win_df.rename(columns={f'{colName}_invadeKill': 'invadeKill', f'{colName}_invadeDeath': 'invadeDeath', 
                                                    f'{colName}_controlWARDPlaced': 'controlWARDPlaced',
                                                    f'{colName}_Kill_top': 'Kill_top',f'{colName}_Kill_jgl': 'Kill_jgl',f'{colName}_Kill_mid': 'Kill_mid',f'{colName}_Kill_ad': 'Kill_ad', f'{colName}_Kill_sup': 'Kill_sup',
                                                    f'{colName}_Death_top': 'Death_top',f'{colName}_Death_jgl': 'Death_jgl',f'{colName}_Death_mid': 'Death_mid',f'{colName}_Death_ad': 'Death_ad',f'{colName}_Death_sup': 'Death_sup',
                                                    f'{colName}_Asisst_top': 'Assist_top',f'{colName}_Asisst_jgl': 'Assist_jgl',f'{colName}_Asisst_mid': 'Assist_mid',f'{colName}_Asisst_ad': 'Assist_ad',f'{colName}_Asisst_sup': 'Assist_sup',
                                                    f'{colName}_LV_top': 'LV_top',f'{colName}_LV_jgl': 'LV_jgl',f'{colName}_LV_mid': 'LV_mid',f'{colName}_LV_ad': 'LV_ad',f'{colName}_LV_sup': 'LV_sup',
                                                    f'{colName}_CS_top': 'CS_top',f'{colName}_CS_jgl': 'CS_jgl',f'{colName}_CS_mid': 'CS_mid',f'{colName}_CS_ad': 'CS_ad',f'{colName}_CS_sup': 'CS_sup',
                                                    f'{colName}_jglCS_top': 'jglCS_top',f'{colName}_jglCS_jgl': 'jglCS_jgl',f'{colName}_jglCS_mid': 'jglCS_mid',f'{colName}_jglCS_ad': 'jglCS_ad',f'{colName}_jglCS_sup': 'jglCS_sup',
                                                    f'{colName}_GOLD_top': 'GOLD_top',f'{colName}_GOLD_jgl': 'GOLD_jgl',f'{colName}_GOLD_mid': 'GOLD_mid',f'{colName}_GOLD_ad': 'GOLD_ad',f'{colName}_GOLD_sup': 'GOLD_sup',
                                                    f'{colName}_WARDkill': 'WARDkill',f'{colName}_Inhibitor': 'Inhibitor',f'{colName}_TOWERkill': 'TOWERkill',f'{colName}_WARDplaced': 'WARDplaced'})

    colName = 'LOSE'
    lose_df = lose_df.rename(columns={f'{colName}_invadeKill': 'invadeKill', f'{colName}_invadeDeath': 'invadeDeath', 
                                                    f'{colName}_controlWARDPlaced': 'controlWARDPlaced',
                                                    f'{colName}_Kill_top': 'Kill_top',f'{colName}_Kill_jgl': 'Kill_jgl',f'{colName}_Kill_mid': 'Kill_mid',f'{colName}_Kill_ad': 'Kill_ad', f'{colName}_Kill_sup': 'Kill_sup',
                                                    f'{colName}_Death_top': 'Death_top',f'{colName}_Death_jgl': 'Death_jgl',f'{colName}_Death_mid': 'Death_mid',f'{colName}_Death_ad': 'Death_ad',f'{colName}_Death_sup': 'Death_sup',
                                                    f'{colName}_Asisst_top': 'Assist_top',f'{colName}_Asisst_jgl': 'Assist_jgl',f'{colName}_Asisst_mid': 'Assist_mid',f'{colName}_Asisst_ad': 'Assist_ad',f'{colName}_Asisst_sup': 'Assist_sup',
                                                    f'{colName}_LV_top': 'LV_top',f'{colName}_LV_jgl': 'LV_jgl',f'{colName}_LV_mid': 'LV_mid',f'{colName}_LV_ad': 'LV_ad',f'{colName}_LV_sup': 'LV_sup',
                                                    f'{colName}_CS_top': 'CS_top',f'{colName}_CS_jgl': 'CS_jgl',f'{colName}_CS_mid': 'CS_mid',f'{colName}_CS_ad': 'CS_ad',f'{colName}_CS_sup': 'CS_sup',
                                                    f'{colName}_jglCS_top': 'jglCS_top',f'{colName}_jglCS_jgl': 'jglCS_jgl',f'{colName}_jglCS_mid': 'jglCS_mid',f'{colName}_jglCS_ad': 'jglCS_ad',f'{colName}_jglCS_sup': 'jglCS_sup',
                                                    f'{colName}_GOLD_top': 'GOLD_top',f'{colName}_GOLD_jgl': 'GOLD_jgl',f'{colName}_GOLD_mid': 'GOLD_mid',f'{colName}_GOLD_ad': 'GOLD_ad',f'{colName}_GOLD_sup': 'GOLD_sup',
                                                    f'{colName}_WARDkill': 'WARDkill',f'{colName}_Inhibitor': 'Inhibitor',f'{colName}_TOWERkill': 'TOWERkill',f'{colName}_WARDplaced': 'WARDplaced'})
    win_df['result'] = 1
    lose_df['result'] = -1
    data = pd.concat([win_df, lose_df], axis=0, ignore_index=True)
    colCnt = data.shape[1]
    print(colCnt)
    X = data.iloc[:, :colCnt-1]
    y = data.iloc[:, colCnt-1:]
    # # features/target, train/test dataset 분리
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42) # 학습데이터와 평가데이터의 비율을 8:2 로 분할|
    y_train = y_train.values.ravel()
    modelList = [rf, lgbm, cat, et]
    modelNameList = ["RandomForest", "LightGBM", "CatBoost", "ExtraTree"]
    fieldnames = ["Minute", "Model", "accuracy_score", "F1_score", "ROC_AUC", "TN", "FP", "FN", "TP"]
    for i in range(4):
        model = modelList[i]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42) # 학습데이터와 평가데이터의 비율을 8:2 로 분할|
        model.fit(X_train, y_train)
        pre = model.predict(X_test)
        accuracy = round(accuracy_score(y_test, pre)*100, 2)
        f1 = round(f1_score(y_test, pre)*100, 2)
        roc_auc = round(roc_auc_score(y_test, pre)*100, 2)
        tn, fp, fn, tp = confusion_matrix(y_test, pre).ravel()
        print(f"{modelNameList[i]} Accuracy : ", accuracy, "%")
        print(f"{modelNameList[i]} f1 :", f1, "%")
        print(f"{modelNameList[i]} ROC_AUC :", roc_auc, "%")
        print('tn:', tn, ' fp:', fp, ' fn:', fn, ' tp:', tp)

        result = {"Minute": min, 
                  "Model": f"{modelNameList[i]}", 
                  "accuracy_score" : accuracy,
                  "F1_score" : f1,
                  "ROC_AUC" : roc_auc,
                  "TN": tn,
                  "FP": fp,
                  "FN": fn,
                  "TP": tp}
        # result = pd.DataFrame(result, index = [0])
        # result.to_csv(resultFilePath, index=False)
        with open(resultFilePath, 'a', newline='') as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            if min == 5 and i == 0:
                w.writeheader()
            w.writerow(result)