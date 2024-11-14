import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import math
from funkce import *

file_path = "./exporty/dovednosti_24-10-01.csv"  # NUTNO MĚNIT ÚDAJE!!!
df = pd.read_csv(file_path, sep=";")

## MH_02_01: GROUPED BAR CHART (skupinový sloupcový graf) - porovnání jednotlivých výsledků (sub_topic) z dotazníku

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

df_grouped = df_2.groupby(['sub_topic', 'rank'], observed=False).size().reset_index(name='counts')

# Vykreslení A) porovnání jednotlivých výsledků (sub_topic) z dotazníku
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=df_grouped,
    x='sub_topic',
    y='counts',
    hue='rank',
    palette='Set1'  
)

plt.title(f'Výsledky v jednotlivých podtématech v dotazníku: {kompetence}')
plt.xlabel('')
plt.tick_params(rotation=45)
plt.ylabel('Počet')
plt.legend(title='Úroveň', fontsize='small', markerfirst=False, draggable=True)
#fig.tight_layout()

filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')

#---------------------------------------------------------------------------------------------------------------
## MH_02_02: GROUPED BAR CHART (skupinový sloupcový graf) - porovnání jednotlivých výsledků (su_topic) dle zemí z dotazníku

df_grouped = df_2.groupby(['sub_topic', 'country', 'rank'], observed=False).size().reset_index(name='counts')
sub_topics = df_2['sub_topic'].unique()
num_subplots = len(sub_topics)

# Vykreslení B) porovnání jednotlivých výsledků (sub_topic) z dotazníku - členěno dle zemí
fig, axes = plt.subplots(nrows=math.ceil(num_subplots / 2), ncols=2, figsize=(16, 10)) # automaticky pocet radku a sloupcu
axes = axes.flatten() # zarovnani subplotů
labels=["Nejhorší úroveň", "Střední úroveň", "Nejlepší úroveň"]


for idx, sub_topic in enumerate(sub_topics):
    sub_topic_data = df_grouped[df_grouped['sub_topic'] == sub_topic]
    
    sns.barplot(
        data=sub_topic_data,
        x='country',
        y='counts',
        hue='rank',
        palette='Set1',
        ax=axes[idx]
    )

    axes[idx].set_title(f'{sub_topic}')
    axes[idx].set_xlabel('')
    axes[idx].set_ylabel('Počet')
    axes[idx].tick_params(axis='x', rotation=0)
    axes[idx].legend().set_visible(False)

for ax in axes[num_subplots:]: # odstraneni prazdnych subplotu (lichy pocet sub_topic)
    fig.delaxes(ax)

fig.suptitle(f'Přehled výsledků dle zemí v jednotlivých podtématech dotazníku: {kompetence}')
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.legend(ncols=1, fontsize='small', markerfirst=False, draggable=True)

filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')

plt.show()