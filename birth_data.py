import pandas as pd
import matplotlib.pyplot as plt


# Код относится к файлам из диретории names, статистика имён , детям родившимся в период с 1880 по 2020

def names_data():
    data = pd.read_csv('names/yob2019.txt', names=['name', 'sex', 'count'])  # читаем файл и добавляем индексы
    view = data[data.sex == 'F'].sort_values('count', ascending=False).head(10)  # топ10 женских имен
    top_2 = data.sort_values('count', ascending=False).drop_duplicates('sex')  # топ женское и мужское имя


# соединем все файлы в один
def join_all_files_in_one():  # объединяем файл в один
    data = pd.DataFrame()

    for year in range(1880, 2021):
        tmp = pd.read_csv(f'names/yob{year}.txt', names=['name', 'sex', 'count'])
        tmp['Year'] = year
        data = pd.concat([data, tmp])
    data.to_csv('yob.csv', index=False)


# стотистика по годам
def birth_rate_by_year():
    data = pd.read_csv('yob.csv')
    g_data = data.groupby(['sex', 'Year']).sum().unstack(level=0)
    plt.plot(g_data)
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.xlabel('Год')
    plt.ylabel('Количество')
    plt.xticks(range(1880, g_data.index.max() + 1, 5), rotation='vertical')
    plt.legend(['Count Female', 'Count Male'])
    plt.show()


# статистика топ имён
def top_names_by_all_time():
    data = pd.read_csv('yob.csv')
    top_male_name = data[data.sex == 'M'].sort_values(by='count', ascending=False).drop_duplicates('name').head(10)
    top_female_name = data[data.sex == 'F'].sort_values(by='count', ascending=False).drop_duplicates('name').head(10)
    df_all = pd.concat([top_female_name, top_male_name])
    return df_all
