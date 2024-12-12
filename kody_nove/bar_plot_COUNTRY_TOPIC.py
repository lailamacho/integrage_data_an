import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from funkce import *
from typing import List

file_path_D_1 = "./exporty_dat/D_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_D_2 = "./exporty_dat/D_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

file_path_TZ_1 = "./exporty_dat/TZ_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_TZ_2 = "./exporty_dat/TZ_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

file_path_OS_1 = "./exporty_dat/OS_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_OS_2 = "./exporty_dat/OS_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

od = "8. 10. 2024"
do = "11. 12. 2024"

my_paths = [(file_path_D_1, file_path_D_2), (file_path_TZ_1, file_path_TZ_2), (file_path_OS_1, file_path_OS_2)]

def paths_to_dfs(paths: List[List[str]]):
    dfs = []
    res = []
    for x_paths in paths:
        d = pd.concat([pd.read_csv(x_paths[0], sep=';'), pd.read_csv(x_paths[1], sep=';')], axis=0, ignore_index=True)
        d_f_age = d[d['age']>50]
        dfs.append(d_f_age)

    for df in dfs:
        points_cols = [col for col in df.columns if "sub_topic_points" in col]
        sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
        kompetence = col_to_topic(sub_topic_cols[0])
        df_filtred = df[points_cols]
        df_filtred['country'] = df['country']
        df_filtred['achieved'] = df_filtred.sum(axis=1, numeric_only=True)
        df_filtred = df_filtred[['country', 'achieved']].dropna()
        res.append((df_filtred, kompetence))
    return res

x = paths_to_dfs(my_paths)
choice = ['mean', 'modus', 'median']

def bar_chart(dotazniky: List[list[pd.DataFrame, str]], choice: str):
    for operace in choice:
        data_df = pd.DataFrame()
        labels = []
        for dotaznik in dotazniky:
            df = dotaznik[0]
            kompetence = dotaznik[1]
            labels.append(kompetence)

            if operace == 'mean':
                popisek = "Průměr"
                df['mean'] = df[['country', 'achieved']].groupby(['country']).transform('mean')
            
            elif operace == 'modus':
                popisek = "Modus"
                df['modus'] = df.groupby(['country'])['achieved'].transform(lambda x: pd.Series.mode(x)[0] if not pd.Series.mode(x).empty else None)
            
            elif operace == 'median':
                popisek = "Medián"
                df['median'] = df[['country', 'achieved']].groupby(['country']).transform('median')


            df_2 = df.drop_duplicates(subset=['country', operace], keep='first')
            df_2 = df_2[['country', operace]]
            df_2.sort_values('country')
            
            if data_df.empty:
                data_df = df_2
            else:
                data_df = pd.merge(data_df, df_2, on='country', how='outer')


        sns.set_theme(style="whitegrid")
        fig = plt.figure(figsize=(12, 8))
        df_long = data_df.melt(id_vars='country', var_name='Category', value_name='Mean')
        sns.barplot(
            data=df_long,
            x='country',
            y='Mean',
            hue='Category',
            palette=[ '#da5c57', '#18baa8', '#00addc']
            )

        plt.title(f'{popisek} získaných bodů v jednotlivých dotaznících \nv období od {od} do {do}',loc='left')
        plt.xlabel('Země')
        plt.tick_params(rotation=45)
        plt.ylabel(f'{popisek} bodů')
        legend = plt.legend(fontsize='small', loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.25))
        for text, label in zip(legend.texts, labels):    
            text.set_text(label)
        
        fig.tight_layout()
        filename = f"Bar-plot_{operace}_{kompetence}"
        fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')  
    plt.show()


bar_chart(x, choice)