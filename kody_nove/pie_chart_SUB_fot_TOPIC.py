import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from funkce import *
from typing import List

file_path_1 = "./exporty_dat/OS_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_2 = "./exporty_dat/OS_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!
df_1 = pd.read_csv(file_path_1, sep=";")
df_2 = pd.read_csv(file_path_2, sep=";")
od = "8. 10. 2024"
do = "11. 12. 2024"

df = pd.concat([df_1, df_2], axis=0, ignore_index=True)
df_f_age = df[df['age']>=50]

zvolena_zeme_kod = "CZ"  # NUTNO MĚNIT ÚDAJE
#zvolena_zeme_kod = input()
sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df.columns if "sub_topic_points" in col]
max_points_cols = [col for col in df.columns if "sub_topic_total_points" in col]

kompetence = col_to_topic(sub_topic_cols[0])

if 'sub_topic_19' in sub_topic_cols:
    sub_topic_cols.remove('sub_topic_19')
    points_cols.remove('sub_topic_points_19')
    max_points_cols.remove('sub_topic_total_points_19')

subtopic_names = []
for col in sub_topic_cols:
    subtopic_names.append(col_to_name(col))

## MH_04: PIE CHART - pro každý stát zvlášť výsledky ze všech tří dotazníků
assert zvolena_zeme_kod in country_code.keys(), f"Zadán nesprávný kód země. Kódy: {country_code}"
df_filtred = df.query(f'country == "{zvolena_zeme_kod}"') 

if not zvolena_zeme_kod in df['country'].values:
    raise ValueError("Pro zadanou zemi nebyla získána data.")


## výpočet max., získaných a chybějících bodů v topicu (dotazník / kompetence)
def compute_points_in_subtopic(df: pd.DataFrame, points_cols, max_points_cols):
    """
    Výpočet získaných, maximálních a chybějících bodů pro všechny subtopics.
    """
    achieved_points_subtopics = []
    max_points_subtopics = []
    missing_points_subtopisc = []

    for col_1, col_2 in zip(points_cols, max_points_cols):
        achieved_points = df[col_1].sum(axis=0)
        help_max_points = df[col_2].sum(axis=0)
        missing_points = help_max_points - achieved_points

        achieved_points_subtopics.append(achieved_points)
        max_points_subtopics.append(df[col_2].head(1))
        missing_points_subtopisc.append(missing_points)

    return achieved_points_subtopics, max_points_subtopics, missing_points_subtopisc

achieved_points, max_points, missing_points= compute_points_in_subtopic(df_filtred, points_cols, max_points_cols)
chart_max = sum(max_points)

perc_achieved = [x / chart_max * 100 for x in achieved_points]
total_missing_points = sum(missing_points)
perc_total_missing = total_missing_points / chart_max * 100

sns.set_theme(style="whitegrid")
my_colours = ['#da5c57', '#f68a42','#9aca3c', '#18baa8','#00addc', '#003399b3']
labels = subtopic_names + ['Chybějící body']
proportions = perc_achieved + [perc_total_missing]
colors = my_colours[0:len(sub_topic_cols)] + ['#d3d3d3']#sns.color_palette("pastel", len(sub_topic_cols)) + ['#d3d3d3']

fig = plt.figure(figsize=(8, 8))
plt.pie(pd.Series(proportions), colors=colors, autopct='%1.1f%%', startangle=90)
plt.title(f"Rozložení získaných bodů v podtématech dotazníku: {kompetence} \npro zemi: {country_code[zvolena_zeme_kod][0]} \nv období od {od} do {do}",loc='left')
plt.axis('equal')
plt.legend(labels, draggable=True, loc='lower center', bbox_to_anchor=(1, 0, 0.5, 1))
filename = f"{kompetence}_pie-chart"
fig.savefig(f"./grafy/top/{filename}.png", dpi=300, bbox_inches='tight')
plt.show()