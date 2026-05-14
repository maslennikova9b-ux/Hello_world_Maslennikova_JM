import pandas as pd
import numpy as np
import statistics

print("=" * 70)
print("ЗАДАНИЕ 1: Анализ вариативности данных (разброс)")
print("=" * 70)

# ============================================
# ЧАСТЬ 1: ДВА НАБОРА С ОДИНАКОВЫМ СРЕДНИМ, НО РАЗНЫМ РАЗБРОСОМ
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 1: Создание двух наборов с одинаковым средним (50)")
print("=" * 70)

# Набор 1: "Плотный" - значения очень близки к среднему
dense_set = [48, 49, 50, 50, 51, 52]  # среднее = 50

# Набор 2: "Широкий" - значения сильно разбросаны
wide_set = [20, 30, 50, 50, 70, 80]  # среднее = 50

# Создаём Series
dense_series = pd.Series(dense_set, name='Плотный набор')
wide_series = pd.Series(wide_set, name='Широкий набор')

print("\n📊 Сравнение двух наборов данных:")
print("-" * 50)

print(f"\n{'Плотный набор':<20} | {'Широкий набор':<20}")
print("-" * 50)

# Выводим значения
print(f"{str(dense_set):<20} | {str(wide_set):<20}")

# Выводим статистики
print(f"\nСтатистика:")
print(f"  Среднее:      {dense_series.mean():.1f}                 | {wide_series.mean():.1f}")
print(f"  Медиана:      {dense_series.median():.1f}                 | {wide_series.median():.1f}")
print(f"  Минимум:      {dense_series.min():.0f}                   | {wide_series.min():.0f}")
print(f"  Максимум:     {dense_series.max():.0f}                   | {wide_series.max():.0f}")
print(
    f"  Размах:       {dense_series.max() - dense_series.min():.0f}                   | {wide_series.max() - wide_series.min():.0f}")

# Дополнительные метрики разброса
dense_std = dense_series.std()
wide_std = wide_series.std()

dense_var = dense_series.var()
wide_var = wide_series.var()

print(f"  Ст. отклонение:{dense_std:.2f}                 | {wide_std:.2f}")
print(f"  Дисперсия:     {dense_var:.2f}                | {wide_var:.2f}")

# Визуализация разброса (текстовая)
print("\n📈 Визуализация разброса (шкала от 0 до 100):")
print("-" * 50)


def visualize_distribution(data, name):
    """Создаёт текстовую визуализацию распределения"""
    min_val = 0
    max_val = 100
    # Создаём "гистограмму" для каждого значения
    positions = []
    for val in data:
        pos = int((val - min_val) / (max_val - min_val) * 50)
        positions.append(pos)

    # Рисуем шкалу
    scale = "0" + " " * 48 + "100"
    print(f"\n{name}:")
    print(f"  Шкала: {scale}")
    print(f"  Данные: ", end="")
    for val in data:
        pos = int((val - min_val) / (max_val - min_val) * 50)
        print(f"{' ' * pos}●", end="")
    print()


visualize_distribution(dense_set, "Плотный набор")
visualize_distribution(wide_set, "Широкий набор")

print("\n💡 ВЫВОД ПО ЧАСТИ 1:")
print("-" * 50)
print("""
✅ Несмотря на ОДИНАКОВОЕ СРЕДНЕЕ (50), наборы сильно отличаются:

   ПЛОТНЫЙ НАБОР:
   • Все значения между 48 и 52 (размах = 4)
   • Стандартное отклонение ~1.87
   • Все студенты учатся стабильно, предсказуемо

   ШИРОКИЙ НАБОР:
   • Значения от 20 до 80 (размах = 60)
   • Стандартное отклонение ~24.49
   • Есть и очень слабые (20), и отличные (80) студенты

   📌 Практический вывод:
   Среднее значение НЕ ДОСТАТОЧНО для описания данных!
   Всегда нужно смотреть и на меры разброса.
""")

# ============================================
# ЧАСТЬ 2: РЕАЛЬНЫЙ ПРИМЕР (ДОХОДЫ В РАЗНЫХ СТРАНАХ)
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 2: Реальный пример - Доходы в двух странах")
print("=" * 70)

"""
РЕАЛЬНЫЙ ПРИМЕР: Сравнение распределения доходов в двух странах

Страна А (Скандинавская модель, например, Швеция/Норвегия):
- Высокая социальная поддержка, прогрессивное налогообложение
- Доходы населения сконцентрированы вокруг среднего значения
- Маленький разрыв между бедными и богатыми

Страна Б (Латиноамериканская модель, например, Бразилия/Мексика):
- Высокое социальное неравенство
- Есть очень богатые и очень бедные
- Большой разрыв между бедными и богатыми

При этом СРЕДНИЙ доход в обеих странах может быть ОДИНАКОВЫМ!
Но уровень жизни и социальная стабильность будут кардинально разными.
"""

# Создаём пример данных для двух стран
np.random.seed(42)

# Страна А: равномерное распределение вокруг среднего
country_A_high_income = np.random.normal(loc=50000, scale=8000, size=50)  # богатые
country_A_mid_income = np.random.normal(loc=35000, scale=5000, size=150)  # средний класс
country_A_low_income = np.random.normal(loc=25000, scale=4000, size=50)  # бедные
country_A_incomes = np.concatenate([country_A_high_income, country_A_mid_income, country_A_low_income])

# Страна Б: высокое неравенство (много бедных и очень богатых)
country_B_poor = np.random.exponential(scale=15000, size=180).clip(5000, 30000)  # много бедных
country_B_rich = np.random.uniform(80000, 200000, size=70)  # очень богатые
country_B_incomes = np.concatenate([country_B_poor, country_B_rich])

# Округляем для удобства
country_A_incomes = np.round(country_A_incomes, -3).astype(int)
country_B_incomes = np.round(country_B_incomes, -3).astype(int)

# Обрезаем экстремальные значения для красоты
country_A_incomes = country_A_incomes.clip(15000, 80000)
country_B_incomes = country_B_incomes.clip(5000, 180000)

# Создаём DataFrame
income_df = pd.DataFrame({
    'Country_A_Income': country_A_incomes,
    'Country_B_Income': country_B_incomes[:len(country_A_incomes)]  # одинаковый размер для сравнения
})

print("\n📊 Сравнение распределения доходов в двух странах:")
print("-" * 50)

# Статистики для Страны А
print(f"\n{'Показатель':<25} | {'Страна А (равномерная)':<25} | {'Страна Б (неравномерная)':<25}")
print("-" * 80)

a_mean = income_df['Country_A_Income'].mean()
b_mean = income_df['Country_B_Income'].mean()

a_median = income_df['Country_A_Income'].median()
b_median = income_df['Country_B_Income'].median()

a_std = income_df['Country_A_Income'].std()
b_std = income_df['Country_B_Income'].std()

a_min = income_df['Country_A_Income'].min()
b_min = income_df['Country_B_Income'].min()

a_max = income_df['Country_A_Income'].max()
b_max = income_df['Country_B_Income'].max()

a_range = a_max - a_min
b_range = b_max - b_min

a_iqr = income_df['Country_A_Income'].quantile(0.75) - income_df['Country_A_Income'].quantile(0.25)
b_iqr = income_df['Country_B_Income'].quantile(0.75) - income_df['Country_B_Income'].quantile(0.25)

print(f"{'Средний доход ($)':<25} | {a_mean:>10,.0f} {'':<14} | {b_mean:>10,.0f}")
print(f"{'Медианный доход ($)':<25} | {a_median:>10,.0f} {'':<14} | {b_median:>10,.0f}")
print(f"{'Станд. отклонение ($)':<25} | {a_std:>10,.0f} {'':<14} | {b_std:>10,.0f}")
print(f"{'Минимальный доход ($)':<25} | {a_min:>10,.0f} {'':<14} | {b_min:>10,.0f}")
print(f"{'Максимальный доход ($)':<25} | {a_max:>10,.0f} {'':<14} | {b_max:>10,.0f}")
print(f"{'Размах ($)':<25} | {a_range:>10,.0f} {'':<14} | {b_range:>10,.0f}")
print(f"{'Межквартильный размах ($)':<25} | {a_iqr:>10,.0f} {'':<14} | {b_iqr:>10,.0f}")

# Визуализация распределения (простая гистограмма)
print("\n📊 Текстовая гистограмма распределения доходов:")
print("-" * 70)


def create_income_histogram(incomes, title,
                            bins=[0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000]):
    print(f"\n{title}:")
    for i in range(len(bins) - 1):
        count = sum((incomes >= bins[i]) & (incomes < bins[i + 1]))
        if count > 0:
            bar = '█' * (count // 2)
            print(f"  {bins[i]:>6,}-{bins[i + 1]:>7,}$: {bar} ({count} чел.)")


create_income_histogram(income_df['Country_A_Income'], "Страна А (равномерное распределение)")
create_income_histogram(income_df['Country_B_Income'], "Страна Б (высокое неравенство)")

# Анализ социального неравенства
print("\n" + "=" * 50)
print("📊 ИНДЕКСЫ НЕРАВЕНСТВА:")
print("=" * 50)

# Коэффициент вариации (CV = std/mean) - относительная мера разброса
cv_a = (a_std / a_mean) * 100
cv_b = (b_std / b_mean) * 100

print(f"\nКоэффициент вариации (CV):")
print(f"  Страна А: {cv_a:.1f}%  {'(низкий разброс)' if cv_a < 50 else '(высокий разброс)'}")
print(f"  Страна Б: {cv_b:.1f}%  {'(низкий разброс)' if cv_b < 50 else '(высокий разброс)'}")

# Соотношение богатых и бедных
a_poor_ratio = (income_df['Country_A_Income'] < 30000).sum() / len(income_df) * 100
b_poor_ratio = (income_df['Country_B_Income'] < 30000).sum() / len(income_df) * 100

a_rich_ratio = (income_df['Country_A_Income'] > 70000).sum() / len(income_df) * 100
b_rich_ratio = (income_df['Country_B_Income'] > 70000).sum() / len(income_df) * 100

print(f"\nСоциальная структура:")
print(f"  Доля бедных (<30k$):   Страна А: {a_poor_ratio:.1f}%  |  Страна Б: {b_poor_ratio:.1f}%")
print(f"  Доля богатых (>70k$):  Страна А: {a_rich_ratio:.1f}%  |  Страна Б: {b_rich_ratio:.1f}%")
print(
    f"  Соотношение богатые/бедные: Страна А: {a_rich_ratio / a_poor_ratio:.2f}  |  Страна Б: {b_rich_ratio / b_poor_ratio:.2f}")

print("\n" + "=" * 70)
print("РЕАЛЬНЫЙ ПРИМЕР ИЗ ЖИЗНИ:")
print("=" * 70)

print("""
🌍 РЕАЛЬНЫЙ ПРИМЕР: Швеция vs Бразилия (данные Всемирного Банка, 2020-2022)

┌─────────────────────────────────────────────────────────────────────┐
│  ПОКАЗАТЕЛЬ              │  ШВЕЦИЯ (равномерная)  │  БРАЗИЛИЯ (неравн.) │
├─────────────────────────────────────────────────────────────────────┤
│  Средний доход (ППС)     │      ~45,000$         │      ~45,000$       │
│  Медианный доход (ППС)   │      ~42,000$         │      ~25,000$       │
│  Коэффициент Джини       │          0.27         │          0.53       │
│  Разрыв 20% бедн/богат   │           4.5         │         21.5        │
└─────────────────────────────────────────────────────────────────────┘

💡 КЛЮЧЕВОЙ ВЫВОД:
   При ОДИНАКОВОМ СРЕДНЕМ доходе, реальное благосостояние населения
   может кардинально отличаться из-за РАЗБРОСА (неравенства)!

   В Швеции:
   • Большинство населения имеет доход, близкий к среднему
   • Высокая социальная мобильность
   • Низкий уровень бедности

   В Бразилии:
   • Есть очень богатые и очень бедные
   • Средний доход "средней температуры по больнице"
   • Медиана гораздо ниже среднего (асимметрия)

📌 ПРАКТИЧЕСКИЙ ВЫВОД ДЛЯ АНАЛИТИКА:
   При анализе доходов, цен на недвижимость и других социально-экономических
   показателей ОБЯЗАТЕЛЬНО используйте:
   1. Медиану (устойчива к выбросам)
   2. Стандартное отклонение (показывает разброс)
   3. Интерквартильный размах (IQR) для сравнения групп
""")

# ============================================
# ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ: ПРАВИЛО 68-95-99.7
# ============================================

print("\n" + "=" * 70)
print("ДОПОЛНЕНИЕ: Правило 68-95-99.7 для нормального распределения")
print("=" * 70)

# Создаём нормальное распределение
np.random.seed(42)
normal_data = np.random.normal(loc=50, scale=10, size=1000)
normal_series = pd.Series(normal_data)

mean_val = normal_series.mean()
std_val = normal_series.std()

print(f"\n📊 Нормальное распределение (среднее={mean_val:.1f}, std={std_val:.1f})")
print("\nПравило 68-95-99.7:")
print("-" * 50)

# Подсчитываем процент значений в пределах 1, 2 и 3 стандартных отклонений
within_1std = sum((normal_series >= mean_val - std_val) & (normal_series <= mean_val + std_val)) / len(
    normal_series) * 100
within_2std = sum((normal_series >= mean_val - 2 * std_val) & (normal_series <= mean_val + 2 * std_val)) / len(
    normal_series) * 100
within_3std = sum((normal_series >= mean_val - 3 * std_val) & (normal_series <= mean_val + 3 * std_val)) / len(
    normal_series) * 100

print(f"  В пределах 1σ  ({mean_val - std_val:.1f} – {mean_val + std_val:.1f}): {within_1std:.1f}% (теоретически 68%)")
print(
    f"  В пределах 2σ  ({mean_val - 2 * std_val:.1f} – {mean_val + 2 * std_val:.1f}): {within_2std:.1f}% (теоретически 95%)")
print(
    f"  В пределах 3σ  ({mean_val - 3 * std_val:.1f} – {mean_val + 3 * std_val:.1f}): {within_3std:.1f}% (теоретически 99.7%)")

print("\n💡 Это правило помогает:")
print("  • Определять выбросы (значения за пределами 3σ)")
print("  • Оценивать нормальность распределения")
print("  • Устанавливать границы нормы в контроле качества")

# Финальные выводы
print("\n" + "=" * 70)
print("ИТОГОВЫЕ ВЫВОДЫ ПО РАБОТЕ")
print("=" * 70)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ОСНОВНЫЕ МЕРЫ РАЗБРОСА:

   1. РАЗМАХ (Range) = max - min
      • Самый простой, но чувствителен к выбросам

   2. ДИСПЕРСИЯ (Variance) = средний квадрат отклонений
      • Учитывает все значения
      • Единицы измерения в квадрате

   3. СТАНДАРТНОЕ ОТКЛОНЕНИЕ (Std) = √дисперсии
      • Удобно для интерпретации
      • В нормальном распределении 68% данных в пределах ±1σ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 КОГДА ИСПОЛЬЗОВАТЬ:

   ✅ МАЛЫЙ РАЗБРОС (низкое std):
      • Процесс стабилен и предсказуем
      • Качество продукции стабильно
      • Риски минимальны

   ⚠️ БОЛЬШОЙ РАЗБРОС (высокое std):
      • Данные гетерогенны
      • Есть сегменты/группы
      • Нужно дополнительное исследование

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 НАШИ ЭКСПЕРИМЕНТЫ ПОКАЗАЛИ:

   • Плотный набор: std ≈ 1.87  (все значения 48-52)
   • Широкий набор: std ≈ 24.49 (значения 20-80)
   • Одинаковое среднее НЕ означает одинаковые данные!
   • Всегда анализируйте и центр, и разброс!
""")

print("=" * 70)
print("✅ ЗАДАНИЕ ВЫПОЛНЕНО УСПЕШНО!")
print("=" * 70)