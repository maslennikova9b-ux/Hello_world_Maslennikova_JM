import pandas as pd
import numpy as np
import statistics
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("ЗАДАНИЕ 1: Анализ моды (Mode) как меры центральной тенденции")
print("="*70)

# ============================================
# ЗАДАНИЕ 1.1: БРОСКИ КУБИКА
# ============================================

print("\n" + "="*70)
print("ЧАСТЬ 1: Анализ результатов бросков кубика")
print("="*70)

# Генерируем 20 бросков кубика (значения от 1 до 6)
np.random.seed(42)  # для воспроизводимости
dice_rolls = np.random.randint(1, 7, size=20)

print("\nРезультаты 20 бросков кубика:")
print(f"Броски: {dice_rolls.tolist()}")
print(f"Отсортировано: {sorted(dice_rolls)}")

# Подсчитываем частоту каждого значения
unique, counts = np.unique(dice_rolls, return_counts=True)
frequency = dict(zip(unique, counts))

print("\nЧастота выпадения каждого значения:")
for value in range(1, 7):
    freq = frequency.get(value, 0)
    bar = '█' * freq
    print(f"  {value}: {freq} раз(а) {bar}")

# Находим моду
# Способ 1: через pandas
dice_series = pd.Series(dice_rolls)
modes_pandas = dice_series.mode().tolist()

# Способ 2: через statistics
modes_stats = statistics.multimode(dice_rolls)

print(f"\nРезультаты поиска моды:")
print(f"  Мода (pandas): {modes_pandas}")
print(f"  Мода (statistics): {modes_stats}")
print(f"  Количество мод: {len(modes_pandas)}")

# Анализ модальности
max_freq = max(counts) if len(counts) > 0 else 0
modes_count = sum(1 for v in counts if v == max_freq)

if modes_count == 1:
    print(f"\n📊 Тип распределения: УНИМОДАЛЬНОЕ")
    print(f"   Одно значение ({modes_pandas[0]}) выпадает чаще всего ({max_freq} раз)")
elif modes_count == 2:
    print(f"\n📊 Тип распределения: БИМОДАЛЬНОЕ")
    print(f"   Два значения ({modes_pandas[0]} и {modes_pandas[1]}) выпадают одинаково часто ({max_freq} раз)")
elif modes_count > 2:
    print(f"\n📊 Тип распределения: МУЛЬТИМОДАЛЬНОЕ")
    print(f"   {modes_count} значения выпадают одинаково часто ({max_freq} раз)")
else:
    print(f"\n📊 Тип распределения: БЕЗ МОДЫ (все значения уникальны)")

# Дополнительный анализ: почему такая модальность?
print(f"\n💡 ПОЧЕМУ ТАКОЙ РЕЗУЛЬТАТ?")
print(f"   • Кубик имеет 6 равновероятных исходов (теоретически 1/6 ≈ 16.7%)")
print(f"   • При 20 бросках ожидаемая частота каждого значения: 20/6 ≈ 3.33")
print(f"   • Из-за случайности реальные частоты отличаются от ожидаемых")
print(f"   • Максимальная частота в данном эксперименте: {max_freq} раза")
print(f"   • Количество мод: {modes_count}")

# ============================================
# ЗАДАНИЕ 1.2: ЛЮБИМЫЙ ЯЗЫК ПРОГРАММИРОВАНИЯ
# ============================================

print("\n" + "="*70)
print("ЧАСТЬ 2: Анализ любимых языков программирования студентов")
print("="*70)

# Создаём данные о 15 студентах
np.random.seed(123)
languages = ['Python', 'Java', 'C++', 'JavaScript', 'Python', 'Python',
             'Java', 'Python', 'JavaScript', 'C++', 'Python', 'Java',
             'Python', 'Go', 'Rust']  # Go и Rust - редкие языки

# Перемешиваем для случайности
np.random.shuffle(languages)

students_df = pd.DataFrame({
    'student_id': range(1, 16),
    'favorite_language': languages
})

print("\nДанные о студентах:")
print(students_df.to_string(index=False))

# Находим моду
mode_languages = students_df['favorite_language'].mode().tolist()
value_counts = students_df['favorite_language'].value_counts()

print(f"\nЧастота выбора языков:")
for lang, count in value_counts.items():
    bar = '█' * count
    print(f"  {lang:<12}: {count} студент(ов) {bar}")

print(f"\nРезультаты:")
print(f"  Мода (самый популярный язык): {mode_languages}")
print(f"  Количество мод: {len(mode_languages)}")

if len(mode_languages) == 1:
    print(f"  Самый популярный язык: {mode_languages[0]} ({value_counts[mode_languages[0]]} студентов)")
else:
    print(f"  Самые популярные языки: {', '.join(mode_languages)}")
    for lang in mode_languages:
        print(f"    • {lang}: {value_counts[lang]} студентов")

# Вопрос: можно ли вычислить среднее?
print("\n" + "="*50)
print("❓ МОЖНО ЛИ ВЫЧИСЛИТЬ СРЕДНЕЕ ДЛЯ ЭТИХ ДАННЫХ?")
print("="*50)

print("""
Ответ: НЕТ, НЕЛЬЗЯ ❌

Почему?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Языки программирования - это НОМИНАЛЬНЫЕ (категориальные) данные
2. Номинальные данные не имеют числового значения и порядка
3. Нельзя сложить "Python" + "Java" или разделить на количество
4. Арифметические операции над категориями не имеют смысла

Какие меры можно вычислить?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ МОДА - можно (самый популярный язык)
✅ ЧАСТОТЫ - можно (сколько человек выбрали каждый язык)
✅ ПРОЦЕНТЫ/ДОЛИ - можно

❌ СРЕДНЕЕ - нельзя
❌ МЕДИАНА - нельзя (нет порядка для упорядочивания)

💡 Важно: Для номинальных данных мода - единственная 
   мера центральной тенденции, которая имеет смысл!
""")

# ============================================
# ЗАДАНИЕ 1.3: РЕАЛЬНЫЙ ДАТАСЕТ
# ============================================

print("\n" + "="*70)
print("ЧАСТЬ 3: Анализ реального датасета (Seaborn - Tips)")
print("="*70)

# Загружаем встроенный датасет tips из seaborn
try:
    import seaborn as sns
    tips = sns.load_dataset('tips')
    print("\n✅ Датасет 'tips' (чаевые в ресторане) успешно загружен!")
except ImportError:
    print("\n⚠️ Seaborn не установлен. Устанавливаем через pip...")
    print("   (или создаём демонстрационный датасет)")
    # Создаём аналогичный датасет вручную
    np.random.seed(42)
    n = 244
    tips = pd.DataFrame({
        'total_bill': np.random.gamma(2, 10, n).round(2),
        'tip': np.random.gamma(1.5, 2, n).round(2),
        'sex': np.random.choice(['Male', 'Female'], n, p=[0.6, 0.4]),
        'smoker': np.random.choice(['Yes', 'No'], n, p=[0.3, 0.7]),
        'day': np.random.choice(['Thur', 'Fri', 'Sat', 'Sun'], n, p=[0.3, 0.1, 0.4, 0.2]),
        'time': np.random.choice(['Lunch', 'Dinner'], n, p=[0.4, 0.6]),
        'size': np.random.randint(1, 7, n)
    })
    tips['total_bill'] = tips['total_bill'].clip(3, 50)
    tips['tip'] = tips['tip'].clip(0.5, 10)

print(f"\nДатасет содержит {len(tips)} записей и {len(tips.columns)} столбцов")
print(f"Столбцы: {tips.columns.tolist()}")
print(f"\nПервые 5 записей:")
print(tips.head())

# Выбираем 3 переменные разных типов
# Переменная 1: total_bill (количественная, непрерывная)
# Переменная 2: day (номинальная)
# Переменная 3: size (количественная, дискретная)

print("\n" + "="*70)
print("АНАЛИЗ ТРЁХ ПЕРЕМЕННЫХ")
print("="*70)

# ========== ПЕРЕМЕННАЯ 1: total_bill ==========
print("\n" + "─"*70)
print("📊 ПЕРЕМЕННАЯ 1: total_bill (Сумма счёта)")
print("─"*70)

bill = tips['total_bill']
print(f"\nТип данных: {bill.dtype} - КОЛИЧЕСТВЕННАЯ НЕПРЕРЫВНАЯ")

# Вычисляем меры
bill_mean = bill.mean()
bill_median = bill.median()
bill_mode = bill.mode().tolist()

print(f"\nМеры центральной тенденции:")
print(f"  • Среднее:  {bill_mean:.2f} $")
print(f"  • Медиана:  {bill_median:.2f} $")
print(f"  • Мода:     {bill_mode[:5]}... (первые 5 значений из {len(bill_mode)})")

# Анализ
print(f"\n📌 ВЫВОД ПО ПЕРЕМЕННОЙ:")
if len(bill_mode) > 10:
    print(f"  • Много мод ({len(bill_mode)}) - характерно для непрерывных данных")
print(f"  • Среднее ({bill_mean:.2f}) {'>' if bill_mean > bill_median else '<'} медианы ({bill_median:.2f})")
if abs(bill_mean - bill_median) > 5:
    print(f"  • Распределение скошено вправо (есть большие счета)")
else:
    print(f"  • Распределение близко к симметричному")
print(f"  • Лучший показатель: {'МЕДИАНА' if abs(bill_mean - bill_median) > 3 else 'СРЕДНЕЕ'}")
print(f"    (медиана устойчива к выбросам)")

# ========== ПЕРЕМЕННАЯ 2: day ==========
print("\n" + "─"*70)
print("📊 ПЕРЕМЕННАЯ 2: day (День недели)")
print("─"*70)

day = tips['day']
print(f"\nТип данных: {day.dtype} - НОМИНАЛЬНАЯ (категориальная)")

# Вычисляем моду
day_mode = day.mode().tolist()
day_counts = day.value_counts()

print(f"\nРаспределение по дням:")
for d, count in day_counts.items():
    bar = '█' * (count // 5)
    print(f"  {d}: {count:3d} посещений {bar}")

print(f"\nМеры центральной тенденции:")
print(f"  • Мода:     {day_mode} (самый популярный день)")
print(f"  • Среднее:  НЕПРИМЕНИМО ❌ (номинальные данные)")
print(f"  • Медиана:  НЕПРИМЕНИМО ❌ (нет порядка)")

print(f"\n📌 ВЫВОД ПО ПЕРЕМЕННОЙ:")
print(f"  • Больше всего посетителей в {day_mode[0]}")
print(f"  • Доля {day_mode[0]}: {day_counts[day_mode[0]]/len(day)*100:.1f}% от всех посещений")
print(f"  • Мода - единственная подходящая мера для этого типа данных")

# ========== ПЕРЕМЕННАЯ 3: size ==========
print("\n" + "─"*70)
print("📊 ПЕРЕМЕННАЯ 3: size (Размер компании/количество человек)")
print("─"*70)

size = tips['size']
print(f"\nТип данных: {size.dtype} - КОЛИЧЕСТВЕННАЯ ДИСКРЕТНАЯ")

# Вычисляем меры
size_mean = size.mean()
size_median = size.median()
size_mode = size.mode().tolist()
size_counts = size.value_counts().sort_index()

print(f"\nРаспределение по размеру компании:")
for s in sorted(size_counts.index):
    count = size_counts[s]
    bar = '█' * (count // 5)
    print(f"  {s} чел.: {count:3d} компаний {bar}")

print(f"\nМеры центральной тенденции:")
print(f"  • Среднее:  {size_mean:.2f} чел.")
print(f"  • Медиана:  {size_median:.0f} чел.")
print(f"  • Мода:     {size_mode} (встречается {size_counts[size_mode[0]]} раз)")

print(f"\n📌 ВЫВОД ПО ПЕРЕМЕННОЙ:")
print(f"  • Чаще всего приходят компаниями из {size_mode[0]} человек")
if len(size_mode) > 1:
    print(f"  • БИМОДАЛЬНОЕ распределение: {size_mode[0]} и {size_mode[1]} человека")
print(f"  • Средний размер компании: {size_mean:.1f} человек")
print(f"  • Медианный размер: {size_median:.0f} человек")
print(f"  • Мода показывает самый распространённый сценарий")
print(f"  • Для планирования посадки важна именно МОДА (самый частый размер)")

# ============================================
# ИТОГОВОЕ СРАВНЕНИЕ
# ============================================

print("\n" + "="*70)
print("ИТОГОВАЯ ТАБЛИЦА СРАВНЕНИЯ ТРЁХ ПЕРЕМЕННЫХ")
print("="*70)

comparison_df = pd.DataFrame({
    'Переменная': ['total_bill', 'day', 'size'],
    'Тип данных': ['Количественный\n(непрерывный)', 'Номинальный\n(категория)', 'Количественный\n(дискретный)'],
    'Среднее': [f'{bill_mean:.2f}', '❌ Неприменимо', f'{size_mean:.2f}'],
    'Медиана': [f'{bill_median:.2f}', '❌ Неприменимо', f'{size_median:.0f}'],
    'Мода': [f'{len(bill_mode)} значений', f'{day_mode[0]}', f'{size_mode}'],
    'Лучшая мера': ['Медиана', 'Мода', 'Мода']
})

print("\n", comparison_df.to_string(index=False))

# Финальные выводы
print("\n" + "="*70)
print("ОСНОВНЫЕ ВЫВОДЫ ПО РАБОТЕ")
print("="*70)

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 ЧТО ТАКОЕ МОДА?
   • Значение, которое встречается наиболее часто
   • Единственная мера центральной тенденции для НОМИНАЛЬНЫХ данных
   • Может быть несколько мод (бимодальные/мультимодальные распределения)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 КОГДА ИСПОЛЬЗОВАТЬ МОДУ?
   ✅ Для категориальных данных (цвет, город, язык программирования)
   ✅ Чтобы найти самое популярное значение
   ✅ Для дискретных данных с повторяющимися значениями
   ✅ В маркетинге: самый популярный товар
   ✅ В социологии: самый частый ответ

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ ОГРАНИЧЕНИЯ МОДЫ:
   • Для непрерывных данных часто неинформативна (все значения уникальны)
   • Не учитывает все данные, только самые частые значения
   • Может быть неустойчивой при малых выборках

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 СРАВНЕНИЕ МЕР ЦЕНТРАЛЬНОЙ ТЕНДЕНЦИИ:

   Характеристика     | Среднее | Медиана | Мода
   -------------------|---------|---------|--------
   Для каких данных?  | Количес | Колич+  | ЛЮБЫЕ
                      | твенные | Порядк  | 
   Устойчивость к     | НЕТ ❌  | ДА ✅   | ДА ✅
   выбросам           |         |         |
   Всегда ли одна?    | ДА      | ДА      | НЕТ
   Смысл              | Баланс  | Середина| Самое частое
""")

print("="*70)
print("✅ ЗАДАНИЕ ВЫПОЛНЕНО ПОЛНОСТЬЮ!")
print("="*70)