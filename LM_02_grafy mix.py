import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "./exporty/dovednosti_24-10-01.csv"
df = pd.read_csv(file_path, sep=";")


## BAR CHART: ROZLOŽENÍ RESPONDENTŮ PODLE POHLAVÍ
fig = plt.figure(figsize=(8, 5))
gender_count = df['gender'].value_counts()
sns.barplot(x=gender_count.index, y=gender_count.values, palette='Set3')
plt.title('Rozložení respondentů podle pohlaví')
plt.xlabel('Pohlaví')
plt.ylabel('Počet respodentů')
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')


## PIE CHART: ROZLOŽENÍ RESPONDENTŮ DLE VZDĚLÁNÍ
fig = plt.figure(figsize=(8, 8))
education_count = df['education'].value_counts()
plt.pie(education_count.values, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set3'))
plt.title('Rozložení respondentů dle vzdělání')
plt.axis('equal')
labels = education_count.index
plt.legend(labels, draggable=True, loc='lower center', bbox_to_anchor=(0.65, 0, 0.5, 0.75))
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')


## HISTOGRAM: VĚKOVÉ SLOŽENÍ RESPONDENTŮ
fig = plt.figure(figsize=(8, 5))
colors=sns.color_palette('Set3')
sns.histplot(df['age'].dropna(), bins=10, color=colors[0], linewidth=0.5)
plt.title('Věkové složení respondentů')
plt.xlabel('Věk')
plt.ylabel('Počet počet respondentů')
filename = input("Název souboru: ")
fig.savefig(f"./grafy/{filename}.png", dpi=300, bbox_inches='tight')
plt.show()