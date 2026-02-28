# task_2-6_3.py

# Задаем группы крови напрямую
donor = "I"  # Группа крови донора
recipient = "IV"  # Группа крови пациента

# Проверяем корректность ввода (на всякий случай)
valid_groups = ["I", "II", "III", "IV"]

if donor not in valid_groups or recipient not in valid_groups:
    print("Ошибка: введите корректную группу крови (I, II, III, IV)")
else:
    # Определяем возможность переливания
    # Переливание возможно если:
    # 1. Донор имеет I (0) группу (универсальный донор) ИЛИ
    # 2. Группы совпадают

    if donor == "I" or donor == recipient:
        print(f"Донор {donor} -> Реципиент {recipient}: Кровь совместима")

        # Дополнительная информация
        if donor == "I" and donor != recipient:
            print("(I группа - универсальный донор)")
        elif donor == recipient:
            print("(Группы совпадают)")
    else:
        print(f"Донор {donor} -> Реципиент {recipient}: Кровь НЕ совместима")