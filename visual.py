import matplotlib.pyplot as plt

def visual(x, Y, dt):
    '''ВІЗУАЛІЗАЦІЯ РЕЗУЛЬТАТІВ - Графіки для різних моментів часу'''

    plt.figure(figsize=(10, 6))
    for i in range(0, Y.shape[0], Y.shape[0]//5):
        plt.plot(x, Y[i, :], label=f't = {i*dt:.1f}s')

    plt.title("Хвильовий процес в R1")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.show()