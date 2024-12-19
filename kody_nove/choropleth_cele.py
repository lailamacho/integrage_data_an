import plotly
import pandas as pd
import plotly.express as px
from pycountry import countries
from funkce import *
from typing import List

file_path_1 = "./exporty_dat/OS_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_2 = "./exporty_dat/OS_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!
df_1 = pd.read_csv(file_path_1, sep=";")
df_2 = pd.read_csv(file_path_2, sep=";")
od = "8. 10. 2024"
do = "11. 12. 2024"

df = pd.concat([df_1, df_2], axis=0, ignore_index=True)

make_for_subtopics = False ## NUTNO MĚNIT

choice = ['mean', 'modus', 'median']

df_f_age = df[df['age']>=50]
sub_topic_cols = [col for col in df_f_age.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df_f_age.columns if "sub_topic_points" in col]
kompetence = col_to_topic(sub_topic_cols[0])

df_filtred = df_f_age[points_cols]
df_filtred['country'] = df['country']

def choropleth(df_filtred: pd.DataFrame, choice:List, sub_topic:bool, col=None, col_2=None):
    if sub_topic == False:
        work_with = 'achieved'
    else:
        work_with = col

    for operace in choice:
        if operace == 'modus':
            popisek = "Modus"
            df_filtred['modus'] = df_filtred.groupby(['country'])[work_with].transform(lambda x: pd.Series.mode(x)[0] if not pd.Series.mode(x).empty else None)
        elif operace == 'mean':
            popisek = "Průměr"
            df_filtred['mean'] = df_filtred[['country', work_with]].groupby(['country']).transform('mean')
        elif operace == 'median':
            popisek = "Medián"
            df_filtred['median'] = df_filtred[['country', work_with]].groupby(['country']).transform('median')
        data = df_filtred[['country', operace]].drop_duplicates(keep='first').dropna().reset_index()
        data["country"] = data["country"].apply(lambda x: countries.get(alpha_2=x).alpha_3 if countries.get(alpha_2=x) else x)

        if sub_topic == False:
            title = f"{popisek} získaných bodů z dotazníku: {kompetence} <br>z období od {od} do {do}"
            nazev = kompetence
            filename = f"CH_{operace}_{nazev}"

        else:
            title = f"{popisek} získaných bodů z dotazníku: {kompetence}, v podtématu: {col_to_name(col_2)} <br>z období od {od} do {do}"
            nazev = col_to_name(col_2)
            filename = f"CH_{operace}_{nazev}"



        fig = px.choropleth(
            data,
            locations='country',
            locationmode='ISO-3',
            color=operace,
            hover_name=operace,
            color_continuous_scale='magenta',
            scope='europe',
            labels={operace: popisek}
        )

        fig.update_layout(
            title=title,
            geo=dict(
                showframe=False, 
                showcoastlines=True,
                #projection_type="mercator",
                center=dict(lat=46.4660, lon=16.96),
                projection=dict(scale=4)
            )
        )
        plotly.offline.plot(fig, filename=f'./grafy/{filename}.html')
    fig.show()


if make_for_subtopics == False:
    df_filtred['achieved'] = df_filtred.sum(axis=1, numeric_only=True)
    df_filtred = df_filtred[['country', 'achieved']].dropna()
    choropleth(df_filtred, choice, False)

else:
    for col, col_2 in zip(points_cols, sub_topic_cols):
        choropleth(df_filtred, choice, True, col, col_2)