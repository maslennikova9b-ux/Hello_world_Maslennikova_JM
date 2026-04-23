# Нахождение количества положительных чисел в массиве

# Заданный массив (с положительными, отрицательными и нулём)
array = [15, -23, 8, -42, 0, 17, -31, 5, 29, -14, 36, -7]

print("Исходный массив:", array)

# Подсчёт положительных чисел
positive_count = 0
positive_numbers = []

for element in array:
    if element > 0:
        positive_count += 1
        positive_numbers.append(element)

# Вывод результата
print(f"Положительные числа: {positive_numbers}")
print(f"Количество положительных чисел: {positive_count}")