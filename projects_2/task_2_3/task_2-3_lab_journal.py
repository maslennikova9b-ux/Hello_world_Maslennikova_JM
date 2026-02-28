# task_2-3_lab_journal.py
# Программа для создания страницы электронного лабораторного журнала

# Сбор данных от пользователя
researcher_name = input("Введите ФИО исследователя: ")
experiment_date = input("Введите дату (ДД.ММ.ГГГГ): ")
experiment_name = input("Введите название эксперимента: ")
experiment_conclusion = input("Введите вывод: ")

# Формирование файла с рамкой
with open('journal.txt', 'w', encoding='utf-8') as file:
    # Верхняя граница
    file.write("+" + "-" * 50 + "+\n")
    
    # Заголовок
    file.write(f"| {'Электронный лабораторный журнал':<48} |\n")
    file.write("+" + "-" * 50 + "+\n")
    
    # Основная информация
    file.write(f"| {'ФИО исследователя :':<20} {researcher_name:<28} |\n")
    file.write(f"| {'Дата             :':<20} {experiment_date:<28} |\n")
    file.write(f"| {'Эксперимент      :':<20} {experiment_name:<28} |\n")
    
    # Разделитель
    file.write("+" + "-" * 50 + "+\n")
    
    # Вывод (с возможным переносом строк)
    file.write(f"| {'Вывод:':<48} |\n")
    
    # Разбиваем вывод на строки по 48 символов (с учетом отступов)
    words = experiment_conclusion.split()
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= 48:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            file.write(f"| {current_line:<48} |\n")
            current_line = word
    
    # Записываем последнюю строку
    if current_line:
        file.write(f"| {current_line:<48} |\n")
    
    # Нижняя граница
    file.write("+" + "-" * 50 + "+\n")

print("\nЗапись в электронный журнал успешно создана!")