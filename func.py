import numpy as np

def solve_wave_equation(params) -> tuple:
    '''СІТКОВИЙ МЕТОД - Розв'язання хвильового рівняння
    РОЗБИВАЄМО ПРОСТІР НА СІТКУ, ВИКОРИСТОВУЄМО ДИСКРЕТНІ ПРИБЛИЖЕННЯ ДЛЯ ЧИСЛЕННОГО РОЗВ'ЯЗАННЯ'''
    L, T, C = float(params[0]), float(params[1]), float(params[2])

    nx = int(L*20)          # РОЗБИТТЯ НА X (100 точок на одиницю довжини)
    nt = int(T*100)          # РОЗБИТТЯ НА T (100 кроків на одиницю часу)

    dx = 2*L / (nx - 1)
    dt = T / nt

    lamd = C * dt / dx      # УМОВА СТІЙКОСТІ
    if lamd > 1:
        print(f"Система нестійка (λ = {lamd:.2f} > 1). Зменшіть dt або збільшіть dx.")
    
    x = np.linspace(-L, L, nx)
    t = np.linspace(0, T, nt)

    Y = np.zeros((nt, nx)) 

    u0 = lambda x: np.sin(np.pi * x / L)     # ПОЧАТКОВі УМОВИ умови (тут треба придумати як реалізувати ввід ) (eval)
    
    u1 = lambda x: np.zeros_like(x)

    def exact_solution(x, t):                            # ФОРМУЛА ДАЛАМБЕРА ДЛЯ БУДЬ ЯКОГО u0 u1 на нескінченній прямій
        res = 0.5 * (u0(x - C * t) + u0(x + C * t))

        # чисельний інтеграл
        integral_part = np.zeros_like(x)

        for i, xi in enumerate(x):
            s = np.linspace(xi - C*t, xi + C*t, 200)  # розбиття
            integral_part[i] = np.trapezoid(u1(s), s)

        res += (1 / (2 * C)) * integral_part
        return res

    Y = np.zeros((nt, nx))

    Y[0, :] = u0(x)                          # ПОЧАТКОВИЙ ШАР

    Y[:, 0] = 0                       # КРАЙОВІ УМОВИ (Діріхле поки, а так теж ввід треба придумати) (тут можна через input)
    Y[:, -1] = 0
    
    for i in range(1, nx-1):
        Y[1, i] = (Y[0, i] + dt * u1(x[i]) + (lamd**2 / 2) * (Y[0, i+1] - 2*Y[0, i] + Y[0, i-1]))


    for n in range(1, nt-1):        # ОСНОВНИЙ ЦИКЛ РОЗВ'ЯЗАННЯ
        for i in range(1, nx-1):
            Y[n+1, i] = (2*Y[n, i] - Y[n-1, i] + lamd**2 * (Y[n, i+1] - 2*Y[n, i] + Y[n, i-1]))

    t_final = t[-1]

    Y_exact = exact_solution(x, t_final)
    Y_numeric = Y[-1, :]

    print("max Y[0]:", np.max(Y[0]))
    print("max Y[1]:", np.max(Y[1]))  # ДОДАНО ДЛЯ ДІАГНОСТИКИ  
    print("lambda:", lamd)
    print("max final:", np.max(Y[-1]))

    err = np.max(np.abs(Y_exact - Y_numeric))
    err2 = np.mean((Y_exact - Y_numeric)**2)

    return x, Y, dt, Y_exact, Y_numeric, err, err2