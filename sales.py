import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
# код относится к файлам из директории Sales_data, статистика продаж электронной техники
# разбитой по месяцам года


# pd settings
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 300)


# Конкатенация csv файлов в один
def concat_csv_file_into_big_one(data):
    data = pd.concat([pd.read_csv(file) for file in data.glob('*.csv')], ignore_index=True)
    data.to_csv('result_data.csv', index=False)


# concat_csv_file_into_big_one(
#     Path('C:/Users/major/PycharmProjects/LeetCodeTaskAndSortingAlghoritms/pandas_practice/Sales_Data'))


# csv файл в DataFrame
def write_big_csv_file_in_dataframe():
    frame = pd.DataFrame(pd.read_csv('result_data.csv'))
    return frame


# Удаляем NaN значения, записываем новый файл
def del_null_from_dataframe_and_write_new(data_file):
    res = data_file.dropna(how='all')
    res.to_csv('result_data_v2.csv')


# переименовываем столбцы
def change_columns_type():
    data = pd.read_csv('result_data_v2.csv')

    data.rename(
        {'Order ID': 'order_id', 'Quantity Ordered': 'quantity', 'Price Each': 'price', 'Order Date': 'order_date',
         'Purchase Address': 'address', 'Product': 'product'},
        inplace=True, axis=1)
    # quantity в int, price в float
    data.quantity = pd.to_numeric(data.quantity, errors='coerce').fillna(0).astype(np.int64)
    data.price = pd.to_numeric(data.price, errors='coerce')
    # удаляем строки-дубликаты
    data = data.drop(data[data.order_date.str.contains('Order Date')].index)
    data.to_csv('result_data_V3.csv', index=False)


# добавить тотал сумму в фрейм
def add_total_column_to_the_frame():
    data = pd.read_csv('result_data_V3.csv')
    data.insert(5, 'Total', data.quantity * data.price)
    data.to_csv('result_data_V4.csv')


# вытащить из даты месяц и создать столбец в фрейме
def add_month_to_the_frame():
    data = pd.read_csv('result_data_V4.csv')
    data['order_date'] = pd.to_datetime(data['order_date'])
    data.insert(8, 'Month', data['order_date'].dt.month)
    data.to_csv('result_data_V5.csv')


# file = pd.read_csv('result_data_V5.csv')
# data_by_month = file.groupby('Month')[['Total']].sum().sort_values(by='Total', ascending=True)

# вывод чистой оси y в plot
def bar_from_pandas():
    data.plot(kind='bar', grid=True).get_yaxis().get_major_formatter().set_scientific(False)
    plt.show()


# визуализация данных, общая статистика
def bar_from_matplotlib(data):
    plt.bar(data.index, data.Total)
    plt.xticks(range(1, 13))  # вывод всех значений на оси х
    plt.yticks(range(0, round(data.max()[0]), 500000))  # вывод значений на у оси, с шагом
    # делаем нормальный вывод чисел по y
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.legend(['Total'])
    plt.grid()
    plt.xlabel('Month')
    plt.ylabel('Total')
    # вывод текста на столбцах графика
    for index, value in enumerate(data.Total):
        plt.text(index + 1, 500000, value, rotation='vertical', size='large', ha='center')
    plt.show()


# лучшие часы для продаж, вывод
def sales_by_hour():
    date = data['order_date'] = pd.to_datetime(data['order_date'])
    data.insert(10, 'Day_name', data['order_date'].dt.day_name())
    data.insert(11, 'Hour', data['order_date'].dt.hour)
    max_hour = data.groupby('Hour').agg(['sum', 'count'])['Total']

    plt.bar(max_hour.index, max_hour['sum'])
    plt.xticks(range(0, 24))  # вывод всех значений на оси х
    plt.yticks(range(0, round(max_hour.max()[0]) + 1500000, 500000))  # вывод значений на у оси, с шагом
    # делаем нормальный вывод чисел по y
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)
    plt.legend(['Total'])
    plt.grid()
    plt.xlabel('Часы')
    plt.ylabel('Total')
    # вывод текста на столбцах графика
    for index, value in enumerate(max_hour['sum']):
        plt.text(index, value + 100000, value, rotation='vertical', size=10, ha='center')
    plt.savefig('counts.png', dpi=100)  # сохранить картинку графика
    plt.show()


# лучшие дни продаж
def best_sales_by_day_of_the_week():
    data = pd.read_csv('results_data.csv')
    sales_by_day = data.groupby('Day_name').agg(['sum', 'count'])['Total']
    sales_by_day.sort_values('sum')
    plt.bar(sales_by_day.index, sales_by_day['sum'])
    plt.xticks(range(0, 8))
    plt.yticks(range(0, round(sales_by_day.max()[0]) + 1500000, 500000))
    plt.grid()
    plt.xlabel('Дни недели')
    plt.ylabel('Total')
    for index, value in enumerate(sales_by_day['sum']):
        plt.text(index, value + 100000, value, rotation='vertical', size=10, ha='center')
    plt.show()


# data = pd.read_csv('results_data.csv')
# sales_by_day = data.groupby('address').agg(['sum', 'count'])['Total']


# Вытаскиваем название город и штат из строки с адресом
def get_city(value: str) -> str:
    result = value.split(',')
    city = result[1].strip(' ')
    code = result[2].split()[0]
    return city + ', ' + code


# лучшие продажи по городам
def best_sales_by_cities():
    data = pd.read_csv('results_data.csv')
    data['city'] = data.address.apply(get_city)
    sales_by_city = data.groupby('city').agg(['sum'])['Total']
    plt.bar(sales_by_city.index, sales_by_city['sum'])
    plt.show()


