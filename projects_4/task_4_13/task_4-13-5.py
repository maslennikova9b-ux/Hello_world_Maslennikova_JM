# Поиск максимального из N чисел

# Список чисел
numbers = [23, 45, 12, 67, 34, 89, 56, 78, 90, 33]
N = len(numbers)

print(f"Числа: {numbers}")
print(f"Количество чисел: {N}")

# Поиск максимального
max_number = numbers[0]

for i in range(1, N):
    if numbers[i] > max_number:
        max_number = numbers[i]

# Вывод результата
print("Максимальное число:", max_number)