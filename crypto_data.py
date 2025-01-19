import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Функция для загрузки данных
def load_data(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json())
    else:
        print("Не удалось загрузить данные")
        return pd.DataFrame()

# Параметры API
url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1,
    "sparkline": False
}

# Загрузка данных
df = load_data(url, params)

# Проверка данных
if not df.empty:
    # Вывод таблицы
    print("Топ-10 криптовалют:")
    print(df[['name', 'symbol', 'current_price', 'market_cap', 'total_volume']])

    # 1. Столбчатый график: текущие цены
    plt.figure(figsize=(10, 6))
    sns.barplot(y='name', x='current_price', data=df, hue='name', dodge=False)
    plt.title("Текущие цены криптовалют (в USD)")
    plt.xlabel("Цена (USD)")
    plt.ylabel("Криптовалюта")
    plt.legend([], [], frameon=False)  # Убираем лишнюю легенду
    plt.show()

    # 2. Круговая диаграмма: доля рыночной капитализации
    plt.figure(figsize=(8, 8))
    plt.pie(
        df['market_cap'],
        labels=df['name'],
        autopct='%1.1f%%',
        startangle=140,
        colors=sns.color_palette('pastel')
    )
    plt.title("Доля рыночной капитализации")
    plt.show()
else:
    print("Нет данных для отображения.")