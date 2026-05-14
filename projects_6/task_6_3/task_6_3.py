import pandas as pd
import numpy as np

# Фиксируем seed для воспроизводимости случайных чисел
np.random.seed(42)

print("="*70)
print("ЗАДАНИЕ 1: Анализ среднего арифметического и влияние выбросов")
print("="*70)

# ============================================
# 1. СОЗДАЁМ DATAFRAME С 8 СТУДЕНТАМИ
# ============================================

print("\n1. ИСХОДНЫЕ ДАННЫЕ (8 студентов)")
print("-" * 50)

# Имена студентов
students = ['Анна', 'Борис', 'Виктория', 'Глеб', 'Дарья', 'Евгений', 'Жанна', 'Захар']

# Генерируем случайные оценки за 4 экзамена (от 40 до 100)
np.random.seed(42)  # для воспроизводимости
grades = np.random.randint(40, 101, size=(8, 4))

# Создаём DataFrame
df = pd.DataFrame(grades, columns=['Math', 'Python', 'Statistics', 'Databases'], index=students)
df.reset_index(inplace=True)
df.rename(columns={'index': 'student'}, inplace=True)

print("\nИсходные данные (8 студентов):")
print(df.to_string(index=False))

# ============================================
# 2. ВЫЧИСЛЯЕМ СРЕДНИЕ (ДО ВЫБРОСОВ)
# ============================================

print("\n" + "="*70)
print("\n2. РАСЧЁТ СРЕДНИХ ЗНАЧЕНИЙ (ДО ДОБАВЛЕНИЯ ВЫБРОСОВ)")
print("-" * 50)

# Средний балл КАЖДОГО студента (по строке)
df['avg_student'] = df[['Math', 'Python', 'Statistics', 'Databases']].mean(axis=1).round(2)

# Средний балл по КАЖДОМУ экзамену (по столбцу)
exam_means_before = df[['Math', 'Python', 'Statistics', 'Databases']].mean().round(2)

print("\nСредний балл КАЖДОГО студента:")
print(df[['student', 'Math', 'Python', 'Statistics', 'Databases', 'avg_student']].to_string(index=False))

print("\nСредний балл по КАЖДОМУ экзамену:")
for exam, mean_val in exam_means_before.items():
    print(f"  {exam}: {mean_val:.2f}")

# Общее среднее до выбросов
total_mean_before = df[['Math', 'Python', 'Statistics', 'Databases']].values.mean()
print(f"\nОбщее среднее по всем экзаменам и студентам: {total_mean_before:.2f}")

# ============================================
# 3. ДОБАВЛЯЕМ СТУДЕНТОВ С ВЫБРОСАМИ
# ============================================

print("\n" + "="*70)
print("\n3. ДОБАВЛЕНИЕ ВЫБРОСОВ (аномальные студенты)")
print("-" * 50)

# Студент с аномально высокими баллами (100 по всем предметам)
high_outlier = pd.DataFrame({
    'student': ['Мэри Сью (высокий выброс)'],
    'Math': [100],
    'Python': [100],
    'Statistics': [100],
    'Databases': [100]
})

# Студент с аномально низкими баллами (20 по всем предметам)
low_outlier = pd.DataFrame({
    'student': ['Ленивый студент (низкий выброс)'],
    'Math': [20],
    'Python': [20],
    'Statistics': [20],
    'Databases': [20]
})

# Добавляем выбросы к исходным данным
df_with_outliers = pd.concat([df, high_outlier, low_outlier], ignore_index=True)

# Удаляем временный столбец avg_student из исходного df, чтобы пересчитать заново
df_with_outliers = df_with_outliers.drop(columns=['avg_student'], errors='ignore')

# Пересчитываем средний балл каждого студента
df_with_outliers['avg_student'] = df_with_outliers[['Math', 'Python', 'Statistics', 'Databases']].mean(axis=1).round(2)

print("\nДанные с добавленными выбросами (всего 10 студентов):")
print(df_with_outliers[['student', 'Math', 'Python', 'Statistics', 'Databases', 'avg_student']].to_string(index=False))

# ============================================
# 4. ПЕРЕСЧИТЫВАЕМ СРЕДНИЕ ПОСЛЕ ДОБАВЛЕНИЯ ВЫБРОСОВ
# ============================================

print("\n" + "="*70)
print("\n4. РАСЧЁТ СРЕДНИХ ЗНАЧЕНИЙ (ПОСЛЕ ДОБАВЛЕНИЯ ВЫБРОСОВ)")
print("-" * 50)

# Средний балл по каждому экзамену (после выбросов)
exam_means_after = df_with_outliers[['Math', 'Python', 'Statistics', 'Databases']].mean().round(2)

print("\nСредний балл по КАЖДОМУ экзамену (с выбросами):")
for exam, mean_val in exam_means_after.items():
    print(f"  {exam}: {mean_val:.2f}")

# Общее среднее после выбросов
total_mean_after = df_with_outliers[['Math', 'Python', 'Statistics', 'Databases']].values.mean()
print(f"\nОбщее среднее по всем экзаменам и студентам (с выбросами): {total_mean_after:.2f}")

# ============================================
# 5. СРАВНИТЕЛЬНЫЙ АНАЛИЗ
# ============================================

print("\n" + "="*70)
print("\n5. СРАВНИТЕЛЬНЫЙ АНАЛИЗ (ВЛИЯНИЕ ВЫБРОСОВ)")
print("-" * 70)

# Создаём таблицу сравнения
comparison = pd.DataFrame({
    'Экзамен': exam_means_before.index,
    'Среднее (до выбросов)': exam_means_before.values,
    'Среднее (после выбросов)': exam_means_after.values,
    'Изменение': (exam_means_after.values - exam_means_before.values).round(2),
    'Изменение (%)': ((exam_means_after.values - exam_means_before.values) / exam_means_before.values * 100).round(1)
})

print("\nТаблица изменения средних баллов по экзаменам:")
print(comparison.to_string(index=False))

print(f"\nИзменение общего среднего:")
print(f"  Общее среднее до выбросов: {total_mean_before:.2f}")
print(f"  Общее среднее после выбросов: {total_mean_after:.2f}")
print(f"  Абсолютное изменение: {(total_mean_after - total_mean_before):.2f}")
print(f"  Относительное изменение: {((total_mean_after - total_mean_before) / total_mean_before * 100):.1f}%")

# ============================================
# 6. НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ ПРОБЛЕМЫ СРЕДНЕГО
# ============================================

print("\n" + "="*70)
print("\n6. НАГЛЯДНАЯ ДЕМОНСТРАЦИЯ ПРОБЛЕМЫ СРЕДНЕГО")
print("-" * 70)

# Показываем на примере одного экзамена (Math)
math_before = df['Math'].mean()
math_after = df_with_outliers['Math'].mean()

print("\nНа примере экзамена по Математике:")
print(f"  Средняя оценка 8 обычных студентов: {math_before:.2f}")
print(f"  Добавили студента со 100 баллами и студента с 20 баллами")
print(f"  Новая средняя оценка 10 студентов: {math_after:.2f}")

print(f"\n  Изменение: {math_after - math_before:+.2f} баллов")

# Показываем медиану как более устойчивую меру
median_before = df['Math'].median()
median_after = df_with_outliers['Math'].median()

print(f"\n  Для сравнения - МЕДИАНА (более устойчивая мера):")
print(f"  Медиана до выбросов: {median_before:.2f}")
print(f"  Медиана после выбросов: {median_after:.2f}")
print(f"  Изменение медианы: {median_after - median_before:+.2f} баллов (гораздо меньше!)")

# ============================================
# 7. ВЫВОДЫ
# ============================================

print("\n" + "="*70)
print("\n7. ВЫВОДЫ ПО РАБОТЕ")
print("-" * 70)

print("""
✅ СРЕДНЕЕ АРИФМЕТИЧЕСКОЕ:
   • Чувствительно к экстремальным значениям (выбросам)
   • Даже два выброса (один высокий, один низкий) могут существенно изменить результат
   • В нашем примере общее среднее изменилось на {:.1f}%

⚠️ КОГДА СРЕДНЕЕ МОЖЕТ ВВОДИТЬ В ЗАБЛУЖДЕНИЕ:
   • При асимметричных распределениях
   • При наличии выбросов
   • В социально-экономических данных (зарплаты, доходы)
   • При оценке типичного представителя группы

💡 ЧТО ИСПОЛЬЗОВАТЬ ВМЕСТО СРЕДНЕГО:
   • Медиану - при наличии выбросов
   • Моду - для категориальных данных
   • Усечённое среднее - для отфильтрованных данных

📊 В НАШЕМ ПРИМЕРЕ:
   • Средняя оценка по математике выросла с {:.1f} до {:.1f} ({:+.1f})
   • Медиана изменилась с {:.1f} до {:.1f} ({:+.1f})
   • Медиана показала себя как более устойчивая мера!
""".format(
    abs((total_mean_after - total_mean_before) / total_mean_before * 100),
    math_before, math_after, (math_after - math_before),
    median_before, median_after, (median_after - median_before)
))

print("="*70)