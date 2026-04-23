# Нахождение суммы всех нечётных элементов в массиве

# Заданный массив
array = [15, 23, 8, 42, 17, 31, 5, 29, 14, 36, 7, 12]

print("Исходный массив:", array)

# Вычисление суммы нечётных элементов
sum_odd = 0
odd_numbers = []

for element in array:
    if element % 2 != 0:  # проверка на нечётность
        sum_odd += element
        odd_numbers.append(element)

# Вывод результата
print(f"Нечётные элементы: {odd_numbers}")
print(f"Сумма всех нечётных элементов: {sum_odd}")