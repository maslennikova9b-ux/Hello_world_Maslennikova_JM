# task_2-2_3.py
# Программа для учета лабораторного оборудования

# Инициализация переменных с данными об оборудовании
# Используем осмысленные имена в стиле snake_case
device_name = "Микроскоп оптический"
inventory_number = "INV-2023-001"
is_operational = True  # True - исправен, False - неисправен
quantity = 3
# device_name2 = "Центрифуга лабораторная"
inventory_number_2 = "INV-2023-045"
is_operational_2 = True
quantity_2 = 1
# device_name3 = "Термостат"
inventory_number_3 = "INV-2022-112"
is_operational_3 = False
quantity_3 = 2
device_name_4 = "Анализатор спектральный"
inventory_number_4 = "INV-2023-089"
is_operational_4 = True
quantity_4 = 1

# Вывод данных в виде таблицы с использованием символов табуляции \t
print("Наименование прибора\t\tИнвентарный номер\tСостояние\tКоличество")
print("-" * 80)

# Функция для преобразования булевого значения в текст
def get_status_text(is_operational):
    return "исправен" if is_operational else "неисправен"

# Вывод данных каждого прибора
print(f"{device_name}\t\t{inventory_number}\t{get_status_text(is_operational)}\t{quantity}")
print(f"{device_name_2}\t{inventory_number_2}\t{get_status_text(is_operational_2)}\t{quantity_2}")
print(f"{device_name_3}\t\t{inventory_number_3}\t{get_status_text(is_operational_3)}\t{quantity_3}")
print(f"{device_name_4}\t{inventory_number_4}\t{get_status_text(is_operational_4)}\t{quantity_4}")

print("-" * 80)