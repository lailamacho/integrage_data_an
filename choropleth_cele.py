import plotly
import pandas as pd
import plotly.express as px
from pycountry import countries
from funkce import *
from random import randint
from typing import List

filepath = "./exporty/dovednosti_od_2024-10-14.csv"  ## NUTNO MĚNIT
df = pd.read_csv(filepath, sep=';')

make_for_subtopics = True  ## NUTNO MĚNIT

choice = ['mean', 'modus']

sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df.columns if "sub_topic_points" in col]
kompetence = col_to_topic(sub_topic_cols[0])

df_filtred = df[points_cols]
df_filtred['country'] = df['country']


def choropleth(df_filtred: pd.DataFrame, choice:List, sub_topic:bool, col=None, col_2=None):
    if sub_topic == False:
        work_with = 'achieved'
    else:
        work_with = col

    for operace in choice:
        if operace == 'modus':
            popisek = "modus"
            df_filtred['modus'] = df_filtred.groupby(['country'])[work_with].transform(lambda x: pd.Series.mode(x)[0] if not pd.Series.mode(x).empty else None)
        elif operace == 'mean':
            popisek = "průměr"
            df_filtred['mean'] = df_filtred[['country', work_with]].groupby(['country']).transform('mean')

        data = df_filtred[['country', operace]].drop_duplicates(keep='first').dropna().reset_index()
        data["country"] = data["country"].apply(lambda x: countries.get(alpha_2=x).alpha_3 if countries.get(alpha_2=x) else x)

        if sub_topic == False:
            title = f"{popisek} získaných bodů z dotazníku: {kompetence}"
            nazev = kompetence
        else:
            title = f"{popisek} získaných bodů z dotazníku: {kompetence}, v podtématu: {col_to_name(col_2)}"
            nazev = col_to_name(col_2)

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

        filename = f"{nazev}_{operace}_{randint(1, 50)}"
        plotly.offline.plot(fig, filename=f'./grafy/{filename}.html')

    fig.show()


if make_for_subtopics == False:
    df_filtred['achieved'] = df_filtred.sum(axis=1, numeric_only=True)
    df_filtred = df_filtred[['country', 'achieved']].dropna()
    choropleth(df_filtred, choice, False)

else:
    for col, col_2 in zip(points_cols, sub_topic_cols):
        choropleth(df_filtred, choice, True, col, col_2)
