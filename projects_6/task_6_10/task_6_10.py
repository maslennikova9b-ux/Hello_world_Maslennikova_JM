import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# Попробуем импортировать seaborn, если он установлен
try:
    import seaborn as sns

    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("⚠️ Seaborn не установлен. Устанавливаем через pip...")
    print("   Выполните: pip install seaborn")
    print("   Или будет использован демонстрационный датасет\n")

print("=" * 70)
print("ИТОГОВОЕ ЗАДАНИЕ: Комплексный анализ мер разброса")
print("=" * 70)

# ============================================
# ЗАДАНИЕ 1.1: АНАЛИЗ ПЕРЕМЕННОЙ С ВЫБРОСАМИ
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 1: Анализ переменной с выбросами")
print("=" * 70)

# Создаём набор данных с выбросами (время выполнения задач в минутах)
np.random.seed(42)

# Нормальные значения (большинство задач 20-40 минут)
normal_tasks = np.random.normal(loc=30, scale=5, size=45)
normal_tasks = np.round(normal_tasks.clip(20, 45), 1)

# Добавляем выбросы (очень долгие задачи)
outliers = [85.0, 92.5, 105.0, 60.0, 120.0]  # 5 выбросов

# Объединяем данные
task_times = np.concatenate([normal_tasks, outliers])
np.random.shuffle(task_times)  # перемешиваем

# Создаём DataFrame
df_original = pd.DataFrame({
    'task_id': range(1, len(task_times) + 1),
    'time_minutes': task_times
})

print(f"\n📊 Исходный набор данных:")
print(f"   Количество записей: {len(df_original)}")
print(f"   Переменная: время выполнения задачи (минуты)")
print(f"\n   Первые 10 записей:")
print(df_original.head(10))
print(f"\n   Статистика:")
print(f"   Среднее: {df_original['time_minutes'].mean():.2f}")
print(f"   Медиана: {df_original['time_minutes'].median():.2f}")

# ============================================
# ЧАСТЬ 1а: РАСЧЁТ МЕР РАЗБРОСА ДО ОЧИСТКИ
# ============================================

print("\n" + "-" * 50)
print("1а. МЕРЫ РАЗБРОСА ДО ОЧИСТКИ ОТ ВЫБРОСОВ:")
print("-" * 50)


# Вычисляем все меры разброса
def calculate_spread_measures(series):
    """Вычисляет все меры разброса для Series"""
    range_val = series.max() - series.min()
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    variance = series.var()
    std = series.std()
    cv = (std / series.mean()) * 100 if series.mean() != 0 else np.nan

    # Находим выбросы методом 1.5×IQR
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outliers = series[(series < lower_fence) | (series > upper_fence)]

    return {
        'count': len(series),
        'mean': series.mean(),
        'median': series.median(),
        'range': range_val,
        'q1': q1,
        'q3': q3,
        'iqr': iqr,
        'variance': variance,
        'std': std,
        'cv': cv,
        'outliers_count': len(outliers),
        'outliers': outliers.tolist(),
        'lower_fence': lower_fence,
        'upper_fence': upper_fence
    }


# Расчёт для исходных данных
original_measures = calculate_spread_measures(df_original['time_minutes'])

print(f"\n📈 Базовые статистики:")
print(f"   Количество значений: n = {original_measures['count']}")
print(f"   Среднее (μ):         {original_measures['mean']:.2f} мин")
print(f"   Медиана:             {original_measures['median']:.2f} мин")

print(f"\n📊 Меры разброса:")
print(f"   Размах (Range):      {original_measures['range']:.2f} мин")
print(f"   Q1 (25-й перцентиль): {original_measures['q1']:.2f} мин")
print(f"   Q3 (75-й перцентиль): {original_measures['q3']:.2f} мин")
print(f"   IQR:                 {original_measures['iqr']:.2f} мин")
print(f"   Дисперсия (s²):      {original_measures['variance']:.2f} мин²")
print(f"   Станд. отклонение:   {original_measures['std']:.2f} мин")
print(f"   Коэфф. вариации (CV): {original_measures['cv']:.1f}%")

print(f"\n🔍 Обнаружение выбросов (метод 1.5×IQR):")
print(f"   Нижняя граница:      {original_measures['lower_fence']:.2f} мин")
print(f"   Верхняя граница:      {original_measures['upper_fence']:.2f} мин")
print(f"   Найдено выбросов:     {original_measures['outliers_count']}")
if original_measures['outliers_count'] > 0:
    print(f"   Значения-выбросы:     {original_measures['outliers']}")

# ============================================
# ЧАСТЬ 1б: УДАЛЕНИЕ ВЫБРОСОВ
# ============================================

print("\n" + "-" * 50)
print("1б. УДАЛЕНИЕ ВЫБРОСОВ МЕТОДОМ 1.5×IQR:")
print("-" * 50)

# Удаляем выбросы
clean_data = df_original[
    (df_original['time_minutes'] >= original_measures['lower_fence']) &
    (df_original['time_minutes'] <= original_measures['upper_fence'])
    ]

df_clean = clean_data.copy()
print(f"\n   Исходное количество: {len(df_original)}")
print(f"   Удалено выбросов:    {len(df_original) - len(df_clean)}")
print(f"   Очищенный набор:     {len(df_clean)} записей")

# ============================================
# ЧАСТЬ 1в: ПЕРЕРАСЧЁТ ПОСЛЕ ОЧИСТКИ
# ============================================

print("\n" + "-" * 50)
print("1в. МЕРЫ РАЗБРОСА ПОСЛЕ ОЧИСТКИ ОТ ВЫБРОСОВ:")
print("-" * 50)

# Расчёт для очищенных данных
clean_measures = calculate_spread_measures(df_clean['time_minutes'])

print(f"\n📈 Базовые статистики:")
print(f"   Количество значений: n = {clean_measures['count']}")
print(f"   Среднее (μ):         {clean_measures['mean']:.2f} мин")
print(f"   Медиана:             {clean_measures['median']:.2f} мин")

print(f"\n📊 Меры разброса:")
print(f"   Размах (Range):      {clean_measures['range']:.2f} мин")
print(f"   Q1 (25-й перцентиль): {clean_measures['q1']:.2f} мин")
print(f"   Q3 (75-й перцентиль): {clean_measures['q3']:.2f} мин")
print(f"   IQR:                 {clean_measures['iqr']:.2f} мин")
print(f"   Дисперсия (s²):      {clean_measures['variance']:.2f} мин²")
print(f"   Станд. отклонение:   {clean_measures['std']:.2f} мин")
print(f"   Коэфф. вариации (CV): {clean_measures['cv']:.1f}%")

# ============================================
# СРАВНИТЕЛЬНАЯ ТАБЛИЦА
# ============================================

print("\n" + "-" * 50)
print("СРАВНИТЕЛЬНАЯ ТАБЛИЦА: ДО vs ПОСЛЕ ОЧИСТКИ")
print("-" * 50)

# Создаём DataFrame для сравнения
comparison_df = pd.DataFrame({
    'Мера': ['Среднее', 'Медиана', 'Размах (Range)', 'Q1', 'Q3',
             'IQR', 'Дисперсия', 'Станд. отклонение', 'CV (%)', 'Количество'],
    'До очистки': [
        f"{original_measures['mean']:.2f}",
        f"{original_measures['median']:.2f}",
        f"{original_measures['range']:.2f}",
        f"{original_measures['q1']:.2f}",
        f"{original_measures['q3']:.2f}",
        f"{original_measures['iqr']:.2f}",
        f"{original_measures['variance']:.2f}",
        f"{original_measures['std']:.2f}",
        f"{original_measures['cv']:.1f}",
        f"{original_measures['count']}"
    ],
    'После очистки': [
        f"{clean_measures['mean']:.2f}",
        f"{clean_measures['median']:.2f}",
        f"{clean_measures['range']:.2f}",
        f"{clean_measures['q1']:.2f}",
        f"{clean_measures['q3']:.2f}",
        f"{clean_measures['iqr']:.2f}",
        f"{clean_measures['variance']:.2f}",
        f"{clean_measures['std']:.2f}",
        f"{clean_measures['cv']:.1f}",
        f"{clean_measures['count']}"
    ],
    'Изменение (%)': [
        f"{(clean_measures['mean'] / original_measures['mean'] - 1) * 100:+.1f}",
        f"{(clean_measures['median'] / original_measures['median'] - 1) * 100:+.1f}",
        f"{(clean_measures['range'] / original_measures['range'] - 1) * 100:+.1f}",
        f"{(clean_measures['q1'] / original_measures['q1'] - 1) * 100:+.1f}",
        f"{(clean_measures['q3'] / original_measures['q3'] - 1) * 100:+.1f}",
        f"{(clean_measures['iqr'] / original_measures['iqr'] - 1) * 100:+.1f}",
        f"{(clean_measures['variance'] / original_measures['variance'] - 1) * 100:+.1f}",
        f"{(clean_measures['std'] / original_measures['std'] - 1) * 100:+.1f}",
        f"{(clean_measures['cv'] / original_measures['cv'] - 1) * 100:+.1f}",
        f"{(clean_measures['count'] / original_measures['count'] - 1) * 100:+.1f}"
    ]
})

print("\n", comparison_df.to_string(index=False))

# Анализ изменений
print("\n" + "-" * 50)
print("📊 АНАЛИЗ ИЗМЕНЕНИЙ:")
print("-" * 50)

mean_change = (clean_measures['mean'] - original_measures['mean']) / original_measures['mean'] * 100
median_change = (clean_measures['median'] - original_measures['median']) / original_measures['median'] * 100
std_change = (clean_measures['std'] - original_measures['std']) / original_measures['std'] * 100

print(f"""
  • Среднее изменилось на {mean_change:+.1f}%
  • Медиана изменилась на {median_change:+.1f}%
  • Стандартное отклонение изменилось на {std_change:+.1f}%

  💡 ВЫВОД: Выбросы сильно влияют на среднее и стандартное отклонение,
     но гораздо меньше на медиану и IQR.
""")

# ============================================
# ЧАСТЬ 2: АНАЛИЗ ДАТАСЕТА SEABORN
# ============================================

print("\n" + "=" * 70)
print("ЧАСТЬ 2: Анализ датасета seaborn")
print("=" * 70)


# Функция для анализа датасета
def analyze_dataset(df, name):
    """Анализирует все числовые переменные датасета"""
    print(f"\n📊 ДАТАСЕТ: {name}")
    print("-" * 50)

    # Выбираем только числовые столбцы
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        print("  Нет числовых переменных для анализа")
        return None

    print(f"  Числовые переменные: {numeric_cols}")

    results = []
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) > 0 and series.mean() != 0:
            mean = series.mean()
            std = series.std()
            cv = (std / mean) * 100
            range_val = series.max() - series.min()
            iqr = series.quantile(0.75) - series.quantile(0.25)

            results.append({
                'Переменная': col,
                'Среднее': mean,
                'СО': std,
                'CV (%)': cv,
                'Range': range_val,
                'IQR': iqr
            })

    return pd.DataFrame(results)


# Пытаемся загрузить датасеты seaborn
if SEABORN_AVAILABLE:
    try:
        # Загружаем датасет tips
        tips = sns.load_dataset('tips')
        tips_results = analyze_dataset(tips, 'Tips (чаевые)')

        # Загружаем датасет penguins
        penguins = sns.load_dataset('penguins')
        penguins_results = analyze_dataset(penguins, 'Penguins (пингвины)')

    except Exception as e:
        print(f"  Ошибка загрузки датасетов: {e}")
        print("  Создаём демонстрационный датасет...")
        SEABORN_AVAILABLE = False

# Если seaborn не доступен, создаём демонстрационный датасет
if not SEABORN_AVAILABLE:
    print("\n  ⚠️ Seaborn не доступен, создаём демонстрационный датасет")

    # Создаём синтетический датасет, похожий на 'tips'
    np.random.seed(42)
    n = 244

    demo_df = pd.DataFrame({
        'total_bill': np.random.gamma(2, 10, n).round(2).clip(3, 50),
        'tip': np.random.gamma(1.5, 2, n).round(2).clip(0.5, 10),
        'size': np.random.randint(1, 6, n),
        'day_code': np.random.choice([1, 2, 3, 4], n),  # числовой код дня
        'time_code': np.random.choice([0, 1], n)  # числовой код времени
    })

    tips_results = analyze_dataset(demo_df, 'Демо-датасет (аналог Tips)')

# Анализ результатов для tips
print("\n" + "-" * 50)
print("АНАЛИЗ КОЭФФИЦИЕНТОВ ВАРИАЦИИ (CV):")
print("-" * 50)

if 'tips_results' in locals() and tips_results is not None:
    print("\n  📊 Tips датасет:")
    print(tips_results.to_string(index=False))

    # Находим самую стабильную и вариативную переменную
    min_cv_row = tips_results.loc[tips_results['CV (%)'].idxmin()]
    max_cv_row = tips_results.loc[tips_results['CV (%)'].idxmax()]

    print(f"\n  🎯 РЕЗУЛЬТАТЫ:")
    print(f"     Самая СТАБИЛЬНАЯ переменная: {min_cv_row['Переменная']}")
    print(f"       • CV = {min_cv_row['CV (%)']:.1f}%")
    print(f"       • Среднее = {min_cv_row['Среднее']:.2f}")
    print(f"       • СО = {min_cv_row['СО']:.2f}")
    print(f"       • Низкая вариация → данные очень однородны")

    print(f"\n     Самая ВАРИАТИВНАЯ переменная: {max_cv_row['Переменная']}")
    print(f"       • CV = {max_cv_row['CV (%)']:.1f}%")
    print(f"       • Среднее = {max_cv_row['Среднее']:.2f}")
    print(f"       • СО = {max_cv_row['СО']:.2f}")
    print(f"       • Высокая вариация → данные сильно различаются")

# Анализ penguins, если доступен
if SEABORN_AVAILABLE and 'penguins_results' in locals() and penguins_results is not None:
    print("\n" + "-" * 50)
    print("  📊 Penguins датасет:")
    print(penguins_results.to_string(index=False))

    min_cv_row = penguins_results.loc[penguins_results['CV (%)'].idxmin()]
    max_cv_row = penguins_results.loc[penguins_results['CV (%)'].idxmax()]

    print(f"\n  🎯 РЕЗУЛЬТАТЫ:")
    print(f"     Самая СТАБИЛЬНАЯ переменная: {min_cv_row['Переменная']}")
    print(f"       • CV = {min_cv_row['CV (%)']:.1f}%")

    print(f"\n     Самая ВАРИАТИВНАЯ переменная: {max_cv_row['Переменная']}")
    print(f"       • CV = {max_cv_row['CV (%)']:.1f}%")

# ============================================
# ИТОГОВАЯ СВОДНАЯ ТАБЛИЦА
# ============================================

print("\n" + "=" * 70)
print("ИТОГОВАЯ СВОДНАЯ ТАБЛИЦА МЕР РАЗБРОСА")
print("=" * 70)

summary_df = pd.DataFrame({
    'Мера': ['Размах (Range)', 'IQR', 'Дисперсия', 'Станд. отклонение', 'Коэфф. вариации (CV)'],
    'Что показывает': [
        'Полный диапазон данных',
        'Разброс центральных 50%',
        'Средний квадрат отклонений',
        'Типичное отклонение от среднего',
        'Относительный разброс (%)'
    ],
    'Устойчивость к выбросам': [
        'Очень низкая ❌',
        'Высокая ✅',
        'Средняя ⚠️',
        'Средняя ⚠️',
        'Средняя ⚠️'
    ],
    'Когда использовать': [
        'Быстрая оценка границ',
        'Данные с выбросами',
        'Математические расчёты',
        'Интерпретация разброса',
        'Сравнение разных единиц'
    ]
})

print("\n", summary_df.to_string(index=False))

print("\n" + "=" * 70)
print("ВЫВОДЫ ПО РАБОТЕ")
print("=" * 70)

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        КЛЮЧЕВЫЕ ВЫВОДЫ                                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝

1. ВЛИЯНИЕ ВЫБРОСОВ НА МЕРЫ РАЗБРОСА:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Размах (Range) - наиболее чувствителен к выбросам
   • Среднее и дисперсия - умеренно чувствительны
   • Медиана и IQR - устойчивы к выбросам

   В нашем эксперименте удаление 5 выбросов привело к:
   • Снижению среднего на {mean_change:.1f}%
   • Снижению стандартного отклонения на {std_change:.1f}%
   • Незначительному изменению медианы и IQR

2. ВЫБОР ПРАВИЛЬНОЙ МЕРЫ:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Если данные БЕЗ ВЫБРОСОВ → используйте СРЕДНЕЕ и СТАНД. ОТКЛОНЕНИЕ
   • Если данные С ВЫБРОСАМИ → используйте МЕДИАНУ и IQR
   • Для сравнения РАЗНЫХ ЕДИНИЦ → используйте КОЭФФИЦИЕНТ ВАРИАЦИИ
   • Для БЫСТРОЙ ОЦЕНКИ границ → используйте РАЗМАХ

3. КОЭФФИЦИЕНТ ВАРИАЦИИ (CV) - КЛЮЧЕВОЙ ИНСТРУМЕНТ:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Позволяет сравнивать разброс разных переменных
   • Выражается в процентах (без единиц измерения)
   • CV < 10% → очень стабильные данные
   • CV > 30% → высокая вариативность

4. ПРАКТИЧЕСКИЙ АЛГОРИТМ АНАЛИЗА:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ШАГ 1: Визуализируйте данные (гистограмма, ящик с усами)
   ШАГ 2: Проверьте наличие выбросов (метод 1.5×IQR)
   ШАГ 3: Если выбросов нет → используйте среднее и СО
   ШАГ 4: Если выбросы есть → используйте медиану и IQR
   ШАГ 5: Для сравнения переменных → используйте CV
""".format(
    mean_change=mean_change if 'mean_change' in locals() else 0,
    std_change=std_change if 'std_change' in locals() else 0
))

print("=" * 70)
print("✅ ЗАДАНИЕ ВЫПОЛНЕНО УСПЕШНО!")
print("=" * 70)