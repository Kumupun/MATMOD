import numpy as np
import func
import visual

def input_parameters() -> tuple:
    '''ВВІД ПАРАМЕТРІВ - Вручну або з файлу '''

    choice = input("Введіть тип вводу параметрів \n1 - Вручну \n2 - З файлу \nВаш вибір: ")
    
    match choice:
        case '1':
            try:
                L = float(input("Введіть довжину області (L): "))
                T = float(input("Введіть час моделювання (T): "))
                C = float(input("Введіть швидкість поширення (c): "))
            except ValueError:
                print("Помилка вводу. Будь ласка, введіть числові значення.")
                return None, None, None
            
        case '2':
            filename = input("Введіть шлях до файлу з параметрами: ")
            if filename.strip() == "":
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

def final_output(params, Y_exact, Y_numeric, err, err2):
    '''ВИВІД РЕЗУЛЬТАТІВ - Вивід точного та чисельного розв'язку, а також помилок'''

    #ФОРМАТ ВИВОДУ МАТРИЦЬ  
    np.set_printoptions(suppress=True, precision=2)                          # ВИВІД , 2 ДЕСЯТКОВИХ ЧИСЛА               
    np.set_printoptions(formatter={'float_kind': lambda x: f"{x:.3e}"})      # ВИВІД У НАУКОВОМУ ФОРМАТІ (НАПРИКЛАД 1.23e-04) З 4 ДЕСЯТКОВИМИ ЧИСЛАМИ

    print(f"Введені параметри: L={params[0]}, T={params[1]}, C={params[2]}")
    print(f"Точне рішення в кінцевий момент часу: \n{Y_exact}\n")
    print(f"Чисельне рішення в кінцевий момент часу: \n{Y_numeric}\n")
    print(f"Максимальна похибка: {err}")
    print(f"Середньоквадратична помилка: {err2}")

def main():
    params = input_parameters()
    if params == (None, None, None):
        raise ValueError("Невірні параметри.")
    
    (x, Y, dt, Y_exact, Y_numeric, err, err2) = func.solve_wave_equation(params)
    
    final_output(params, Y_exact, Y_numeric, err, err2)

    visual.visual(x, Y, dt)

if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print(f"Сталася помилка: {e}")