# create_test_data.py - Создание тестовых данных для анализа

import psycopg2
import random

connection = psycopg2.connect(
    host="localhost",
    port="5432",
    user="postgres",
    password="example",
    database="testdb"
)

cursor = connection.cursor()

# Создаём таблицы (если не существуют)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS prices (
        price_id SERIAL PRIMARY KEY,
        product_id INTEGER REFERENCES products(product_id),
        price DECIMAL(10, 2) NOT NULL,
        date_recorded DATE NOT NULL
    );
""")

# Добавляем товары
products = [
    ("Ноутбук", "Электроника"),
    ("Смартфон", "Электроника"),
    ("Наушники", "Электроника"),
    ("Книга", "Книги"),
    ("Кроссовки", "Одежда"),
    ("Куртка", "Одежда"),
    ("Часы", "Аксессуары"),
    ("Стул", "Мебель"),
    ("Стол", "Мебель"),
    ("Мышка", "Электроника"),
]

for name, category in products:
    cursor.execute(
        "INSERT INTO products (product_name, category) VALUES (%s, %s) ON CONFLICT DO NOTHING",
        (name, category)
    )

# Добавляем цены с разбросом для каждого товара
cursor.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

for product_id in product_ids:
    # Базовая цена зависит от категории
    cursor.execute("SELECT category FROM products WHERE product_id = %s", (product_id,))
    category = cursor.fetchone()[0]

    if category == "Электроника":
        base_prices = [5000, 30000, 15000, 25000]
    elif category == "Одежда":
        base_prices = [2000, 5000, 3000]
    elif category == "Книги":
        base_prices = [300, 500, 700, 1000]
    elif category == "Мебель":
        base_prices = [5000, 10000, 8000]
    else:  # Аксессуары
        base_prices = [1000, 2000, 1500]

    # Добавляем 3-5 записей о ценах для каждого товара
    for _ in range(random.randint(3, 6)):
        price = random.choice(base_prices) * random.uniform(0.8, 1.2)
        cursor.execute(
            "INSERT INTO prices (product_id, price, date_recorded) VALUES (%s, %s, CURRENT_DATE)",
            (product_id, round(price, 2))
        )

connection.commit()
cursor.close()
connection.close()
print("✅ Тестовые данные созданы успешно!")