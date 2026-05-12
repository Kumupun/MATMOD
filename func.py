import numpy as np

def solve_wave_equation(L, T, C) -> tuple:
    '''СІТКОВИЙ МЕТОД - Розв'язання хвильового рівняння
    РОЗБИВАЄМО ПРОСТІР НА СІТКУ, ВИКОРИСТОВУЄМО ДИСКРЕТНІ ПРИБЛИЖЕННЯ ДЛЯ ЧИСЛЕННОГО РОЗВ'ЯЗАННЯ'''

    nx = int(L*20)          # РОЗБИТТЯ НА X (20 точок на одиницю довжини)
    nt = int(T*100)          # РОЗЬИТТЯ НА T (100 кроків на одиницю часу)

    dx = 2*L / (nx - 1)
    dt = T / nt

    lamd = C * dt / dx      # УМОВА СТІЙКОСТІ
    if lamd > 1:
        print(f"Система нестійка (λ = {lamd:.2f} > 1). Зменшіть dt або збільшіть dx.")
    
    x = np.linspace(-L, L, nx)
    t = np.linspace(0, T, nt)
    y = np.zeros((nt, nx))

    u0 = lambda x: np.exp(-x**2)            # ПОЧАТКОВА УМОВИ умови (тут треба придумати як реалізувати ввід )
    u1 = lambda x: np.zeros_like(x)

    def exact_solution(x, t):               # ТОЧНЕ РІВНЯННЯ ДЛЯ ПЕРЕВІРКИ ТІЛЬКИ КОЛИ u1 = 0
        return 0.5 * (u0(x - C*t) + u0(x + C*t))

    Y = np.zeros((nt, nx))

    Y[0, :] = u0(x)                          # ПОЧАТКОВИЙ ШАР
    for i in range(1, nx-1):
        Y[1, i] = (Y[0, i] + dt * u1(x[i]) + (lamd**2 / 2) * (Y[0, i+1] - 2*Y[0, i] + Y[0, i-1]))

    y[:, 0] = 0                         # КРАЙОВІ УМОВИ (Діріхле поки, а так теж ввід треба придумати)
    y[:, -1] = 0

    for n in range(1, nt-1):        # ОСНОВНИЙ ЦИКЛ РОЗВ'ЯЗАННЯ
        for i in range(1, nx-1):
            Y[n+1, i] = (2*Y[n, i] - Y[n-1, i] + lamd**2 * (Y[n, i+1] - 2*Y[n, i] + Y[n, i-1]))

    t_final = t[-1]

    Y_exact = exact_solution(x, t_final)
    Y_numeric = Y[-1]

    err = np.max(np.abs(Y_exact - Y_numeric))
    err2 = np.mean((Y_exact - Y_numeric)**2)

    return x, Y, dt, Y_exact, Y_numeric, err, err2