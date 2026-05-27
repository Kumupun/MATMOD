import numpy as np

def input_function(name, L):
    # ВВІД ФУНКЦІЇ
    while True:
        expr = input(f"Введіть {name}(x): ").strip().replace("L", str(L))
        try:
            compile(expr, "<string>", "eval")
            def f(x, _e=expr):
                x = np.asarray(x, dtype=float)
                r = eval(_e, {"x": x, "np": np, "sin": np.sin, "cos": np.cos,
                              "exp": np.exp, "sqrt": np.sqrt, "pi": np.pi, "e": np.e})
                return r * np.ones_like(x) if np.ndim(r) == 0 else r
            vals = f(np.linspace(-L, L, 20))
            if not np.all(np.isfinite(vals)):
                print("Функція дає NaN або inf. Спробуйте ще раз.")
                continue
            return f
        except Exception as e:
            print(f"Помилка: {e}. Спробуйте ще раз.")

def input_boundary_conditions(dx):
    # ВВІД КРАЙОВИХ УМОВ: 1 - ДІРІХЛЕ, 2 - НЕЙМАН, 3 - РОБІН
    print("Крайові умови: 1 - Діріхле | 2 - Нейман | 3 - Робін")
    choice = input("Ваш вибір: ").strip()

    if choice == "1":
        vl = float(input("u(-L) = "))
        vr = float(input("u(+L) = "))
        def apply(Y, n):
            Y[n, 0] = vl;  Y[n, -1] = vr
        return apply

    elif choice == "2":
        hl = float(input("u_x(-L) = "))
        hr = float(input("u_x(+L) = "))
        def apply(Y, n):
            Y[n, 0]  = Y[n, 1]  - dx * hl
            Y[n, -1] = Y[n, -2] + dx * hr
        return apply

    elif choice == "3":
        alpha   = float(input("α = "))
        beta    = float(input("β = "))
        g_left  = float(input("g(-L) = "))
        g_right = float(input("g(+L) = "))
        denom   = alpha + beta / dx
        def apply(Y, n):
            Y[n, 0]  = (g_left  + (beta / dx) * Y[n, 1])  / denom
            Y[n, -1] = (g_right + (beta / dx) * Y[n, -2]) / denom
        return apply

    else:
        print("Невідомий вибір. Використовуємо Діріхле(0, 0).")
        def apply(Y, n):
            Y[n, 0] = 0;  Y[n, -1] = 0
        return apply

def solve_wave_equation(params) -> tuple:
    '''СІТКОВИЙ МЕТОД - Розв'язання хвильового рівняння
    РОЗБИВАЄМО ПРОСТІР НА СІТКУ, ВИКОРИСТОВУЄМО ДИСКРЕТНІ ПРИБЛИЖЕННЯ ДЛЯ ЧИСЛЕННОГО РОЗВ'ЯЗАННЯ'''
    L, T, C = float(params[0]), float(params[1]), float(params[2])

    nx = int(L*20)          # РОЗБИТТЯ НА X (100 точок на одиницю довжини)
    nt = int(T*100)         # РОЗБИТТЯ НА T (100 кроків на одиницю часу)

    dx = 2*L / (nx - 1)
    dt = T / nt

    lamd = C * dt / dx      # УМОВА СТІЙКОСТІ
    if lamd > 1:
        print(f"Система нестійка (λ = {lamd:.2f} > 1). Зменшіть dt або збільшіть dx.")

    x = np.linspace(-L, L, nx)
    t = np.linspace(0, T, nt)

    Y = np.zeros((nt, nx))

    u0 = input_function("u0", L)    # ПОЧАТКОВІ УМОВИ ЧЕРЕЗ EVAL
    u1 = input_function("u1", L)

    apply_bc = input_boundary_conditions(dx)    # КРАЙОВІ УМОВИ

    def exact_solution(x, t):                   # ФОРМУЛА ДАЛАМБЕРА ДЛЯ БУДЬ ЯКОГО u0 u1 на нескінченній прямій
        res = 0.5 * (u0(x - C * t) + u0(x + C * t))

        # чисельний інтеграл
        integral_part = np.zeros_like(x)
        for i, xi in enumerate(x):
            s = np.linspace(xi - C*t, xi + C*t, 200)  # розбиття
            integral_part[i] = np.trapezoid(u1(s), s)

        res += (1 / (2 * C)) * integral_part
        return res

    Y[0, :] = u0(x)                 # ПОЧАТКОВИЙ ШАР
    apply_bc(Y, 0)                  # КРАЙОВІ УМОВИ

    for i in range(1, nx-1):
        Y[1, i] = (Y[0, i] + dt * u1(x[i]) + (lamd**2 / 2) * (Y[0, i+1] - 2*Y[0, i] + Y[0, i-1]))
    apply_bc(Y, 1)

    for n in range(1, nt-1):        # ОСНОВНИЙ ЦИКЛ РОЗВ'ЯЗАННЯ
        for i in range(1, nx-1):
            Y[n+1, i] = (2*Y[n, i] - Y[n-1, i] + lamd**2 * (Y[n, i+1] - 2*Y[n, i] + Y[n, i-1]))
        apply_bc(Y, n+1)

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