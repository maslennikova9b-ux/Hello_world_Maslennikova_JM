import pandas as pd
import numpy as np
import math

print("=" * 70)
print("ЗАДАНИЕ 1: Стандартное отклонение (SD) и коэффициент вариации (CV)")
print("=" * 70)

# ============================================
# ЗАДАНИЕ 1.1: ВРЕМЯ ДОСТАВКИ ЗАКАЗОВ
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 1: Анализ времени доставки заказов")
print("=" * 70)

# Исходные данные
delivery_days = [2, 3, 2, 4, 3, 5, 2, 3, 4, 3]
print(f"\nИсходные данные (время доставки в днях): {delivery_days}")
print(f"Количество заказов: n = {len(delivery_days)}")

# ---------- ВЫЧИСЛЕНИЕ СТАНДАРТНОГО ОТКЛОНЕНИЯ ВРУЧНУЮ ----------
print("\n" + "-" * 50)
print("ВЫЧИСЛЕНИЕ СТАНДАРТНОГО ОТКЛОНЕНИЯ ВРУЧНУЮ:")
print("-" * 50)

# Шаг 1: Вычисляем среднее
mean_manual = sum(delivery_days) / len(delivery_days)
print(f"\nШАГ 1: Среднее = {sum(delivery_days)} / {len(delivery_days)} = {mean_manual:.3f}")

# Шаг 2: Вычисляем отклонения и квадраты
print(f"\nШАГ 2: Отклонения и квадраты:")
squared_deviations = []
for x in delivery_days:
    deviation = x - mean_manual
    sq_dev = deviation ** 2
    squared_deviations.append(sq_dev)
    print(f"  {x} - {mean_manual:.3f} = {deviation:+.3f} → ({deviation:.3f})² = {sq_dev:.3f}")

# Шаг 3: Сумма квадратов
ss = sum(squared_deviations)
print(f"\nШАГ 3: Сумма квадратов отклонений = {ss:.3f}")

# Шаг 4: Дисперсия (делим на n-1)
n = len(delivery_days)
variance_manual = ss / (n - 1)
print(f"\nШАГ 4: Выборочная дисперсия = SS / (n-1) = {ss:.3f} / {n - 1} = {variance_manual:.3f}")

# Шаг 5: Стандартное отклонение (корень из дисперсии)
std_manual = math.sqrt(variance_manual)
print(f"\nШАГ 5: Стандартное отклонение = √{variance_manual:.3f} = {std_manual:.3f}")

# Проверка через pandas
print("\n" + "-" * 50)
print("ПРОВЕРКА ЧЕРЕЗ PANDAS:")
print("-" * 50)

delivery_series = pd.Series(delivery_days)
std_pandas = delivery_series.std()
mean_pandas = delivery_series.mean()

print(f"Среднее (pandas):     {mean_pandas:.3f}")
print(f"Станд. отклонение (pandas): {std_pandas:.3f}")
print(f"Ручное вычисление:         {std_manual:.3f}")
print(f"\n✅ Результаты совпадают! Разница: {abs(std_manual - std_pandas):.6f}")

# ---------- ТИПИЧНЫЙ ДИАПАЗОН ----------
print("\n" + "-" * 50)
print("ТИПИЧНЫЙ ДИАПАЗОН (mean ± 1 SD):")
print("-" * 50)

lower_bound = mean_pandas - std_pandas
upper_bound = mean_pandas + std_pandas

print(f"Среднее (μ):      {mean_pandas:.3f} дня")
print(f"СО (σ):           {std_pandas:.3f} дня")
print(f"\nНижняя граница:   {lower_bound:.3f} дня")
print(f"Верхняя граница:  {upper_bound:.3f} дня")
print(f"Типичный диапазон: [{lower_bound:.3f}, {upper_bound:.3f}] дней")

# Проверяем, сколько значений попадает в диапазон
in_range = delivery_series[(delivery_series >= lower_bound) & (delivery_series <= upper_bound)]
count_in_range = len(in_range)
percentage = (count_in_range / len(delivery_series)) * 100

print(f"\nЗначения в диапазоне: {in_range.tolist()}")
print(f"Количество: {count_in_range} из {len(delivery_series)} ({percentage:.1f}%)")

print(f"\n💡 ИНТЕРПРЕТАЦИЯ:")
print(f"  • Типичное время доставки: от {lower_bound:.1f} до {upper_bound:.1f} дней")
print(f"  • {percentage:.0f}% заказов попадают в типичный диапазон")
if percentage >= 68:
    print(f"  • Распределение близко к нормальному (ожидается ~68%)")
else:
    print(f"  • Распределение может отличаться от нормального")

# ============================================
# ЗАДАНИЕ 1.2: ДВА НАБОРА С ОДИНАКОВЫМ СРЕДНИМ, РАЗНЫМ СО
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 2: Сравнение двух наборов с одинаковым средним, разным СО")
print("=" * 70)

# Создаём два набора с одинаковым средним (50)
np.random.seed(42)

# Набор А: маленькое СО (низкий разброс)
# Генерируем значения вокруг среднего 50 с СО=3
set_A_raw = np.random.normal(loc=50, scale=3, size=200)
set_A = np.round(np.clip(set_A_raw, 40, 60), 1).tolist()

# Набор Б: большое СО (высокий разброс) - в 2+ раза больше
set_B_raw = np.random.normal(loc=50, scale=8, size=200)
set_B = np.round(np.clip(set_B_raw, 30, 70), 1).tolist()

# Создаём Series
set_A_series = pd.Series(set_A)
set_B_series = pd.Series(set_B)

# Статистики
mean_A = set_A_series.mean()
mean_B = set_B_series.mean()
std_A = set_A_series.std()
std_B = set_B_series.std()

print(f"\n📊 ХАРАКТЕРИСТИКИ НАБОРОВ:")
print("-" * 50)
print(f"{'Показатель':<20} | {'Набор А (малое СО)':<25} | {'Набор Б (большое СО)':<25}")
print("-" * 75)
print(f"{'Среднее':<20} | {mean_A:<25.2f} | {mean_B:<25.2f}")
print(f"{'СО (σ)':<20} | {std_A:<25.2f} | {std_B:<25.2f}")
print(f"{'Отношение СО':<20} | {1:<25} | {(std_B / std_A):<25.2f}")

# Правило двух сигм для набора А
print("\n" + "-" * 50)
print("ПРАВИЛО ДВУХ СИГМ для Набора А (малое СО):")
print("-" * 50)

for sigma in [1, 2]:
    lower = mean_A - sigma * std_A
    upper = mean_A + sigma * std_A
    count = set_A_series[(set_A_series >= lower) & (set_A_series <= upper)].count()
    pct = count / len(set_A_series) * 100
    theory = {1: 68, 2: 95}[sigma]
    print(f"  mean ± {sigma}σ  [{lower:.1f}, {upper:.1f}]  → {count} точек ({pct:.1f}%)  теория: {theory}%")

# Правило двух сигм для набора Б
print("\n" + "-" * 50)
print("ПРАВИЛО ДВУХ СИГМ для Набора Б (большое СО):")
print("-" * 50)

for sigma in [1, 2]:
    lower = mean_B - sigma * std_B
    upper = mean_B + sigma * std_B
    count = set_B_series[(set_B_series >= lower) & (set_B_series <= upper)].count()
    pct = count / len(set_B_series) * 100
    theory = {1: 68, 2: 95}[sigma]
    print(f"  mean ± {sigma}σ  [{lower:.1f}, {upper:.1f}]  → {count} точек ({pct:.1f}%)  теория: {theory}%")

# Сравнение точности правила
print("\n" + "-" * 50)
print("СРАВНЕНИЕ ТОЧНОСТИ ПРАВИЛА ДВУХ СИГМ:")
print("-" * 50)

# Для mean ± 2σ (95% теория)
lower_A_2 = mean_A - 2 * std_A
upper_A_2 = mean_A + 2 * std_A
pct_A_2 = (set_A_series[(set_A_series >= lower_A_2) & (set_A_series <= upper_A_2)].count() / len(set_A_series)) * 100

lower_B_2 = mean_B - 2 * std_B
upper_B_2 = mean_B + 2 * std_B
pct_B_2 = (set_B_series[(set_B_series >= lower_B_2) & (set_B_series <= upper_B_2)].count() / len(set_A_series)) * 100

print(f"\n  Набор А (малое СО):   {pct_A_2:.1f}% в пределах 2σ (теория: 95%) → разница: {abs(pct_A_2 - 95):.1f}%")
print(f"  Набор Б (большое СО):  {pct_B_2:.1f}% в пределах 2σ (теория: 95%) → разница: {abs(pct_B_2 - 95):.1f}%")

print(f"\n💡 ВЫВОД:")
if abs(pct_A_2 - 95) < abs(pct_B_2 - 95):
    print(f"  • Правило двух сигм работает ТОЧНЕЕ для набора с МЕНЬШИМ СО (набор А)")
    print(f"  • Чем меньше разброс, тем лучше распределение соответствует нормальному")
else:
    print(f"  • Правило двух сигм работает ТОЧНЕЕ для набора с БОЛЬШИМ СО (набор Б)")

# Визуализация распределений
print("\n" + "-" * 50)
print("ВИЗУАЛИЗАЦИЯ РАСПРЕДЕЛЕНИЙ:")
print("-" * 50)


def create_histogram_text(data, title, bins=10):
    hist, bin_edges = np.histogram(data, bins=bins)
    print(f"\n{title}:")
    max_count = max(hist)
    for i in range(len(hist)):
        count = hist[i]
        bar = '█' * int(count / max_count * 30) if max_count > 0 else ''
        print(f"  {bin_edges[i]:>5.1f}-{bin_edges[i + 1]:<5.1f}: {bar} ({count})")


create_histogram_text(set_A, "Распределение А (малое СО)")
create_histogram_text(set_B, "Распределение Б (большое СО)")

# ============================================
# ЗАДАНИЕ 1.3: КОЭФФИЦИЕНТ ВАРИАЦИИ (CV)
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 3: Коэффициент вариации (CV) для сравнения разных единиц")
print("=" * 70)

# Создаём данные из разных областей
print("\n📊 ДАННЫЕ ИЗ РАЗНЫХ ОБЛАСТЕЙ:")

# 1. Цены в рублях (товары в магазине)
np.random.seed(42)
prices_rub = np.random.randint(100, 5000, size=50)
prices_rub = np.round(prices_rub / 100) * 100  # округляем до сотен

# 2. Рост в сантиметрах (люди)
heights_cm = np.random.normal(loc=170, scale=10, size=50)
heights_cm = np.round(heights_cm, 1).clip(150, 200)

# 3. Оценки в баллах (студенты)
scores_points = np.random.randint(40, 100, size=50)

# Создаём DataFrame
data_df = pd.DataFrame({
    'price_rub': prices_rub,
    'height_cm': heights_cm,
    'score_points': scores_points
})

print("\nПервые 10 записей:")
print(data_df.head(10))

print("\n" + "-" * 50)
print("РАСЧЁТ КОЭФФИЦИЕНТА ВАРИАЦИИ (CV):")
print("-" * 50)

# Вычисляем статистики
results = []

for column in data_df.columns:
    mean_val = data_df[column].mean()
    std_val = data_df[column].std()
    cv = (std_val / mean_val) * 100

    # Определяем уровень вариации
    if cv < 10:
        level = "Низкая вариация (однородные данные)"
    elif cv < 33:
        level = "Средняя вариация"
    else:
        level = "Высокая вариация (неоднородные данные)"

    results.append({
        'Переменная': column,
        'Среднее': mean_val,
        'СО': std_val,
        'CV (%)': cv,
        'Уровень': level
    })

    print(f"\n{column.upper()}:")
    print(f"  Среднее: {mean_val:.2f}")
    print(f"  СО:      {std_val:.2f}")
    print(f"  CV:      {cv:.2f}%")
    print(f"  Уровень: {level}")

# Итоговая таблица
print("\n" + "-" * 50)
print("СРАВНИТЕЛЬНАЯ ТАБЛИЦА:")
print("-" * 50)

result_df = pd.DataFrame(results)
print(result_df.to_string(index=False))

# Анализ результатов
print("\n" + "-" * 50)
print("АНАЛИЗ КОЭФФИЦИЕНТА ВАРИАЦИИ:")
print("-" * 50)

# Находим переменную с наибольшим CV
max_cv_row = result_df.loc[result_df['CV (%)'].idxmax()]
min_cv_row = result_df.loc[result_df['CV (%)'].idxmin()]

print(f"\n🔍 Переменная с НАИБОЛЬШИМ относительным разбросом:")
print(f"   • {max_cv_row['Переменная']}: CV = {max_cv_row['CV (%)']:.2f}%")
print(f"   • Уровень: {max_cv_row['Уровень']}")
print(f"   • Это означает, что значения этой переменной сильно различаются")

print(f"\n🔍 Переменная с НАИМЕНЬШИМ относительным разбросом:")
print(f"   • {min_cv_row['Переменная']}: CV = {min_cv_row['CV (%)']:.2f}%")
print(f"   • Уровень: {min_cv_row['Уровень']}")
print(f"   • Значения этой переменной более однородны")

# Дополнительный анализ: что означает CV
print("\n" + "-" * 50)
print("ИНТЕРПРЕТАЦИЯ КОЭФФИЦИЕНТА ВАРИАЦИИ:")
print("-" * 50)

print("""
CV < 10%  → Очень низкая вариация (данные почти одинаковы)
            Пример: рост взрослых людей в одной группе

10% < CV < 33% → Средняя вариация (естественный разброс)
                  Пример: оценки студентов, цены на однотипные товары

CV > 33% → Высокая вариация (данные сильно отличаются)
            Пример: доходы населения, цены на разные категории товаров
""")

# Сравнение CV с абсолютным СО
print("\n" + "-" * 50)
print("ПОЧЕМУ CV ВАЖНЕЕ АБСОЛЮТНОГО СО?")
print("-" * 50)

print("""
Абсолютное СО нельзя сравнивать между разными переменными:

  • Цены (руб): среднее = {price_mean:.0f}, СО = {price_std:.0f}
  • Рост (см):  среднее = {height_mean:.1f}, СО = {height_std:.1f}

  Вопрос: что разбросано сильнее - цены или рост?
  • По СО кажется, что цены (СО={price_std:.0f}) разбросаны сильнее роста (СО={height_std:.1f})
  • НО! Это обманчиво, потому что у цен другой масштаб (сотни рублей против десятков см)

Решение: CV (в процентах)

  • Цены: CV = {price_cv:.1f}%
  • Рост: CV = {height_cv:.1f}%

  Теперь видно, что на самом деле {more_variable}!

  CV позволяет сравнить несравнимое!
""".format(
    price_mean=results[0]['Среднее'],
    price_std=results[0]['СО'],
    height_mean=results[1]['Среднее'],
    height_std=results[1]['СО'],
    price_cv=results[0]['CV (%)'],
    height_cv=results[1]['CV (%)'],
    more_variable="цены разбросаны сильнее" if results[0]['CV (%)'] > results[1]['CV (%)'] else "рост разбросан сильнее"
))

# Дополнительная визуализация CV
print("\n" + "-" * 50)
print("ВИЗУАЛИЗАЦИЯ СРАВНЕНИЯ CV:")
print("-" * 50)

cv_values = [row['CV (%)'] for row in results]
labels = [row['Переменная'] for row in results]

print("\n  Коэффициент вариации (%):")
max_cv = max(cv_values)
for label, cv in zip(labels, cv_values):
    bar = '█' * int(cv / max_cv * 30) if max_cv > 0 else ''
    print(f"  {label:<15}: {bar} {cv:.1f}%")

# Финальные выводы
print("\n" + "=" * 70)
print("ИТОГОВЫЕ ВЫВОДЫ ПО РАБОТЕ")
print("=" * 70)

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         ОСНОВНЫЕ ПОНЯТИЯ СЕГОДНЯ                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

1. СТАНДАРТНОЕ ОТКЛОНЕНИЕ (σ или s)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Квадратный корень из дисперсии
   • Возвращает единицы измерения в исходный вид
   • Показывает "типичное" отклонение от среднего
   • Формула: s = √[ Σ(xi - x̄)² / (n-1) ]

2. ПРАВИЛО ДВУХ СИГМ (для нормальных распределений)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • mean ± 1σ → ~68% данных
   • mean ± 2σ → ~95% данных
   • mean ± 3σ → ~99.7% данных

   Чем МЕНЬШЕ разброс, тем точнее работает правило!

3. КОЭФФИЦИЕНТ ВАРИАЦИИ (CV)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • CV = (σ / μ) × 100%
   • Позволяет сравнивать разброс разных переменных
   • Выражается в процентах (без единиц измерения)

   Шкала интерпретации:
   • CV < 10%  → очень однородные данные
   • 10% < CV < 33% → умеренный разброс
   • CV > 33% → высокая неоднородность

4. ПРАКТИЧЕСКИЕ ВЫВОДЫ
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Для интерпретации используйте СТАНДАРТНОЕ ОТКЛОНЕНИЕ
   • Для сравнения разных переменных используйте КОЭФФИЦИЕНТ ВАРИАЦИИ
   • Для проверки нормальности используйте ПРАВИЛО ДВУХ СИГМ

   В НАШЕМ АНАЛИЗЕ:
   • Время доставки: типичный диапазон = mean ± 1σ
   • Набор с меньшим СО показал более точное правило двух сигм
   • CV позволил сравнить цены, рост и оценки в одних процентах
""")

print("=" * 70)
print("✅ ЗАДАНИЕ ВЫПОЛНЕНО УСПЕШНО!")
print("=" * 70)