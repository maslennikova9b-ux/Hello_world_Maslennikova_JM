# task_2-5_nucl_count.py

# Задаем последовательность ДНК напрямую
dna_sequence = "ATGCTAGC"

# Преобразуем последовательность в верхний регистр (на всякий случай, если вдруг будут маленькие буквы)
dna_upper = dna_sequence.upper()

# Выводим последовательность в верхнем регистре
print(f"\nПоследовательность в верхнем регистре: {dna_upper}")

# Подсчитываем количество каждого нуклеотида
count_A = dna_upper.count('A')
count_T = dna_upper.count('T')
count_G = dna_upper.count('G')
count_C = dna_upper.count('C')

# Выводим подсчет нуклеотидов
print("\nПодсчёт нуклеотидов:")
print(f"A: {count_A}")
print(f"T: {count_T}")
print(f"G: {count_G}")
print(f"C: {count_C}")

# Общая длина последовательности
total_length = len(dna_upper)
print(f"\nОбщая длина: {total_length} нуклеотидов")

# Рассчитываем и выводим процентное содержание
print("\nПроцентное содержание:")
print(f"A: {(count_A / total_length * 100):.2f}%")
print(f"T: {(count_T / total_length * 100):.2f}%")
print(f"G: {(count_G / total_length * 100):.2f}%")
print(f"C: {(count_C / total_length * 100):.2f}%")