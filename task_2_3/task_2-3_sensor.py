# task_2-3_sensor.py
# Программа для создания логов датчика давления

# Запрос данных у пользователя
operator_name = input("Введите имя оператора: ")
pressure_value = input("Введите текущее значение давления (Па): ")

# Запись данных в файл в формате таблицы
with open('sensor_log.txt', 'a', encoding='utf-8') as file:
    file.write(f"{operator_name}\t{pressure_value}\n")

# Вывод сообщения о завершении
print("Данные успешно сохранены в sensor_log.txt")