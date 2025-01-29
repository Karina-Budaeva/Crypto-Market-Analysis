import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate


# Функция для загрузки данных
def load_data(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and data and all(isinstance(item, dict) for item in data):
            return pd.DataFrame(data)
        else:
            print("Ошибка: получены некорректные данные от API")
            return pd.DataFrame()
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе API: {e}")
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
    # Проверка наличия нужных колонок
    required_columns = {'name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'high_24h', 'low_24h'}
    if not required_columns.issubset(df.columns):
        print(f"Ошибка: отсутствуют столбцы {required_columns - set(df.columns)}")
    else:
        # Расчет волатильности и коэффициента ликвидности
        df['volatility'] = ((df['high_24h'] - df['low_24h']) / df['low_24h']) * 100
        df['liquidity_ratio'] = df['total_volume'] / df['market_cap']

        # Вывод данных
        print("Топ-10 криптовалют:")
        print(df[['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'volatility', 'liquidity_ratio']])

        # Сохранение таблицы в Markdown
        table_md = tabulate(
            df[['name', 'symbol', 'current_price', 'market_cap', 'total_volume', 'volatility', 'liquidity_ratio']],
            headers=['Name', 'Symbol', 'Price (USD)', 'Market Cap', 'Volume', 'Volatility (%)', 'Liquidity Ratio'],
            tablefmt="github"
        )
        with open("table.md", "w", encoding="utf-8") as f:
            f.write("### Анализ криптовалют\n")
            f.write(table_md)
        print("\nТаблица успешно сохранена в файл table.md.")


# 1. Столбчатый график: текущие цены (по убыванию)
    df_sorted_by_price = df.sort_values('current_price', ascending=False)
    plt.figure(figsize=(10, 6))
    sns.barplot(y='name', x='current_price', data=df_sorted_by_price, palette='coolwarm', hue='name')
    plt.title('Текущие цены криптовалют (по убыванию)')
    plt.xlabel('Цена (USD)')
    plt.ylabel('Криптовалюта')
    plt.show()

# 2. Круговая диаграмма: доля рыночной капитализации TOP-5 + другие
    df_sorted = df.sort_values(by='market_cap', ascending=False)
    top_5 = df_sorted[:5]
    others = df_sorted[5:].market_cap.sum()

    labels = list(top_5['name']) + ['Другие']
    values = list(top_5['market_cap']) + [others]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title("Доля рыночной капитализации (Top-5 + другие)")
    plt.savefig("market_cap_pie.png")
    plt.show()

else:
    print("Нет данных для отображения.")