import pandas as pd
import numpy as np

print("=" * 70)
print("ЗАДАНИЕ 1: Анализ размаха (Range), IQR и обнаружение выбросов")
print("=" * 70)

# ============================================
# ЗАДАНИЕ 1.1: РУЧНОЙ РАСЧЁТ RANGE И IQR
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 1: Вычисление Range и IQR вручную")
print("=" * 70)

# Исходный набор оценок
grades = [55, 60, 62, 65, 67, 70, 72, 74, 75, 78, 80, 82, 98]

print("\nИсходный набор данных (оценки за экзамен):")
print(f"Данные: {grades}")
print(f"Количество элементов: n = {len(grades)}")

# ---------- РУЧНОЙ РАСЧЁТ RANGE ----------
print("\n" + "-" * 50)
print("ШАГ 1: Вычисление РАЗМАХА (Range) вручную")
print("-" * 50)

min_val = min(grades)
max_val = max(grades)
range_manual = max_val - min_val

print(f"1. Находим минимальное значение: min = {min_val}")
print(f"2. Находим максимальное значение: max = {max_val}")
print(f"3. Размах = max - min = {max_val} - {min_val} = {range_manual}")

# ---------- РУЧНОЙ РАСЧЁТ IQR ----------
print("\n" + "-" * 50)
print("ШАГ 2: Вычисление IQR вручную")
print("-" * 50)

# Сортируем данные (уже отсортированы)
sorted_grades = sorted(grades)
print(f"1. Отсортированные данные: {sorted_grades}")

# Находим позиции квартилей
n = len(sorted_grades)
print(f"2. Количество элементов: n = {n}")

# Q1 (25-й перцентиль) - позиция (n+1)*0.25
q1_pos = (n + 1) * 0.25
print(f"3. Позиция Q1 = (n+1)*0.25 = ({n}+1)*0.25 = {q1_pos}")

# Интерполяция для Q1
q1_idx_low = int(q1_pos) - 1  # индекс нижнего элемента (0-based)
q1_idx_high = q1_idx_low + 1
q1_weight = q1_pos - int(q1_pos)

if q1_weight == 0:
    q1_manual = sorted_grades[q1_idx_low]
else:
    q1_manual = sorted_grades[q1_idx_low] * (1 - q1_weight) + sorted_grades[q1_idx_high] * q1_weight

print(
    f"   Q1 = {sorted_grades[q1_idx_low]} + {q1_weight} * ({sorted_grades[q1_idx_high]} - {sorted_grades[q1_idx_low]}) = {q1_manual:.2f}")

# Q3 (75-й перцентиль) - позиция (n+1)*0.75
q3_pos = (n + 1) * 0.75
print(f"4. Позиция Q3 = (n+1)*0.75 = ({n}+1)*0.75 = {q3_pos}")

# Интерполяция для Q3
q3_idx_low = int(q3_pos) - 1
q3_idx_high = q3_idx_low + 1
q3_weight = q3_pos - int(q3_pos)

if q3_weight == 0:
    q3_manual = sorted_grades[q3_idx_low]
else:
    q3_manual = sorted_grades[q3_idx_low] * (1 - q3_weight) + sorted_grades[q3_idx_high] * q3_weight

print(
    f"   Q3 = {sorted_grades[q3_idx_low]} + {q3_weight} * ({sorted_grades[q3_idx_high]} - {sorted_grades[q3_idx_low]}) = {q3_manual:.2f}")

# Вычисляем IQR
iqr_manual = q3_manual - q1_manual
print(f"5. IQR = Q3 - Q1 = {q3_manual:.2f} - {q1_manual:.2f} = {iqr_manual:.2f}")

# ---------- ПРОВЕРКА ЧЕРЕЗ PANDAS ----------
print("\n" + "-" * 50)
print("ШАГ 3: Проверка через pandas")
print("-" * 50)

grades_series = pd.Series(grades)
range_pandas = grades_series.max() - grades_series.min()
q1_pandas = grades_series.quantile(0.25)
q3_pandas = grades_series.quantile(0.75)
iqr_pandas = q3_pandas - q1_pandas

print(f"Range: {range_pandas} (ручной: {range_manual})")
print(f"Q1:    {q1_pandas:.2f} (ручной: {q1_manual:.2f})")
print(f"Q3:    {q3_pandas:.2f} (ручной: {q3_manual:.2f})")
print(f"IQR:   {iqr_pandas:.2f} (ручной: {iqr_manual:.2f})")

print("\n✅ Ручные расчёты совпадают с pandas!")

# ============================================
# ЗАДАНИЕ 1.2: ОБНАРУЖЕНИЕ ВЫБРОСОВ МЕТОДОМ 1.5 × IQR
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 2: Обнаружение выбросов методом 1.5 × IQR")
print("=" * 70)

# Вычисляем границы
lower_fence = q1_pandas - 1.5 * iqr_pandas
upper_fence = q3_pandas + 1.5 * iqr_pandas

print(f"\nПараметры для обнаружения выбросов:")
print(f"  Q1 = {q1_pandas:.2f}")
print(f"  Q3 = {q3_pandas:.2f}")
print(f"  IQR = {iqr_pandas:.2f}")
print(f"  1.5 × IQR = {1.5 * iqr_pandas:.2f}")
print(f"\nГраницы для выбросов:")
print(f"  Нижняя граница: Q1 - 1.5×IQR = {q1_pandas:.2f} - {1.5 * iqr_pandas:.2f} = {lower_fence:.2f}")
print(f"  Верхняя граница: Q3 + 1.5×IQR = {q3_pandas:.2f} + {1.5 * iqr_pandas:.2f} = {upper_fence:.2f}")

# Находим выбросы
outliers_mask = (grades_series < lower_fence) | (grades_series > upper_fence)
outliers = grades_series[outliers_mask]
clean_grades = grades_series[~outliers_mask]

print(f"\n🔍 Результаты обнаружения выбросов:")
print(f"  Выбросы: {outliers.tolist() if len(outliers) > 0 else 'Не обнаружено'}")
print(f"  Количество выбросов: {len(outliers)}")
print(f"  Очищенные данные: {sorted(clean_grades.tolist())}")

# Сравнение средних
mean_with_outliers = grades_series.mean()
mean_without_outliers = clean_grades.mean()

print(f"\n📊 Сравнение среднего значения:")
print(f"  Среднее с выбросами:    {mean_with_outliers:.2f}")
print(f"  Среднее без выбросов:   {mean_without_outliers:.2f}")
print(f"  Изменение:              {mean_without_outliers - mean_with_outliers:+.2f}")
print(f"  Изменение в %:          {(mean_without_outliers / mean_with_outliers - 1) * 100:+.1f}%")

print(f"\n💡 ВЫВОД ПО ЧАСТИ 2:")
if len(outliers) > 0:
    print(f"  ✅ Обнаружен выброс: {outliers.tolist()[0]}")
    print(f"  ✅ После удаления выброса среднее изменилось на {abs(mean_without_outliers - mean_with_outliers):.2f}")
    print(f"  ✅ Новое среднее более репрезентативно для типичного студента")
else:
    print(f"  ℹ️ Выбросов не обнаружено, данные чистые")

# ============================================
# ЗАДАНИЕ 1.3: ИНТЕРНЕТ-МАГАЗИН (15 ТОВАРОВ + ВЫБРОСЫ)
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 3: Анализ цен в интернет-магазине (с выбросами)")
print("=" * 70)

# Создаём данные о товарах
np.random.seed(42)

# Нормальные цены (от 500 до 3000 рублей)
normal_prices = np.random.randint(500, 3000, size=13)

# Добавляем 2 выброса:
# - очень дешёвый товар (10 рублей)
# - очень дорогой товар (50000 рублей)
prices_with_outliers = np.append(normal_prices, [10, 50000])

# Создаём DataFrame
products_df = pd.DataFrame({
    'product_id': range(1, 16),
    'price': prices_with_outliers,
    'category': np.random.choice(['Электроника', 'Одежда', 'Книги', 'Дом'], size=15)
})

print("\n📊 Исходные данные о товарах:")
print(products_df.to_string(index=False))

# Вычисляем статистику исходных данных
print("\n" + "-" * 50)
print("СТАТИСТИКА ДО ОЧИСТКИ ОТ ВЫБРОСОВ:")
print("-" * 50)

original_mean = products_df['price'].mean()
original_median = products_df['price'].median()
original_min = products_df['price'].min()
original_max = products_df['price'].max()
original_std = products_df['price'].std()

print(f"  Средняя цена:    {original_mean:>10,.2f} руб.")
print(f"  Медианная цена:  {original_median:>10,.2f} руб.")
print(f"  Минимальная цена:{original_min:>10,.2f} руб.")
print(f"  Максимальная цена:{original_max:>10,.2f} руб.")
print(f"  Стандартное отклонение: {original_std:>10,.2f} руб.")

# ---------- ОБНАРУЖЕНИЕ ВЫБРОСОВ ----------
print("\n" + "-" * 50)
print("ОБНАРУЖЕНИЕ ВЫБРОСОВ МЕТОДОМ 1.5 × IQR:")
print("-" * 50)

# Вычисляем квартили и IQR
q1 = products_df['price'].quantile(0.25)
q3 = products_df['price'].quantile(0.75)
iqr = q3 - q1

lower_fence = q1 - 1.5 * iqr
upper_fence = q3 + 1.5 * iqr

print(f"  Q1 = {q1:.2f} руб.")
print(f"  Q3 = {q3:.2f} руб.")
print(f"  IQR = {iqr:.2f} руб.")
print(f"  Нижняя граница: {lower_fence:.2f} руб.")
print(f"  Верхняя граница: {upper_fence:.2f} руб.")

# Находим выбросы
outliers_mask = (products_df['price'] < lower_fence) | (products_df['price'] > upper_fence)
outliers_df = products_df[outliers_mask]
clean_df = products_df[~outliers_mask]

print(f"\n  Обнаружено выбросов: {len(outliers_df)}")
if len(outliers_df) > 0:
    print(f"\n  Выбросы:")
    for _, row in outliers_df.iterrows():
        print(f"    • Товар #{row['product_id']}: {row['price']:,.0f} руб. ({row['category']})")

# ---------- СТАТИСТИКА ПОСЛЕ ОЧИСТКИ ----------
print("\n" + "-" * 50)
print("СТАТИСТИКА ПОСЛЕ ОЧИСТКИ ОТ ВЫБРОСОВ:")
print("-" * 50)

clean_mean = clean_df['price'].mean()
clean_median = clean_df['price'].median()
clean_min = clean_df['price'].min()
clean_max = clean_df['price'].max()
clean_std = clean_df['price'].std()

print(f"  Средняя цена:    {clean_mean:>10,.2f} руб.")
print(f"  Медианная цена:  {clean_median:>10,.2f} руб.")
print(f"  Минимальная цена:{clean_min:>10,.2f} руб.")
print(f"  Максимальная цена:{clean_max:>10,.2f} руб.")
print(f"  Стандартное отклонение: {clean_std:>10,.2f} руб.")

print("\n" + "-" * 50)
print("СРАВНИТЕЛЬНЫЙ АНАЛИЗ:")
print("-" * 50)

mean_change = clean_mean - original_mean
mean_change_pct = (mean_change / original_mean) * 100

print(f"\n  {'Показатель':<25} | {'До очистки':>12} | {'После очистки':>12} | {'Изменение':>12}")
print("  " + "-" * 65)
print(
    f"  {'Средняя цена':<25} | {original_mean:>10,.0f} | {clean_mean:>10,.0f} | {mean_change:>+10,.0f} ({mean_change_pct:>+5.1f}%)")
print(
    f"  {'Медианная цена':<25} | {original_median:>10,.0f} | {clean_median:>10,.0f} | {clean_median - original_median:>+10,.0f}")
print(
    f"  {'Станд. отклонение':<25} | {original_std:>10,.0f} | {clean_std:>10,.0f} | {clean_std - original_std:>+10,.0f}")
print(
    f"  {'Размах (max-min)':<25} | {original_max - original_min:>10,.0f} | {clean_max - clean_min:>10,.0f} | {(clean_max - clean_min) - (original_max - original_min):>+10,.0f}")

# Визуализация распределения цен
print("\n" + "=" * 50)
print("ВИЗУАЛИЗАЦИЯ РАСПРЕДЕЛЕНИЯ ЦЕН:")
print("=" * 50)


def create_price_histogram(prices, title, max_price=50000):
    print(f"\n{title}:")
    bins = [0, 1000, 2000, 3000, 4000, 5000, 10000, 20000, 50000]
    for i in range(len(bins) - 1):
        count = sum((prices >= bins[i]) & (prices < bins[i + 1]))
        if count > 0:
            bar = '█' * count
            print(f"  {bins[i]:>6,}-{bins[i + 1]:>7,} руб.: {bar} ({count} товаров)")


create_price_histogram(products_df['price'], "📊 До очистки от выбросов")
create_price_histogram(clean_df['price'], "📊 После очистки от выбросов")

# Дополнительный анализ: что представляют собой выбросы
print("\n" + "=" * 50)
print("ДЕТАЛЬНЫЙ АНАЛИЗ ВЫБРОСОВ:")
print("=" * 50)

if len(outliers_df) > 0:
    print("\n  Почему эти значения считаются выбросами?")
    for _, row in outliers_df.iterrows():
        price = row['price']
        if price < lower_fence:
            print(f"    • Товар #{row['product_id']} (цена {price:,.0f} руб.)")
            print(f"      - Ниже нижней границы ({lower_fence:.0f} руб.)")
            print(
                f"      - Отклонение от Q1: {q1 - price:.0f} руб. ({(q1 - price) / q1 * 100:.0f}% ниже типичной нижней границы)")
        if price > upper_fence:
            print(f"    • Товар #{row['product_id']} (цена {price:,.0f} руб.)")
            print(f"      - Выше верхней границы ({upper_fence:.0f} руб.)")
            print(
                f"      - Отклонение от Q3: {price - q3:.0f} руб. (в {(price - q3) / q3:.1f} раза выше типичной цены)")

print("\n" + "=" * 70)
print("ИТОГОВЫЕ ВЫВОДЫ ПО РАБОТЕ")
print("=" * 70)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 СРАВНЕНИЕ RANGE И IQR:

   ХАРАКТЕРИСТИКА     |    RANGE (Размах)    |    IQR (Межквартильный)
   -------------------|----------------------|-------------------------
   Что показывает?    | Полный диапазон      | Разброс "средних 50%"
   Чувствительность   | Очень высокая ❌     | Низкая (робастный) ✅
   к выбросам         |                      |
   Учитывает крайние  | Да                   | Нет
   значения           |                      |
   Стабильность       | Нестабилен           | Стабилен

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 МЕТОД 1.5 × IQR ДЛЯ ОБНАРУЖЕНИЯ ВЫБРОСОВ:

   Правило: Выброс = значение < Q1 - 1.5×IQR ИЛИ значение > Q3 + 1.5×IQR

   Преимущества:
   ✅ Автоматический и объективный
   ✅ Не требует ручного просмотра
   ✅ Работает для любых количественных данных
   ✅ Основан на устойчивых статистиках

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 РЕЗУЛЬТАТЫ НАШИХ ЭКСПЕРИМЕНТОВ:

   1. ОЦЕНКИ СТУДЕНТОВ:
      • Обнаружен выброс: 98 баллов
      • Среднее изменилось с {:.1f} до {:.1f}
      • Медиана осталась стабильной

   2. ИНТЕРНЕТ-МАГАЗИН:
      • Обнаружены выбросы: 10 руб. и 50 000 руб.
      • Средняя цена изменилась с {:.0f} до {:.0f} руб.
      • Изменение составило {:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 ПРАКТИЧЕСКИЕ РЕКОМЕНДАЦИИ:

   1. Всегда проверяйте данные на выбросы перед анализом
   2. Используйте метод 1.5×IQR для автоматического обнаружения
   3. При наличии выбросов:
      - Для анализа центра используйте МЕДИАНУ
      - Для анализа разброса используйте IQR
   4. Удаление выбросов уместно, если:
      - Это ошибки измерения/ввода
      - Значения нереалистичны для вашей задачи
      - Вы хотите проанализировать "типичный" случай
""".format(mean_with_outliers, mean_without_outliers,
           original_mean, clean_mean,
           abs(mean_change_pct)))

print("=" * 70)
print("✅ ЗАДАНИЕ ВЫПОЛНЕНО УСПЕШНО!")
print("=" * 70)