import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings('ignore')

# Попробуем импортировать seaborn и scipy
try:
    import seaborn as sns

    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("⚠️ Seaborn не установлен. Устанавливаем через: pip install seaborn")

try:
    from scipy import stats

    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    print("⚠️ Scipy не установлен. Устанавливаем через: pip install scipy")

print("=" * 70)
print("ЗАДАНИЕ: Перцентили, квартили и IQR")
print("=" * 70)

# ============================================
# ЗАДАНИЕ 1.1: ПЕРЦЕНТИЛЬНЫЙ РАНГ ОЦЕНКИ
# ============================================

print("\n" + "=" * 70)
print("ЗАДАНИЕ 1: Перцентильный ранг оценки студента")
print("=" * 70)

# Создаём Series из 15 произвольных оценок
np.random.seed(42)
scores = np.random.randint(30, 101, size=15)
scores_series = pd.Series(scores, name='lab_scores')

print("\n📊 Результаты лабораторных работ (15 студентов):")
print(f"Оценки: {scores_series.tolist()}")
print(f"Отсортировано: {sorted(scores_series.tolist())}")

# Задаём свой балл
your_score = 70
print(f"\n🎓 Ваш балл: {your_score}")

# Вычисляем перцентильный ранг
rank = (scores_series < your_score).sum()
percentile_rank_manual = (rank / len(scores_series)) * 100

print(f"\n📈 РАСЧЁТ ПЕРЦЕНТИЛЬНОГО РАНГА:")
print(f"  Студентов с баллом НИЖЕ {your_score}: {rank} из {len(scores_series)}")
print(f"  Перцентильный ранг: {percentile_rank_manual:.1f}-й перцентиль")

# Проверка через scipy (если доступен)
if SCIPY_AVAILABLE:
    pct_rank_scipy = stats.percentileofscore(scores_series, your_score, kind='weak')
    print(f"  Проверка (scipy): {pct_rank_scipy:.1f}-й перцентиль")
    print(f"  Разница: {abs(percentile_rank_manual - pct_rank_scipy):.1f}")

print(f"\n💡 ИНТЕРПРЕТАЦИЯ:")
print(f"  Ваш балл {your_score} выше, чем у {percentile_rank_manual:.0f}% студентов группы.")

# Визуализация позиции в распределении
print("\n📊 Визуализация вашей позиции в группе:")
sorted_scores = sorted(scores_series.tolist())
print("  Шкала баллов: 30" + " " * 40 + "100")
print("  Распределение: ", end="")
for score in sorted_scores:
    if score < your_score:
        print("◯", end="")
    elif score == your_score:
        print("●", end="")
    else:
        print("○", end="")
print()

# ============================================
# ЗАДАНИЕ 1.2: БАЛЛ vs ПЕРЦЕНТИЛЬНЫЙ РАНГ
# ============================================

print("\n" + "=" * 70)
print("ЗАДАНИЕ 1.2: Разница между баллом и перцентильным рангом")
print("=" * 70)

print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║  ВОПРОС: Если перцентильный ранг равен 80 — это значит, что вы получили 80   ║
║          баллов?                                                             ║
╚═══════════════════════════════════════════════════════════════════════════════╝

ОТВЕТ: НЕТ, ЭТО НЕ ОДНО И ТО ЖЕ!

┌─────────────────────────────────────────────────────────────────────────────┐
│  БАЛЛ (абсолютное значение)                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Это конкретная числовая оценка (например, 82 балла из 100)              │
│  • Показывает, КАК ВЫ ВЫПОЛНИЛИ работу                                      │
│  • Не зависит от других студентов                                           │
│  • Шкала фиксирована (0-100)                                                │
│  • Пример: "Я получил 82 балла"                                             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│  ПЕРЦЕНТИЛЬНЫЙ РАНГ (относительная позиция)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Это процент людей, которых вы ОБОШЛИ                                      │
│  • Показывает, КАК ВЫ ВЫГЛЯДИТЕ НА ФОНЕ ДРУГИХ                              │
│  • Зависит от всех остальных                                                │
│  • Шкала всегда от 0 до 100                                                 │
│  • Пример: "Я обошёл 80% участников"                                        │
└─────────────────────────────────────────────────────────────────────────────┘

НАГЛЯДНЫЙ ПРИМЕР:

  Сценарий 1 (лёгкий экзамен):
    • Ваш балл: 80
    • Все остальные написали на 90+
    • Ваш перцентиль: 20 (вы обошли только 20%)

  Сценарий 2 (сложный экзамен):
    • Ваш балл: 80  
    • Все остальные написали на 50+
    • Ваш перцентиль: 90 (вы обошли 90%)

  ВЫВОД: ОДИНАКОВЫЙ БАЛЛ может давать РАЗНЫЙ перцентильный ранг!
         И наоборот: одинаковый перцентиль может быть при разных баллах.

📌 ГЛАВНОЕ ОТЛИЧИЕ:
  • Балл — АБСОЛЮТНАЯ характеристика (сколько знаний/умений)
  • Перцентиль — ОТНОСИТЕЛЬНАЯ характеристика (место в группе)
""")

# ============================================
# ЗАДАНИЕ 2.1: ПЕРЦЕНТИЛИ ДЛИНЫ КРЫЛА ПИНГВИНОВ
# ============================================

print("\n" + "=" * 70)
print("ЗАДАНИЕ 2.1: Анализ длины крыла пингвинов")
print("=" * 70)

# Загружаем датасет penguins или создаём аналог
if SEABORN_AVAILABLE:
    try:
        penguins = sns.load_dataset('penguins')
        print("\n✅ Датасет 'penguins' успешно загружен!")
    except Exception as e:
        print(f"\n⚠️ Ошибка загрузки: {e}")
        print("   Создаём демонстрационный датасет...")
        SEABORN_AVAILABLE = False

if not SEABORN_AVAILABLE:
    # Создаём синтетический датасет пингвинов
    np.random.seed(42)
    n = 344
    penguins = pd.DataFrame({
        'species': np.random.choice(['Adelie', 'Chinstrap', 'Gentoo'], n, p=[0.44, 0.32, 0.24]),
        'flipper_length_mm': np.concatenate([
            np.random.normal(190, 6, 150),
            np.random.normal(196, 7, 110),
            np.random.normal(217, 8, 84)
        ]).round(1).clip(170, 240)
    })
    print("\n📊 Создан демонстрационный датасет пингвинов")

# Берём столбец flipper_length_mm, удаляем пропуски
flipper_length = penguins['flipper_length_mm'].dropna()
print(f"\n📏 Анализ длины крыла пингвинов (flipper_length_mm)")
print(f"   Количество наблюдений: {len(flipper_length)}")
print(f"   Диапазон: от {flipper_length.min():.1f} до {flipper_length.max():.1f} мм")

# Вычисляем перцентили
percentiles_needed = [0.10, 0.25, 0.50, 0.75, 0.90]
percentile_values = flipper_length.quantile(percentiles_needed)

print("\n" + "-" * 50)
print("РЕЗУЛЬТАТЫ РАСЧЁТА ПЕРЦЕНТИЛЕЙ:")
print("-" * 50)

# Создаём таблицу с описанием
results_2_1 = []
for p in percentiles_needed:
    p_int = int(p * 100)
    value = percentile_values[p]

    if p == 0.10:
        desc = f"P{p_int} — нижние 10% (самые короткие крылья)"
    elif p == 0.25:
        desc = f"Q1 (P{p_int}) — первый квартиль"
    elif p == 0.50:
        desc = f"Q2 (P{p_int}) — медиана"
    elif p == 0.75:
        desc = f"Q3 (P{p_int}) — третий квартиль"
    elif p == 0.90:
        desc = f"P{p_int} — верхние 10% (самые длинные крылья)"
    else:
        desc = f"{p_int}-й перцентиль"

    results_2_1.append({
        'Перцентиль': f'P{p_int}',
        'Значение (мм)': f'{value:.1f}',
        'Описание': desc
    })

result_df_2_1 = pd.DataFrame(results_2_1)
print("\n", result_df_2_1.to_string(index=False))

print(f"\n💡 ЧТО ОЗНАЧАЕТ P10 (10-й перцентиль)?")
print(f"   P10 = {percentile_values[0.10]:.1f} мм")
print(f"   Это значит, что 10% пингвинов имеют длину крыла МЕНЬШЕ {percentile_values[0.10]:.1f} мм")
print(f"   И 90% пингвинов имеют длину крыла БОЛЬШЕ этого значения.")
print(f"\n   Другими словами: {percentile_values[0.10]:.1f} мм — это граница")
print(f"   между 10% самых 'короткокрылых' и остальными 90% пингвинов.")

# Визуализация
print("\n📊 Распределение длины крыла с отмеченными перцентилями:")


def create_percentile_chart(data, percentiles_dict, width=50):
    min_val = data.min()
    max_val = data.max()
    line = []
    for i in range(width + 1):
        pos = min_val + (max_val - min_val) * i / width
        line_char = "─"
        for p_name, p_val in percentiles_dict.items():
            if abs(pos - p_val) < (max_val - min_val) / width / 2:
                line_char = "●"
                break
        line.append(line_char)

    print("  " + "".join(line))
    print(f"  {min_val:.0f}" + " " * (width - 4) + f"{max_val:.0f}")


percentiles_dict = {
    'P10': percentile_values[0.10],
    'Q1': percentile_values[0.25],
    'Median': percentile_values[0.50],
    'Q3': percentile_values[0.75],
    'P90': percentile_values[0.90]
}
create_percentile_chart(flipper_length, percentiles_dict)
print("  " + " " * 8 + "●" + " " * 2 + "●" + " " * 10 + "●" + " " * 10 + "●" + " " * 8 + "●")
print("  " + " " * 4 + "P10" + " " * 3 + "Q1" + " " * 10 + "Med" + " " * 9 + "Q3" + " " * 6 + "P90")

# ============================================
# ЗАДАНИЕ 2.2: ПЕРЦЕНТИЛЬНЫЙ РАНГ ПИНГВИНА ADELIE
# ============================================

print("\n" + "=" * 70)
print("ЗАДАНИЕ 2.2: Перцентильный ранг пингвина Adelie")
print("=" * 70)

# Пингвин Adelie с длиной крыла 190 мм
target_flipper = 190
adelie_flipper = 190

print(f"\�" + "🐧 Пингвин вида Adelie с длиной крыла: {adelie_flipper} мм")

# Ручной расчёт перцентильного ранга
rank_adelie = (flipper_length < adelie_flipper).sum()
pct_rank_adelie_manual = (rank_adelie / len(flipper_length)) * 100

print(f"\n📊 РУЧНОЙ РАСЧЁТ:")
print(f"  Пингвинов с длиной крыла МЕНЬШЕ {adelie_flipper} мм: {rank_adelie} из {len(flipper_length)}")
print(f"  Перцентильный ранг: {pct_rank_adelie_manual:.1f}-й перцентиль")

# Расчёт через scipy (если доступен)
if SCIPY_AVAILABLE:
    pct_rank_adelie_scipy = stats.percentileofscore(flipper_length, adelie_flipper, kind='weak')
    print(f"\n📊 РАСЧЁТ ЧЕРЕЗ SCIPY:")
    print(f"  Перцентильный ранг: {pct_rank_adelie_scipy:.1f}-й перцентиль")
    print(f"  Разница с ручным расчётом: {abs(pct_rank_adelie_manual - pct_rank_adelie_scipy):.1f}")

    # Другой метод (strict)
    pct_rank_adelie_strict = stats.percentileofscore(flipper_length, adelie_flipper, kind='strict')
    print(f"  Перцентильный ранг (strict): {pct_rank_adelie_strict:.1f}-й перцентиль")

print(f"\n💡 ИНТЕРПРЕТАЦИЯ:")
print(f"  Пингвин Adelie с длиной крыла {adelie_flipper} мм находится на")
print(f"  {pct_rank_adelie_manual:.0f}-м перцентиле среди всех пингвинов.")
print(f"  Это значит, что он имеет БОЛЕЕ ДЛИННЫЕ крылья, чем {pct_rank_adelie_manual:.0f}% пингвинов,")
print(f"  и БОЛЕЕ КОРОТКИЕ, чем {100 - pct_rank_adelie_manual:.0f}% пингвинов.")

# Дополнительно: где находится конкретный пингвин
print(f"\n📊 Визуализация позиции пингвина Adelie:")
all_flippers = sorted(flipper_length.tolist())
print("  Длина крыла (мм): ", end="")
for i, flipper in enumerate(all_flippers):
    if flipper < adelie_flipper:
        print("◯", end="")
    elif flipper == adelie_flipper and i == all_flippers.index(adelie_flipper):
        print("🐧", end="")
    else:
        print("○", end="")
print()

# ============================================
# ЗАДАНИЕ 2.3: ПОРОГ ПРИЁМА
# ============================================

print("\n" + "=" * 70)
print("ЗАДАНИЕ 2.3: Реальный сценарий - вступительный экзамен")
print("=" * 70)

# Создаём результаты 50 студентов
np.random.seed(123)
exam_scores = pd.Series(np.random.randint(40, 101, size=50), name='exam_scores')

print(f"\n📊 Результаты вступительного экзамена (50 абитуриентов):")
print(f"  Средний балл: {exam_scores.mean():.1f}")
print(f"  Медиана: {exam_scores.median():.1f}")
print(f"  Минимум: {exam_scores.min()}")
print(f"  Максимум: {exam_scores.max()}")

# Балл студента
student_score = 82
print(f"\n🎓 Студент получил: {student_score} баллов")

# Вычисляем перцентильный ранг
rank_student = (exam_scores < student_score).sum()
percentile_rank_student = (rank_student / len(exam_scores)) * 100

print(f"\n📈 ПЕРЦЕНТИЛЬНЫЙ РАНГ:")
print(f"  Абитуриентов с баллом НИЖЕ {student_score}: {rank_student} из {len(exam_scores)}")
print(f"  Перцентильный ранг: {percentile_rank_student:.1f}-й перцентиль")

# Порог приёма: верхние 30% (P70)
p70_threshold = exam_scores.quantile(0.70)
print(f"\n🎯 УСЛОВИЯ ПОСТУПЛЕНИЯ:")
print(f"  Порог приёма: верхние 30% абитуриентов (P70)")
print(f"  P70 = {p70_threshold:.1f} баллов")

# Проверяем, прошёл ли студент
if student_score >= p70_threshold:
    print(f"\n✅ РЕЗУЛЬТАТ: СТУДЕНТ ПРОШЁЛ!")
    print(f"   {student_score} баллов >= {p70_threshold:.1f} (P70)")
    print(f"   Студент находится на {percentile_rank_student:.0f}-м перцентиле,")
    print(f"   что выше порогового 70-го перцентиля.")
else:
    print(f"\n❌ РЕЗУЛЬТАТ: СТУДЕНТ НЕ ПРОШЁЛ")
    print(f"   {student_score} баллов < {p70_threshold:.1f} (P70)")
    print(f"   Студент находится на {percentile_rank_student:.0f}-м перцентиле,")
    print(f"   что ниже требуемого 70-го перцентиля.")

# Дополнительный анализ: распределение баллов
print("\n📊 Распределение баллов абитуриентов:")
sorted_scores = sorted(exam_scores.tolist())
print("  Баллы:   ", end="")
for score in sorted_scores:
    if score < p70_threshold:
        print("◯", end="")
    else:
        print("●", end="")
print()
print("           " + " " * (int(len(sorted_scores) * 0.7)) + "↑")
print("           " + " " * (int(len(sorted_scores) * 0.7)) + "P70")

# Сводная статистика по перцентилям
print("\n📊 КЛЮЧЕВЫЕ ПЕРЦЕНТИЛИ:")
key_percentiles = [0.10, 0.25, 0.50, 0.70, 0.75, 0.90, 0.95]
pct_values = exam_scores.quantile(key_percentiles)

for p in key_percentiles:
    if p == 0.70:
        print(f"  P70 (порог):      {pct_values[p]:.1f} баллов")
    else:
        print(f"  P{int(p * 100):2d}:                {pct_values[p]:.1f} баллов")

# ============================================
# ИТОГОВАЯ ТАБЛИЦА ПО ЗАДАНИЮ 2.1
# ============================================

print("\n" + "=" * 70)
print("ИТОГОВАЯ ТАБЛИЦА ПО ЗАДАНИЮ 2.1")
print("=" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ПОЗИЦИОННЫЕ ХАРАКТЕРИСТИКИ                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  КВАРТИЛИ (делят данные на 4 части):                                        │
│  • Q1 (25-й перцентиль) — граница первой четверти                          │
│  • Q2 (50-й перцентиль) — медиана                                          │
│  • Q3 (75-й перцентиль) — граница третьей четверти                         │
│                                                                             │
│  IQR (Interquartile Range) = Q3 - Q1                                        │
│  • Показывает разброс центральных 50% данных                                │
│  • Устойчив к выбросам                                                     │
│                                                                             │
│  ПРАВИЛО ОБНАРУЖЕНИЯ ВЫБРОСОВ (1.5×IQR):                                    │
│  • Нижняя граница: Q1 - 1.5×IQR                                            │
│  • Верхняя граница: Q3 + 1.5×IQR                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

📊 РАСЧЁТЫ ДЛЯ ДЛИНЫ КРЫЛА ПИНГВИНОВ:

   Q1 (25-й перцентиль):  {q1:.1f} мм
   Q3 (75-й перцентиль):  {q3:.1f} мм
   IQR:                   {iqr:.1f} мм
   Медиана (Q2):          {med:.1f} мм

   Верхняя граница для выбросов: {upper:.1f} мм
""".format(
    q1=percentile_values[0.25],
    q3=percentile_values[0.75],
    iqr=percentile_values[0.75] - percentile_values[0.25],
    med=percentile_values[0.50],
    upper=percentile_values[0.75] + 1.5 * (percentile_values[0.75] - percentile_values[0.25])
))

print("=" * 70)
print("✅ ВСЕ ЗАДАНИЯ ВЫПОЛНЕНЫ УСПЕШНО!")
print("=" * 70)