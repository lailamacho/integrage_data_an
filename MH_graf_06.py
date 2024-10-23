import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from funkce import *

file_path = "./exporty/export_dovednosti_02.csv"
df = pd.read_csv(file_path, sep=';')

## MH_06: LINE CHART (spojnicový graf)
# osa x = věk; osa y = počet; každná linie zobrazuje jednu úroveň (nejlepší/ střední/ nejhorší)

sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df.columns if "sub_topic_points" in col]
total_points_cols = [col for col in df.columns if "sub_topic_total_points" in col]
total = int(df[total_points_cols].head(1).sum(axis=1))
kompetence = col_to_topic(sub_topic_cols[0])

df['sumicka'] = df[points_cols].sum(axis=1)
df_2 = df[['age', 'sumicka']].dropna().reset_index()

perces = []
ranks = []

for idx in range(len(df_2['age'].values)):
    perc = (df_2['sumicka'].iloc[idx]) / (total / 100)
    perces.append(perc)

df_2['percentes'] = perces

for x in df_2['percentes']:
    if x <= 33:
        ranks.append("Nejhorší úroveň")
    elif x > 33 and x <= 66:
        ranks.append("Střední úroveň")
    elif x > 66 and x <= 100:
        ranks.append("Nejlepší úroveň")

df_2['ranks'] = ranks

df_grouped = df_2.groupby(['age', 'ranks'], observed=False).size().reset_index(name='pocet')

nejlepsi_val = []
nejlepsi_age = []

stredni_val = []
stredni_age = []

nejhorsi_val = []
nejhorsi_age = []

for row in df_grouped[['age', 'pocet', 'ranks']].values:
    if row[2] == "Nejlepší úroveň":
        nejlepsi_val.append(row[1])
        nejlepsi_age.append(row[0])
    elif row[2] == "Střední úroveň":
        stredni_val.append(row[1])
        stredni_age.append(row[0])
    elif row[2] == "Nejhorší úroveň":
        nejhorsi_val.append(row[1])
        nejhorsi_age.append(row[0])

plt.figure(figsize=(6, 6))
sns.lineplot(x=nejlepsi_age, y=nejlepsi_val, color='green', marker="o", alpha=0.5, label="Nejlepší úroveň")
sns.lineplot(x=stredni_age, y=stredni_val, color='blue', marker="o", alpha=0.5, label="Střední úroveň")
sns.lineplot(x=nejhorsi_age, y=nejhorsi_val, color='red', marker="o", alpha=0.5, label='Nejhorší úroveň')
plt.xlim([int(df_grouped['age'].values.min())-1, int(df_grouped['age'].values.max())])
plt.xlabel('Věk')
plt.ylabel('Počet')
plt.title(f'Kompetence: {kompetence}')
plt.legend()
plt.show()