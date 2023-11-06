import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# win_10_Chanllenger = pd.read_csv('Dataset/win_10/10_Chanllenger.csv')
# lose_10_Chanllenger = pd.read_csv('Dataset/lose_10/10_Chanllenger_lose.csv')

win_10_Chanllenger = pd.read_csv('Dataset/win_10/10_Grandmaster.csv')
lose_10_Chanllenger = pd.read_csv('Dataset/lose_10/10_Grandmaster.csv')

# win_10_Chanllenger = pd.read_csv('Dataset/win/Bronze_I.csv')
# lose_10_Chanllenger = pd.read_csv('Dataset/lose/Bronze_I_lose.csv')

df = pd.concat([win_10_Chanllenger, lose_10_Chanllenger], ignore_index=True)
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
df= df.drop(['LOSE_controlWARDPlaced'],axis=1)
df= df.drop(['WIN_controlWARDPlaced'],axis=1)
# df= df.drop(['result'],axis=1)

columns = np.array(df.columns)
df_small = df[columns]
df_corr = df_small.corr()

plt.figure(figsize=(10,10))
sns.heatmap(df_corr, annot=True, fmt=".2f", cmap="Blues")

plt.show()