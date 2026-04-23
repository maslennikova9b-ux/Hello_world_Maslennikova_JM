# Нахождение минимального из четырёх чисел

# Четыре числа
a = 25
b = 18
c = 32
d = 14

print(f"Числа: {a}, {b}, {c}, {d}")

# Поиск минимума
min_number = a

if b < min_number:
    min_number = b
if c < min_number:
    min_number = c
if d < min_number:
    min_number = d

# Вывод результата
print("Минимальное число:", min_number)