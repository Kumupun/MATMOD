import numpy as np

import func
import visual

def input_parameters() -> tuple:
    '''ВВІД ПАРАМЕТРІВ - Вручну або з файлу '''

    choice = input("Введіть тип вводу параметрів \n1 - Вручну \n2 - З файлу \nВаш вибір: ")
    match choice:
        case '1':
            L = float(input("Введіть довжину області (L): "))
            T = float(input("Введіть час моделювання (T): "))
            C = float(input("Введіть швидкість поширення (c): "))
        case '2':
            filename = input("Введіть шлях до файлу з параметрами: ")
            if filename == "":
                print("Шлях не вказано. Використовуються параметри за замовчуванням test.txt")
                filename = "test.txt"
            try:
                with open(filename, 'r') as file:
                    lines = file.readlines()
                    L = float(lines[1].split()[1])
                    T = float(lines[2].split()[1])
                    C = float(lines[3].split()[1])
            except Exception as e:
                print(f"Помилка при читанні файлу: {e}")
                return None, None, None
    
    return L, T, C 


def main():
    L, T, C = input_parameters()
    
    result = func.solve_wave_equation(L, T, C)

    visual.visual(result[0], result[1], result[2])
    
    print(f"Введені параметри: L={L}, T={T}, C={C}")
    print(f"Точне рішення в кінцевий момент часу: \n{result[3]}\n")
    print(f"Чисельне рішення в кінцевий момент часу: \n{result[4]}\n")
    print(f"Максимальна похибка: {result[5]}")
    print(f"Середньоквадратична помилка: {result[6]}")

if __name__ == "__main__":
    main()