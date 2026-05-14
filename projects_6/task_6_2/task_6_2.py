import pandas as pd
import numpy as np

# Фиксируем seed для воспроизводимости результатов
np.random.seed(42)

print("=" * 70)
print("ЗАДАНИЕ 1: Генеральная совокупность и выборки")
print("=" * 70)

# ============================================
# 1. СОЗДАЁМ ГЕНЕРАЛЬНУЮ СОВОКУПНОСТЬ
# ============================================

# Создаём DataFrame из 500 товаров интернет-магазина
population_size = 500

# Генерируем данные
np.random.seed(42)  # для воспроизводимости

population = pd.DataFrame({
    'product_id': range(1, population_size + 1),

    # Цена (непрерывная) - от 500 до 15000 рублей, с разным распределением
    'price': np.random.gamma(shape=2, scale=1500, size=population_size).round(2),

    # Количество отзывов (дискретная) - от 0 до 500
    'reviews_count': np.random.poisson(lam=50, size=population_size),

    # Категория товара (номинальная) - 4 категории с разной вероятностью
    'category': np.random.choice(
        ['Электроника', 'Одежда', 'Книги', 'Дом и кухня', 'Спорт'],
        size=population_size,
        p=[0.3, 0.25, 0.2, 0.15, 0.1]  # разные доли категорий
    ),

    # Рейтинг (порядковая: 1-5 звёзд) - с разной вероятностью
    'rating': np.random.choice(
        [1, 2, 3, 4, 5],
        size=population_size,
        p=[0.05, 0.1, 0.2, 0.35, 0.3]  # больше высоких рейтингов
    )
})

# Корректируем цены: делаем минимальную цену 100 руб, максимальную 30000 руб
population['price'] = population['price'].clip(100, 30000).round(2)

# Для дискретных данных: количество отзывов не может быть отрицательным
population['reviews_count'] = population['reviews_count'].clip(0, 500)

print("\n1. ГЕНЕРАЛЬНАЯ СОВОКУПНОСТЬ")
print("-" * 50)
print(f"Размер совокупности (N): {len(population)} товаров")
print(f"\nПервые 10 записей:")
print(population.head(10))
print(f"\nОсновные статистики совокупности:")
print(population.describe().round(2))

# Вычисляем параметр генеральной совокупности (истинное среднее)
population_mean_price = population['price'].mean()
print(f"\nПАРАМЕТР ГЕНЕРАЛЬНОЙ СОВОКУПНОСТИ (μ):")
print(f"Средняя цена всех товаров: {population_mean_price:.2f} руб.")

# Дополнительная информация о распределении категорий
print(f"\nРаспределение категорий в совокупности:")
print(population['category'].value_counts(normalize=True).round(3))

print(f"\nРаспределение рейтингов в совокупности:")
print(population['rating'].value_counts(normalize=True).sort_index().round(3))

print("\n" + "=" * 70)

# ============================================
# 2. ФОРМИРУЕМ ТРИ ВЫБОРКИ РАЗНОГО РАЗМЕРА
# ============================================

print("\n2. ФОРМИРОВАНИЕ ВЫБОРОК")
print("-" * 50)

# Размеры выборок
sample_sizes = [20, 50, 100]

# Создаём словарь для хранения выборок
samples = {}

for size in sample_sizes:
    # Берём случайную выборку без повторений
    samples[size] = population.sample(n=size, random_state=42 + size)
    print(f"Выборка n={size}: создана (случайная, random_state={42 + size})")

print("\n" + "=" * 70)

# ============================================
# 3. СРАВНИВАЕМ СРЕДНИЕ ЗНАЧЕНИЯ
# ============================================

print("\n3. СРАВНЕНИЕ СРЕДНИХ ЦЕН")
print("-" * 50)

# Создаём список для результатов
results = []

for size in sample_sizes:
    sample_mean = samples[size]['price'].mean()
    error = abs(sample_mean - population_mean_price)
    relative_error = (error / population_mean_price) * 100

    results.append({
        'Размер выборки (n)': size,
        'Среднее (выборка)': f"{sample_mean:.2f}",
        'Параметр (μ)': f"{population_mean_price:.2f}",
        'Абсолютная ошибка': f"{error:.2f}",
        'Относительная ошибка': f"{relative_error:.1f}%"
    })

    print(f"\nВыборка n={size}:")
    print(f"  Средняя цена в выборке (x̄): {sample_mean:.2f} руб.")
    print(f"  Средняя цена в совокупности (μ): {population_mean_price:.2f} руб.")
    print(f"  Абсолютная ошибка: {error:.2f} руб.")
    print(f"  Относительная ошибка: {relative_error:.1f}%")

# Выводим итоговую таблицу
print("\n" + "=" * 70)
print("\nИТОГОВАЯ ТАБЛИЦА СРАВНЕНИЯ:")
print("-" * 70)

result_df = pd.DataFrame(results)
print(result_df.to_string(index=False))

print("\n" + "=" * 70)

# ============================================
# ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ РЕПРЕЗЕНТАТИВНОСТИ
# ============================================

print("\n4. ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ РЕПРЕЗЕНТАТИВНОСТИ")
print("-" * 50)

print("\nСравнение распределения категорий товаров:")

for size in sample_sizes:
    print(f"\n--- Выборка n={size} ---")
    print("Категория | Доля в выборке | Доля в совокупности | Разница")
    print("-" * 60)

    # Получаем доли категорий в выборке
    sample_cats = samples[size]['category'].value_counts(normalize=True)
    # Доли в совокупности
    pop_cats = population['category'].value_counts(normalize=True)

    for cat in pop_cats.index:
        sample_prop = sample_cats.get(cat, 0)
        pop_prop = pop_cats[cat]
        diff = abs(sample_prop - pop_prop)
        print(f"{cat:<10} | {sample_prop:.3f}        | {pop_prop:.3f}           | {diff:.3f}")

print("\n" + "=" * 70)
print("\nВЫВОДЫ:")
print("-" * 50)

# Анализ результатов
for size in sample_sizes:
    sample_mean = samples[size]['price'].mean()
    error = abs(sample_mean - population_mean_price)
    relative_error = (error / population_mean_price) * 100

    if relative_error < 5:
        quality = "Отличная"
    elif relative_error < 10:
        quality = "Хорошая"
    else:
        quality = "Удовлетворительная"

    print(f"\n• Выборка n={size} показывает {quality.lower()} репрезентативность")
    print(f"  (ошибка {relative_error:.1f}% относительно параметра совокупности)")

# Общий вывод
print("\n" + "=" * 70)
print("\nОСНОВНЫЕ ВЫВОДЫ:")
print("1. С увеличением размера выборки ошибка обычно уменьшается")
print("2. Даже маленькая выборка (n=20) может дать неплохое приближение")
print("3. Однако для точных оценок рекомендуется использовать выборки n≥100")
print("4. Важно проверять репрезентативность не только по средним, но и по категориям")
print("=" * 70)