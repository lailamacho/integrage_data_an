import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
from funkce import *

file_path = "./exporty/dovednosti_24-10-01.csv"  # NUTNO MĚNIT ÚDAJE!!!
df = pd.read_csv(file_path, sep=";")

## LM_01: BOXPLOT - rozložení bodů pro jednotlivé země v každém sub_topic za danou kompetenci

sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
points_cols = [col for col in df.columns if "sub_topic_points" in col]
kompetence = col_to_topic(sub_topic_cols[0])


df_long = pd.DataFrame(columns=['country', 'sub_topic', 'points'])

for idx, sub_topic in enumerate(sub_topic_cols):
    temp_df = df[['country']].copy()
    temp_df['sub_topic'] = sub_topic
    temp_df['points'] = df[points_cols[idx]]
    df_long = pd.concat([df_long, temp_df], axis=0).dropna()

df_long = df_long[df_long['sub_topic'] != 'sub_topic_19']

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(nrows=math.ceil(len(sub_topic_cols) / 2), ncols=2, figsize=(16, 10))
axes = axes.flatten()

sub_topics_filtred = df_long['sub_topic'].unique()

for idx, sub_topic in enumerate(sub_topics_filtred):
    sub_topic_data = df_long[df_long['sub_topic'] == sub_topic]
    
    sns.boxplot(
        data=sub_topic_data,
        x='country',
        y='points',
        hue='country',
        palette='Set2',
        ax=axes[idx],
        legend=False
    )

    axes[idx].set_title(f'{col_to_name(sub_topic)}')
    axes[idx].set_xlabel('')
    axes[idx].set_ylabel('Body')
    axes[idx].tick_params(axis='x', rotation=45)

for ax in axes[len(sub_topics_filtred):]:  
    fig.delaxes(ax)

fig.suptitle(f'Rozložení bodů dle zemí v jednotlivých podtématech dotazníku: {kompetence}')
plt.tight_layout(rect=[0, 0, 1, 0.95])
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')
plt.show()