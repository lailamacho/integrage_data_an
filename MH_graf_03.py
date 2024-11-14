import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import math
from funkce import *

file_path = "./exporty/export_tech_zdat_02.csv"  # NUTNO MĚNIT ÚDAJE!!!
df = pd.read_csv(file_path, sep=";")


## MH_03: STACKED BAR CHART(skládaný sloupcový graf) - porovnání regionů a jednotlivých výsledků z dotazníku

sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df.columns if "sub_topic_points" in col]
total_points_cols = [col for col in df.columns if "sub_topic_total_points" in col]
kompetence = col_to_topic(sub_topic_cols[0])

df_2 = pd.DataFrame(columns=['country','sub_topic', 'rank'])

for idx, sub_topic in enumerate(sub_topic_cols):
    perc = df[points_cols[idx]] / (df[total_points_cols[idx]] / 100)
    df['perc'] = perc
    df['rank'] = pd.cut(
        df['perc'],
        bins=[0, 33, 66, 100],
        labels=["Nejhorší úroveň", "Střední úroveň", "Nejlepší úroveň"])
    
    temp_df = df[['country', sub_topic, 'rank']].dropna()
    temp_df.columns = ['country', 'sub_topic', 'rank']
    df_2 = pd.concat([df_2, temp_df], axis=0)

df_grouped = df_2.groupby(['sub_topic', 'country', 'rank'], observed=False).size().reset_index(name='counts')
sub_topics = df_2['sub_topic'].unique()


# vykreslení
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(nrows=math.ceil(len(sub_topics) / 2), ncols=2, figsize=(16, 10))
labels=["Nejhorší úroveň", "Střední úroveň", "Nejlepší úroveň"]
palette = sns.color_palette("Set1", n_colors=3)

axes = axes.flatten()

for idx, sub_topic in enumerate(sub_topics):
    sub_topic_data = df_grouped[df_grouped['sub_topic'] == sub_topic]
    
    countries = sub_topic_data['country'].unique()
    ranks = sub_topic_data['rank'].unique()
    
    bottom_values = np.zeros(len(countries)) #inicializace hodnot pro skladani (vsechny od 0)

    for rank_idx, rank in enumerate(ranks):
        rank_data = sub_topic_data[sub_topic_data['rank'] == rank]
        rank_counts = rank_data.set_index('country').reindex(countries)['counts'].fillna(0)
        
        axes[idx].bar(
            countries,
            rank_counts,
            bottom=bottom_values,
            label=rank,
            color=palette[rank_idx]
        )
        bottom_values += rank_counts

    axes[idx].set_title(f'{sub_topic}')
    axes[idx].set_xlabel('')
    axes[idx].set_ylabel('Počet')
    axes[idx].tick_params(axis='x', rotation=45)

fig.legend(labels=labels, fontsize='small', markerfirst=False, draggable=True)
fig.suptitle(f'Výsledky v jednotlivých podtématech v dotazníku: {kompetence}')
plt.tight_layout(rect=[0, 0, 1, 0.95])
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')
plt.show()