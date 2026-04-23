# Нахождение среднего арифметического элементов с чётными индексами

# Заданный массив
array = [12, 25, 38, 41, 55, 63, 77, 84, 96, 10]

print("Исходный массив:", array)
print("Индексы:        0   1   2   3   4   5   6   7   8   9")

# Вычисление суммы и количества элементов с чётными индексами
sum_even_index = 0
count_even_index = 0
even_index_elements = []

for i in range(len(array)):
    if i % 2 == 0:  # проверка на чётность индекса
        sum_even_index += array[i]
        count_even_index += 1
        even_index_elements.append(array[i])
        print(f"Элемент с индексом {i} (значение {array[i]}) учтён")

# Вычисление среднего арифметического
average = sum_even_index / count_even_index

# Вывод результата
print(f"\nЭлементы с чётными индексами: {even_index_elements}")
print(f"Сумма элементов с чётными индексами: {sum_even_index}")
print(f"Количество элементов с чётными индексами: {count_even_index}")
print(f"Среднее арифметическое: {average:.2f}")