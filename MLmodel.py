import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score # 정확도 함수
from catboost import CatBoostClassifier


win_Chanllenger = pd.read_csv('Dataset/win/Chanllenger.csv')
lose_Chanllenger = pd.read_csv('Dataset/lose/Chanllenger.csv')

win_10_Chanllenger = pd.read_csv('Dataset/win_10/win_10_Chanllenger.csv')
lose_10_Chanllenger = pd.read_csv('Dataset/lose_10/lose_10_Chanllenger.csv')

win_Grandmaster = pd.read_csv('Dataset/win/Grandmaster.csv')
lose_Grandmaster = pd.read_csv('Dataset/lose/Grandmaster.csv')

win_10_Grandmaster = pd.read_csv('Dataset/win_10/win_10_Grandmaster.csv')
lose_10_Grandmaster = pd.read_csv('Dataset/lose_10/lose_10_Grandmaster.csv')

data = pd.concat([win_10_Grandmaster, lose_10_Grandmaster], ignore_index=True)
# data = pd.concat([win_10_Chanllenger, lose_10_Chanllenger], ignore_index=True)
# data = data[data["queueId"] == 420]
# # 무의미한 변수 제거
data= data.drop(['matchId'],axis=1)
data= data.drop(['queueId'],axis=1)
data= data.drop(['K-WIN-top'],axis=1)
data= data.drop(['K-LOSE-top'],axis=1)
data= data.drop(['K-WIN-jug'],axis=1)
data= data.drop(['K-LOSE-jug'],axis=1)
data= data.drop(['K-WIN-mid'],axis=1)
data= data.drop(['K-LOSE-mid'],axis=1)
data= data.drop(['K-WIN-ad'],axis=1)
data= data.drop(['K-LOSE-ad'],axis=1)
data= data.drop(['K-WIN-sup'],axis=1)
data= data.drop(['K-LOSE-sup'],axis=1)
data= data.drop(['LOSE_controlWARDPlaced'],axis=1)
data= data.drop(['WIN_controlWARDPlaced'],axis=1)

X = data.iloc[:, :21]
y = data.iloc[:, 21:]

# # features/target, train/test dataset 분리
train_x, test_x, train_y, test_y = train_test_split(X, y, test_size = 0.3, random_state = 42) # 학습데이터와 평가데이터의 비율을 8:2 로 분할| 

# #기본적인 randomforest모형

rf = RandomForestClassifier(n_estimators=100, max_depth=20,random_state=0)
rf.fit(train_x,train_y)

lgbm = LGBMClassifier(n_estimators=100)
lgbm.fit(train_x, train_y)

cat = CatBoostClassifier(iterations=2, depth=2, learning_rate=1)
cat.fit(train_x, train_y)

et = ExtraTreesClassifier(n_estimators=100, random_state=0)
et.fit(train_x, train_y)

rf_pre = rf.predict(test_x)
lgbm_pre = lgbm.predict(test_x)
cat_pre = cat.predict(test_x)
et_pre = et.predict(test_x)

print("RandomForest :", round(accuracy_score(test_y, rf_pre)*100, 2), "%")
print("lightGBM :", round(accuracy_score(test_y, lgbm_pre)*100, 2), "%")
print("CatBoost :", round(accuracy_score(test_y, cat_pre)*100, 2), "%")
print("ExtraTrees :", round(accuracy_score(test_y, et_pre)*100, 2), "%")