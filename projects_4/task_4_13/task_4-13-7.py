# Нахождение среднего арифметического всех элементов массива

# Заданный массив чисел
array = [15, 23, 8, 42, 17, 31, 5, 29, 14, 36]

print("Исходный массив:", array)

# Вычисление суммы элементов
sum_elements = 0
for element in array:
    sum_elements += element

# Вычисление среднего арифметического
average = sum_elements / len(array)

# Вывод результата
print(f"Сумма элементов: {sum_elements}")
print(f"Количество элементов: {len(array)}")
print(f"Среднее арифметическое: {average:.2f}")