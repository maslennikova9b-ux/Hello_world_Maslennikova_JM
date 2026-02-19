# task_2-3_recipe.py
# Программа для создания рецептурного справочника

# Запрос данных у пользователя
medium_name = input("Введите название питательной среды: ")
agar_concentration = input("Введите концентрацию агара (%): ")
sterilization_temp = input("Введите температуру стерилизации (°C): ")

# Запись данных в файл
with open('recipe.txt', 'w', encoding='utf-8') as file:
    file.write(f"{medium_name}\n")
    file.write("=" * 30 + "\n")
    file.write(f"• Концентрация агара: {agar_concentration}%\n")
    file.write(f"• Температура стерилизации: {sterilization_temp}°C\n")

# Вывод сообщения о завершении
print(f"\nФайл 'recipe.txt' успешно сформирован!")