"""
Задание 7: Визуализация данных учебной базы данных
Анализ успеваемости студентов, популярности курсов и распределения оценок
"""

import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Patch
import numpy as np

# ============================================
# БЛОК 1: ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ (С ИСПРАВЛЕНИЕМ КОДИРОВКИ)
# ============================================

print("=" * 70)
print("АНАЛИЗ УЧЕБНОЙ БАЗЫ ДАННЫХ - ВИЗУАЛИЗАЦИЯ")
print("=" * 70)

# Параметры подключения (ПРОВЕРЬТЕ СВОИ!)
DB_CONFIG = {
    "host": "localhost",
    "port": "5432",
    "user": "postgres",
    "password": "example",
    "database": "testdb"
}

try:
    # Добавляем параметры для решения проблемы кодировки
    connection = psycopg2.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
        client_encoding='UTF8'  # Явно указываем кодировку
    )
    print("\n✓ Подключение к базе данных установлено")

except Exception as error:
    print(f"\n❌ Ошибка подключения: {error}")
    print("\nВозможные причины:")
    print("  1. Контейнер PostgreSQL не запущен")
    print("  2. Неправильные параметры подключения (проверьте host, port, user, password, database)")
    print("  3. Проблема с кодировкой в базе данных")
    print("\nПроверьте параметры подключения и запустите контейнер:")
    print("  docker start <название_контейнера>")
    raise SystemExit

# ============================================
# БЛОК 2: ИЗВЛЕЧЕНИЕ ДАННЫХ
# ============================================

print("\n" + "=" * 70)
print("ИЗВЛЕЧЕНИЕ ДАННЫХ")
print("=" * 70)

try:
    # Запрос 1: Средний балл по курсам
    df_courses = pd.read_sql("""
        SELECT
            c.course_name AS course,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
            COUNT(e.enrollment_id) AS total_enrollments,
            MIN(e.grade) AS min_grade,
            MAX(e.grade) AS max_grade
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        GROUP BY c.course_name
        ORDER BY avg_grade DESC
    """, connection)

    # Запрос 2: Все оценки (для распределения)
    df_all_grades = pd.read_sql("SELECT grade FROM enrollments", connection)

    # Запрос 3: Студенты по году поступления
    df_years = pd.read_sql("""
        SELECT
            enrollment_year AS year,
            COUNT(student_id) AS students
        FROM students
        GROUP BY enrollment_year
        ORDER BY enrollment_year
    """, connection)

    # Запрос 4: Студенты без оценок (аномалии)
    df_missing = pd.read_sql("""
        SELECT
            s.first_name || ' ' || s.last_name AS student,
            s.enrollment_year
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        WHERE e.enrollment_id IS NULL
        ORDER BY s.enrollment_year, s.last_name
    """, connection)

    # Запрос 5: Успеваемость по годам поступления
    df_yearly_performance = pd.read_sql("""
        SELECT
            s.enrollment_year,
            ROUND(AVG(e.grade)::numeric, 2) AS avg_grade,
            COUNT(DISTINCT s.student_id) AS students_count,
            COUNT(e.enrollment_id) AS exams_count
        FROM students s
        LEFT JOIN enrollments e ON s.student_id = e.student_id
        GROUP BY s.enrollment_year
        ORDER BY s.enrollment_year
    """, connection)

    print(f"\n✓ Загружено {len(df_courses)} курсов")
    print(f"✓ Загружено {len(df_all_grades)} записей об оценках")
    print(f"✓ Загружено {len(df_years)} годов поступления")
    print(f"✓ Выявлено {len(df_missing)} студентов без оценок")

except Exception as error:
    print(f"\n❌ Ошибка при выполнении запроса: {error}")
    connection.close()
    raise SystemExit

finally:
    connection.close()
    print("\n✓ Соединение закрыто")

# ============================================
# БЛОК 3: ПОДГОТОВКА ДАННЫХ ДЛЯ ВИЗУАЛИЗАЦИИ
# ============================================

print("\n" + "=" * 70)
print("ПОДГОТОВКА ДАННЫХ ДЛЯ ВИЗУАЛИЗАЦИИ")
print("=" * 70)

# Сокращённые названия курсов
NAME_MAP = {
    "Основы программирования на Python": "Python",
    "Алгоритмы и структуры данных": "Алгоритмы",
    "Базы данных и SQL": "SQL",
    "Веб-разработка (Frontend)": "Frontend",
    "Администрирование Linux": "Linux",
    "Математический анализ": "Матанализ",
    "Дискретная математика": "Дискр. мат.",
    "Английский язык для IT": "Английский",
}
df_courses["short_name"] = df_courses["course"].map(NAME_MAP)

# Статистические метрики
overall_mean = df_all_grades['grade'].mean()
overall_median = df_all_grades['grade'].median()
overall_std = df_all_grades['grade'].std()

print(f"\n📊 ОСНОВНЫЕ СТАТИСТИЧЕСКИЕ МЕТРИКИ ПО ВСЕМ ОЦЕНКАМ:")
print(f"   • Среднее значение: {overall_mean:.2f}")
print(f"   • Медиана: {overall_median:.2f}")
print(f"   • Стандартное отклонение: {overall_std:.2f}")
print(f"   • Минимум: {df_all_grades['grade'].min()}")
print(f"   • Максимум: {df_all_grades['grade'].max()}")

# Проверка на пустые данные
if df_courses.empty:
    print("\n⚠️ ВНИМАНИЕ: Нет данных о курсах! Возможно, таблицы пусты.")
    print("   Запустите скрипт для заполнения базы данных перед выполнением этого задания.")
    exit(0)

# ============================================
# БЛОК 4: ПОСТРОЕНИЕ ГРАФИКОВ
# ============================================

print("\n" + "=" * 70)
print("ПОСТРОЕНИЕ ГРАФИКОВ")
print("=" * 70)

# Настройка стилей
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

# Создаём фигуру с сеткой 2×2
fig = plt.figure(figsize=(16, 12))
fig.suptitle("Анализ успеваемости студентов\nСтатистика по курсам и оценкам",
             fontsize=16, fontweight="bold")

gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

ax1 = fig.add_subplot(gs[0, 0])  # Средний балл по курсам
ax2 = fig.add_subplot(gs[0, 1])  # Количество сдач по курсам
ax3 = fig.add_subplot(gs[1, 0])  # Распределение оценок (гистограмма)
ax4 = fig.add_subplot(gs[1, 1])  # Успеваемость по годам

# ============================================
# ГРАФИК 1: СРЕДНИЙ БАЛЛ ПО КУРСАМ
# ============================================

print("\n📊 График 1: Средний балл по курсам (столбчатая диаграмма)")

# Выбираем цвета: красный для курсов ниже среднего
bar_colors = ['#d9534f' if g < overall_mean else '#4a90d9'
              for g in df_courses['avg_grade']]

bars1 = ax1.bar(df_courses['short_name'], df_courses['avg_grade'],
                color=bar_colors, edgecolor='white', width=0.6)

# Подписи значений над столбцами
for bar, val in zip(bars1, df_courses['avg_grade']):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05,
             f'{val:.2f}', ha='center', fontsize=9)

# Горизонтальная линия среднего
ax1.axhline(overall_mean, color='darkorange', linestyle='--',
            linewidth=1.5, label=f'Общее среднее: {overall_mean:.2f}')

ax1.set_ylim(2.5, 5.5)
ax1.set_ylabel('Средний балл')
ax1.set_title('Средний балл по курсам', fontweight='bold', pad=10)
ax1.set_xticklabels(df_courses['short_name'], rotation=45, ha='right')
ax1.legend(loc='lower right')

# Выводы по графику
if not df_courses.empty:
    best_course = df_courses.loc[df_courses['avg_grade'].idxmax()]
    worst_course = df_courses.loc[df_courses['avg_grade'].idxmin()]
    print(f"   • Лучший курс: «{best_course['short_name']}» ({best_course['avg_grade']:.2f})")
    print(f"   • Худший курс: «{worst_course['short_name']}» ({worst_course['avg_grade']:.2f})")

# ============================================
# ГРАФИК 2: КОЛИЧЕСТВО СДАЧ ПО КУРСАМ
# ============================================

print("\n📊 График 2: Количество сдач по курсам (столбчатая диаграмма)")

bars2 = ax2.bar(df_courses['short_name'], df_courses['total_enrollments'],
                color='#5cb85c', edgecolor='white', width=0.6)

for bar in bars2:
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
             str(int(bar.get_height())), ha='center', fontsize=9)

ax2.set_ylabel('Количество сдач')
ax2.set_title('Количество сдач по курсам', fontweight='bold', pad=10)
ax2.set_xticklabels(df_courses['short_name'], rotation=45, ha='right')

# Выводы по графику
if not df_courses.empty:
    most_popular = df_courses.loc[df_courses['total_enrollments'].idxmax()]
    print(f"   • Самый популярный курс: «{most_popular['short_name']}» ({most_popular['total_enrollments']} сдач)")

# ============================================
# ГРАФИК 3: РАСПРЕДЕЛЕНИЕ ОЦЕНОК
# ============================================

print("\n📊 График 3: Распределение оценок (гистограмма)")

grade_counts = df_all_grades['grade'].value_counts().sort_index()

bars3 = ax3.bar(grade_counts.index, grade_counts.values,
                color='#f0ad4e', edgecolor='white', width=0.5)

# Подписи над столбцами
for bar, (grade, cnt) in zip(bars3, grade_counts.items()):
    pct = cnt / len(df_all_grades) * 100
    ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
             f'{cnt}\n({pct:.0f}%)', ha='center', fontsize=8)

# Линии среднего и медианы
ax3.axvline(overall_mean, color='blue', linestyle='--',
            linewidth=1.5, label=f'Среднее: {overall_mean:.2f}')
ax3.axvline(overall_median, color='crimson', linestyle='--',
            linewidth=1.5, label=f'Медиана: {overall_median:.2f}')

ax3.set_xticks([2, 3, 4, 5])
ax3.set_xlabel('Оценка')
ax3.set_ylabel('Количество записей')
ax3.set_title('Распределение оценок', fontweight='bold', pad=10)
ax3.legend()

# Текст со статистикой
stats_text = f'Всего оценок: {len(df_all_grades)}\nСр.знач: {overall_mean:.2f}\nМедиана: {overall_median:.2f}\nСт.откл.: {overall_std:.2f}'
ax3.text(0.97, 0.95, stats_text, transform=ax3.transAxes,
         va='top', ha='right', fontsize=8,
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# ============================================
# ГРАФИК 4: УСПЕВАЕМОСТЬ ПО ГОДАМ ПОСТУПЛЕНИЯ
# ============================================

print("\n📊 График 4: Успеваемость по годам поступления (линейный график)")

# Удаляем строки с NULL (где нет оценок)
df_yearly_performance_clean = df_yearly_performance.dropna(subset=['avg_grade'])

if not df_yearly_performance_clean.empty:
    ax4.plot(df_yearly_performance_clean['enrollment_year'],
             df_yearly_performance_clean['avg_grade'],
             marker='o', linewidth=2, markersize=8, color='#7b68ee')

    # Подписи точек
    for _, row in df_yearly_performance_clean.iterrows():
        ax4.annotate(f'{row["avg_grade"]:.2f}',
                     (row['enrollment_year'], row['avg_grade']),
                     textcoords="offset points", xytext=(0, 10), ha='center')

    ax4.set_xlabel('Год поступления')
    ax4.set_ylabel('Средний балл')
    ax4.set_title('Успеваемость по годам поступления', fontweight='bold', pad=10)
    ax4.set_xticks(df_yearly_performance_clean['enrollment_year'])
    ax4.set_ylim(3.5, 4.5)

    print(
        f"   • Динамика успеваемости: от {df_yearly_performance_clean['avg_grade'].min():.2f} до {df_yearly_performance_clean['avg_grade'].max():.2f}")
else:
    ax4.text(0.5, 0.5, 'Недостаточно данных\nдля отображения',
             ha='center', va='center', transform=ax4.transAxes)
    print("   • Недостаточно данных для анализа динамики")

# ============================================
# БЛОК 5: АНОМАЛИИ И ИТОГОВЫЕ ВЫВОДЫ
# ============================================

print("\n" + "=" * 70)
print("АНАЛИЗ АНОМАЛИЙ И ИТОГОВЫЕ ВЫВОДЫ")
print("=" * 70)

print("\n🔍 ОБНАРУЖЕННЫЕ АНОМАЛИИ:")

# Аномалия 1: Студенты без оценок
if len(df_missing) > 0:
    print(f"\n   1. Студенты без записей об успеваемости: {len(df_missing)} человек")
    for _, student in df_missing.head(5).iterrows():
        print(f"      • {student['student']} (год поступления: {int(student['enrollment_year'])})")
    if len(df_missing) > 5:
        print(f"      ... и ещё {len(df_missing) - 5} студентов")
else:
    print("\n   1. Студентов без оценок не обнаружено ✅")

# Аномалия 2: Оценки 2
grade_2_count = len(df_all_grades[df_all_grades['grade'] == 2])
if grade_2_count > 0:
    print(
        f"\n   2. Оценки «2» (неудовлетворительно): {grade_2_count} шт. ({grade_2_count / len(df_all_grades) * 100:.1f}%)")
    print("      → Требуется анализ причин низкой успеваемости")
else:
    print("\n   2. Оценок «2» не обнаружено ✅")

# Аномалия 3: Курс с аномально низким средним
if not df_courses.empty:
    lowest_course = df_courses.loc[df_courses['avg_grade'].idxmin()]
    if lowest_course['avg_grade'] < overall_mean - overall_std:
        print(f"\n   3. Курс с аномально низкой успеваемостью: «{lowest_course['short_name']}»")
        print(
            f"      Средний балл: {lowest_course['avg_grade']:.2f} (ниже общего среднего на {overall_mean - lowest_course['avg_grade']:.2f})")
    else:
        print(f"\n   3. Курсов с аномально низкой успеваемостью не обнаружено ✅")

# ============================================
# СОХРАНЕНИЕ ГРАФИКА
# ============================================

plt.tight_layout()
OUTPUT_FILE = "student_analysis_charts.png"
plt.savefig(OUTPUT_FILE, bbox_inches='tight', dpi=150)
print(f"\n✓ График сохранён: {OUTPUT_FILE}")

# ============================================
# ИТОГОВЫЕ ВЫВОДЫ
# ============================================

print("\n" + "=" * 70)
print("ИТОГОВЫЕ ВЫВОДЫ ПО РЕЗУЛЬТАТАМ АНАЛИЗА")
print("=" * 70)

print(f"""
1. ПО УСПЕВАЕМОСТИ:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • Общая средняя успеваемость: {overall_mean:.2f} балла
   • Медиана ({overall_median:.2f}) {'выше' if overall_median > overall_mean else 'ниже'} среднего
   • Стандартное отклонение: {overall_std:.2f} (умеренный разброс)

2. РЕКОМЕНДАЦИИ:
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   • {'Провести анализ причин низкой успеваемости' if grade_2_count > 0 else 'Продолжать поддерживать высокий уровень успеваемости'}
   • {'Добавить записи об успеваемости для студентов без оценок' if len(df_missing) > 0 else 'Все студенты имеют записи об успеваемости'}
   • {'Обратить внимание на курс с низкой успеваемостью' if not df_courses.empty and df_courses['avg_grade'].min() < overall_mean - overall_std else 'Успеваемость по всем курсам стабильна'}
""")

# Показываем график
plt.show()

print("\n" + "=" * 70)
print("ЗАДАНИЕ ВЫПОЛНЕНО УСПЕШНО!")
print("=" * 70)