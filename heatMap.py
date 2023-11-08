import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# win_10_Chanllenger = pd.read_csv('Dataset/win_10/10_Chanllenger.csv')
# lose_10_Chanllenger = pd.read_csv('Dataset/lose_10/10_Chanllenger_lose.csv')

win_10_Grandmaster = pd.read_csv('Dataset/win_10/10_Grandmaster.csv')
lose_10_Grandmaster = pd.read_csv('Dataset/lose_10/10_Grandmaster.csv')

# win_10_Chanllenger = pd.read_csv('Dataset/win/Bronze_I.csv')
# lose_10_Chanllenger = pd.read_csv('Dataset/lose/Bronze_I_lose.csv')

df = pd.concat([win_10_Grandmaster, lose_10_Grandmaster], ignore_index=True)
df= df.drop(['matchId'],axis=1)
df= df.drop(['queueId'],axis=1)
df= df.drop(['K-WIN-top'],axis=1)
df= df.drop(['K-LOSE-top'],axis=1)
df= df.drop(['K-WIN-jug'],axis=1)
df= df.drop(['K-LOSE-jug'],axis=1)
df= df.drop(['K-WIN-mid'],axis=1)
df= df.drop(['K-LOSE-mid'],axis=1)
df= df.drop(['K-WIN-ad'],axis=1)
df= df.drop(['K-LOSE-ad'],axis=1)
df= df.drop(['K-WIN-sup'],axis=1)
df= df.drop(['K-LOSE-sup'],axis=1)
# df= df.drop(['Diff-K'],axis=1)
# df= df.drop(['Diff-A'],axis=1)
# df= df.drop(['Diff_LV'],axis=1)
df= df.drop(['LOSE_controlWARDPlaced'],axis=1)
df= df.drop(['WIN_controlWARDPlaced'],axis=1)
# df= df.drop(['result'],axis=1)

columns = np.array(df.columns)
# print(columns)
df_small = df[columns]
# print(df_small)
df_corr = df_small.corr()
print(df.corr()['result'])
# print(df_corr)
plt.figure(figsize=(10,10))
sns.heatmap(df_corr, annot=True, cmap="Blues")

plt.show()