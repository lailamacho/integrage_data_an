import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from funkce import *
from typing import List
from random import randint

file_path_1 = "./exporty/stare/tech_zdat_24-10-01.csv"  # NUTNO MĚNIT ÚDAJE!!!
df_1 = pd.read_csv(file_path_1, sep=";")

file_path_2 = "./exporty/stare/dovednosti_24-10-01.csv"  # NUTNO MĚNIT ÚDAJE!!!
df_2 = pd.read_csv(file_path_2, sep=";")

file_path_3 = "./exporty/stare/os_rozv_24-10-01.csv"  # NUTNO MĚNIT ÚDAJE!!!
df_3 = pd.read_csv(file_path_3, sep=";")

zvolena_zeme_kod = "CZ"  # NUTNO MĚNIT ÚDAJE
#zvolena_zeme_kod = input()


## MH_04: PIE CHART - pro každý stát zvlášť výsledky ze všech tří dotazníků
assert zvolena_zeme_kod in country_code.keys(), f"Zadán nesprávný kód země. Kódy: {country_code}"

df_1_filtred = df_1.query(f'country == "{zvolena_zeme_kod}"') 
df_2_filtred = df_2.query(f'country == "{zvolena_zeme_kod}"') 
df_3_filtred = df_3.query(f'country == "{zvolena_zeme_kod}"') 

data_frames = [df_1_filtred, df_2_filtred, df_3_filtred]

for df in data_frames:
    if not zvolena_zeme_kod in df['country'].values:
        raise ValueError("Pro zadanou zemi nebyla získána data.")

def names(dfs: List[pd.DataFrame]):
    names = []
    for df in dfs:
        cols = [col for col in df.columns if 'sub_topic' in col and len(col) <=12]
        name = col_to_topic(cols[0])
        names.append(name)
    return names

topic_names = names(data_frames)


#výpočet max., získaných a chybějících bodů v topicu (dotazní / kompetence)

def compute_points_in_topic(dfs: List[pd.DataFrame]):
    """
    Výpočet max. a získaných bodů v topicu (kompetence / dotazník) z vloženého seznamu dataframů.
    """
    max_points_topic = []
    achieved_points_topic = []

    for df in dfs:
        max_points_cols = [col for col in df.columns if "sub_topic_total_points" in col]
        points_cols = [col for col in df.columns if "sub_topic_points" in col]
        df_for_sum_max = df[max_points_cols].head(1)
        df_for_sum_achieved = df[points_cols].head(1)

        sum_max_df =  int(df_for_sum_max.sum(axis=1)) #TODO: fix -> FutureWarning: Calling int on a single element Series is deprecated and will raise a TypeError in the future. Use int(ser.iloc[0]) instead
        sum_achieved_df = int(df_for_sum_achieved.sum(axis=1))

        max_points_topic.append(sum_max_df)
        achieved_points_topic.append(sum_achieved_df)

    return max_points_topic, achieved_points_topic
    
max_points, achieved_points = compute_points_in_topic(data_frames)
missing_points = [x - y for x, y in zip(max_points, achieved_points)]


# výpočty graf pro graf: celkový počet bodů -> 100% grafu; % díly každého topicu
chart_max = sum(max_points)
perc_achieved = [x / chart_max * 100 for x in achieved_points]
perc_missing = [x / chart_max * 100 for x in missing_points]

labels = []
for idx, name in enumerate(topic_names):
    labels.append(f'{name} - dosažené')
    labels.append(f'{name} - chybějící body')

proportions = []
for achieved, missing in zip(perc_achieved, perc_missing):
    proportions.append(achieved)
    proportions.append(missing)


# vykreslení A) chybějící body rozdělené dle topiců
sns.set_theme(style="whitegrid")
colors = sns.color_palette("Paired", len(proportions))

fig = plt.figure(figsize=(8, 8))
plt.pie(proportions, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
plt.title(f'Podíl dosažených bodů ze všech tří dotazníků pro zemi: {country_code[zvolena_zeme_kod][0]}')
plt.legend(labels, draggable=True, loc='lower center', bbox_to_anchor=(1, 0, 0.5, 1))
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')


# vykreslení B) chybějící body jako jedna část
total_missing_points = sum(max_points) - sum(achieved_points)
perc_total_missing = total_missing_points / chart_max * 100

labels_2 = topic_names + ['Chybějící body']
proportions_2 = perc_achieved + [perc_total_missing]
colors_2 = sns.color_palette("pastel", len(topic_names)) + ['#d3d3d3']

fig = plt.figure(figsize=(8, 8))
plt.pie(proportions_2, colors=colors_2, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
plt.title(f'Podíl dosažených bodů ze všech tří dotazníků pro zemi: {country_code[zvolena_zeme_kod][0]}')
plt.legend(labels_2, draggable=True, loc='lower center', bbox_to_anchor=(1, 0, 0.5, 1))
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')
plt.show()