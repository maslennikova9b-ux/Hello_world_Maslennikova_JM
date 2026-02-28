# task_2-6_2.py

temp = float(input("Какая температура листа сейчас? "))

if temp < 5:
    print("Слишком холодно. Фотосинтез почти не идёт.")
elif 5 <= temp <= 25:
    print("Оптимально для растений с C3-метаболизмом")
elif 25 < temp <= 35:
    print("Хорошо для растений C4-метаболизмом")
else:  # temp > 35
    print("It's hot as hell! Cool down, bro.")