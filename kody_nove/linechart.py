import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from funkce import *
from typing import Tuple, List
from matplotlib.ticker import MultipleLocator

file_path_D_1 = "./exporty_dat/D_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_D_2 = "./exporty_dat/D_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

file_path_TZ_1 = "./exporty_dat/TZ_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_TZ_2 = "./exporty_dat/TZ_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

file_path_OS_1 = "./exporty_dat/OS_2024-10-16_to_2024-12-11.csv"  # NUTNO MĚNIT ÚDAJE!!!
file_path_OS_2 = "./exporty_dat/OS_2024-10-08_to_2024-10-15.csv"  # NUTNO MĚNIT ÚDAJE!!!

od = "8. 10. 2024"
do = "11. 12. 2024"

my_country = "CZ"
my_paths = [(file_path_D_1, file_path_D_2), (file_path_TZ_1, file_path_TZ_2), (file_path_OS_1, file_path_OS_2)]
choice = ['mean', 'modus', 'median']
make_for_subtopic = True


def paths_to_dfs(paths: List[List[str]], my_country:str):
    dfs = []
    res = []
    for x_paths in paths:
        d = pd.concat([pd.read_csv(x_paths[0], sep=';'), pd.read_csv(x_paths[1], sep=';')], axis=0, ignore_index=True)
        d_f_age = d[d['age']>50]
        df_cz = d_f_age.query(f'country == "{my_country}"') 

        dfs.append(df_cz)

    for df in dfs:
        points_cols = [col for col in df.columns if "sub_topic_points" in col]
        sub_topic_cols = [col for col in df.columns if "sub_topic" in col and len(col) <= 12]
        kompetence = col_to_topic(sub_topic_cols[0])
        df_filtred = df[points_cols].copy()
        df_filtred[sub_topic_cols] = df[sub_topic_cols]
        df_filtred['age'] = df['age']

        #df_filtred['achieved'] = df_filtred.sum(axis=1, numeric_only=True)
        #df_filtred = df_filtred[['education', 'gender', 'achieved']].dropna()
        res.append((df_filtred.dropna(), kompetence))
    return res

my_dfs = paths_to_dfs(my_paths, my_country)

def line_chart(dotazniky: List[Tuple[pd.DataFrame, str]], choice: str, my_country:str, subtopic: bool, col=None, col_2=None):
    for operace in choice:
        data_df = pd.DataFrame()
        df = dotazniky[0]
        kompetence = dotazniky[1]

        if subtopic == False:
                work_with = 'achieved'

        elif subtopic == True:
                work_with = col

        if operace == 'mean':
            popisek = "Průměr"
            df['mean'] = df.groupby(['age'])[work_with].transform('mean')
                
        elif operace == 'modus':
            popisek = "Modus"
            df['modus'] = df.groupby(['age'])[work_with].transform(lambda x: pd.Series.mode(x)[0] if not pd.Series.mode(x).empty else None)
                
        elif operace == 'median':
            popisek = "Medián"
            df['median'] = df.groupby(['age'])[work_with].transform('median')

        df_2 = df.drop_duplicates(subset=['age', operace], keep='first')
        df_2 = df_2.sort_values('age')
           
        if subtopic == False:
            title = f"{popisek} získaných bodů v závislosti na věku respondentů \nDotazník: {kompetence} \npro zemi: {country_code[my_country][0]} \nv období od {od} do {do}"
            filename = f"Linechart_body-vek_{operace}_{kompetence}"

        else:
            title = f"{popisek} získaných bodů v závislosti na věku respondentů \nDotazník: {kompetence}, podtémma: {col_to_name(col_2)} \npro zemi: {country_code[my_country][0]} \nv období od {od} do {do}"
            filename = f"Linechart_body-vek_{operace}_{kompetence}_{col_to_name(col_2)}"

        #print(df_2)
        sns.set_theme(style="whitegrid")
        fig = plt.figure(figsize=(12, 8))
        sns.lineplot(
                data=df_2,
                x='age',
                y=operace,
                marker='o',
                palette=['#00addc']
                )
        ax = plt.gca()
        ax.xaxis.set_major_locator(MultipleLocator(1))
        
        plt.title(title, loc='left')
        plt.xlabel('Věk')
        plt.tick_params(rotation=0)
        plt.ylabel(f'{popisek} bodů')             
        fig.tight_layout()
        fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')
    #plt.show()

if make_for_subtopic == False:
    for idx, x in enumerate(my_dfs):
        points_cols = [col for col in x[0].columns if "sub_topic_points" in col]
        x[0]['achieved'] = x[0][points_cols].sum(axis=1,numeric_only=True)
        line_chart(my_dfs[idx], choice, my_country, subtopic=False)

elif make_for_subtopic == True:
    for idx, x in enumerate(my_dfs):
        points_cols = [col for col in x[0].columns if "sub_topic_points" in col]
        sub_topic_cols = [col for col in x[0].columns if "sub_topic" in col and len(col) <= 12]
        for col, col_2 in zip(points_cols, sub_topic_cols):
            line_chart(my_dfs[idx], choice, my_country, subtopic=True, col=col, col_2=col_2)