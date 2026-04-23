# Нахождение суммы элементов с нечётными индексами

# Заданный массив
array = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

print("Исходный массив:", array)
print("Индексы:        0   1   2   3   4   5   6   7   8   9")

# Вычисление суммы элементов с нечётными индексами
sum_odd_index = 0
odd_index_elements = []

for i in range(len(array)):
    if i % 2 != 0:  # проверка на нечётность индекса
        sum_odd_index += array[i]
        odd_index_elements.append(array[i])
        print(f"Элемент с индексом {i} (значение {array[i]}) добавлен")

# Вывод результата
print(f"\nЭлементы с нечётными индексами: {odd_index_elements}")
print(f"Сумма элементов с нечётными индексами: {sum_odd_index}")