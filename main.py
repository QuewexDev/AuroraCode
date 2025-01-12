from barcode import EAN13
from barcode.writer import ImageWriter
import json
import sys
import os
import random
import time

# Словарь для хранения сгенерированных кодов
generated_codes = {}
last_code = 0

# Функция для вычисления контрольной цифры (V)
def calculate_v(base_code):
    digits = [int(d) for d in str(base_code)]
    total = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits))
    v = (10 - (total % 10)) % 10
    return v

# Функция для отображения меню с проверкой ввода
def menu(vars: list, input_text=">") -> int:
    for i in range(len(vars)):
        print(f'{i+1}: {vars[i]}')

    while True:
        try:
            response = int(input(input_text+" "))
            if 1 <= response <= len(vars):
                return response - 1
            else:
                print("Неверный выбор, попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

# Функция для создания кода EAN13
def create_code(code):
    global last_code
    last_code = code
    digits = [int(d) for d in str(code)]

    if len(digits) not in [4, 5, 6]:
        print("Ошибка: Код должен быть 4, 5 или 6 цифр.")
        return
    
    # Формирование кода EAN13
    c = "290000" + ("0" * (6 - len(digits)) + str(code))

    c_v = c + str(calculate_v(c))

    # Генерация изображения штрих-кода
    result = EAN13(c_v, writer=ImageWriter()) 
    result.save(str(code) + "_barcode_aurora", text=f"AuroraCode\n{c_v}")

    # Добавление сгенерированного кода в список
    generated_codes[str(code)] = c_v
    print(f"Штрих-код для {code} сохранен как {code}_barcode_aurora.png")
    time.sleep(4)

# Главная программа
banner = """
                                     _____          _      
     /\\                             / ____|        | |     
    /  \\  _   _ _ __ ___  _ __ __ _| |     ___   __| | ___ 
   / /\\ \\| | | | '__/ _ \\| '__/ _` | |    / _ \\ / _` |/ _ \\
  / ____ \\ |_| | | | (_) | | | (_| | |___| (_) | (_| |  __/
 /_/    \\_\\__,_|_|  \\___/|_|  \\__,_|\\_____\\___/ \\__,_|\\___|
 """

while True:
    # Очистка экрана в зависимости от операционной системы
    os.system("cls" if sys.platform == "win32" else "clear")

    print(banner)
    print(f"Last Created Code: {last_code}")
    ipt = menu(["Create Code", "Generate Code"])

    if ipt == 0:
        code = input("Введите код (4, 5 или 6 цифр): ")
        if code.isdigit() and len(code) in [4, 5, 6]:
            create_code(code)
        else:
            print("Ошибка: Код должен быть 4, 5 или 6 цифр.")

    elif ipt == 1:
        next_code = random.randint(1000, 112830)

        create_code(next_code)