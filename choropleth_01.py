import plotly
import pandas as pd
import plotly.express as px
from pycountry import countries
from funkce import *

filepath = "./exporty/export_dovednosti_02.csv"
df = pd.read_csv(filepath, sep=';')

df = df[['country', 'education']].dropna()
df_grouped = df.groupby(['country', 'education']).size().reset_index(name='count')
df_grouped["country"] = df_grouped["country"].apply(lambda x: countries.get(alpha_2=x).alpha_3 if countries.get(alpha_2=x) else x)

fig = px.choropleth(
    df_grouped,
    locations='country',
    locationmode='ISO-3',
    color='count',
    hover_name='education',
    color_continuous_scale='Viridis',
    scope='europe',
    labels={'count': 'Počet'}
)

fig.update_layout(
    title="Rozložení vzdělání dle zemí v Evropě",
    geo=dict(
        showframe=False, 
        showcoastlines=True,
        #projection_type="mercator",
        center=dict(lat=46.4660, lon=16.96),
        projection=dict(scale=4)
    )
)

custom_filename = input("Název souboru: ")
plotly.offline.plot(fig, filename=f'./grafy/{custom_filename}.html')
#fig.write_image("./grafy/ifeExp.png")
fig.show()