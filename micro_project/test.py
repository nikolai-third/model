import numpy as np
import matplotlib.pyplot as plt
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

def solve_poisson_equation(f, Nx, Ny, Lx, Ly, boundary_conditions):
    # Создание сетки
    x = np.linspace(0, Lx, Nx)
    y = np.linspace(0, Ly, Ny)
    dx = x[1] - x[0]
    dy = y[1] - y[0]

    # Формирование координатной сетки
    X, Y = np.meshgrid(x, y)
    
    # Преобразование правой части в одномерный массив
    f_vec = f(X, Y).flatten()

    # Формирование матрицы системы уравнений
    main_diag = -2 * (1 / dx**2 + 1 / dy**2) * np.ones(Nx * Ny)
    off_diag = np.ones(Nx * Ny - 1) / dx**2
    off_diag2 = np.ones(Nx * (Ny - 1)) / dy**2

    diagonals = [main_diag, off_diag, off_diag, off_diag2, off_diag2]
    offsets = [0, -1, 1, -Nx, Nx]
    A = diags(diagonals, offsets, shape=(Nx * Ny, Nx * Ny), format='csr')

    # Обработка граничных условий
    for i, boundary_condition in enumerate(boundary_conditions):
        if boundary_condition is not None:
            if i == 0:  # lower boundary
                f_vec[:Nx] += boundary_condition(X[0, :], Y[0, :]) / dy**2
                A[:Nx, :] = 0
                A[:Nx, :Nx] = diags([np.ones(Nx)], [0], shape=(Nx, Nx), format='csr') / dy**2
            elif i == 1:  # upper boundary
                f_vec[-Nx:] += boundary_condition(X[-1, :], Y[-1, :]) / dy**2
                A[-Nx:, :] = 0
                A[-Nx:, -Nx:] = diags([np.ones(Nx)], [0], shape=(Nx, Nx), format='csr') / dy**2
            elif i == 2:  # left boundary
                f_vec[::Nx] += boundary_condition(X[:, 0], Y[:, 0]) / dx**2
                A[::Nx, :] = 0
                A[::Nx, ::Nx] = diags([np.ones(Ny)], [0], shape=(Ny, Ny), format='csr') / dx**2
            elif i == 3:  # right boundary
                f_vec[Nx-1::Nx] += boundary_condition(X[:, -1], Y[:, -1]) / dx**2
                A[Nx-1::Nx, :] = 0
                A[Nx-1::Nx, Nx-1::Nx] = diags([np.ones(Ny)], [0], shape=(Ny, Ny), format='csr') / dx**2

    # Решение системы уравнений
    u_vec = spsolve(A, f_vec)

    # Преобразование одномерного решения в двумерное
    u = np.reshape(u_vec, (Ny, Nx))

    return x, y, u

def visualize_solution(x, y, u):
    plt.figure(figsize=(8, 6))
    plt.contourf(x, y, u, cmap='viridis')
    plt.colorbar(label='u')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Solution of Poisson Equation')
    plt.grid(True)
    plt.show()

# Пример правой части уравнения (можно заменить на другую функцию)
def f(x, y):
    return np.sin(np.pi * x) * np.cos(np.pi * y)

# Пример граничного условия (можно изменить)
def boundary_condition_lower(x, y):
    return np.zeros_like(x)

def boundary_condition_upper(x, y):
    return np.zeros_like(x)

def boundary_condition_left(x, y):
    return np.sin(np.pi * x)

def boundary_condition_right(x, y):
    return np.sin(np.pi * x)

# Параметры сетки и области
Nx = 100
Ny = 100
Lx = 1
Ly = 1

# Граничные условия (None для свободных границ)
boundary_conditions = [boundary_condition_lower, boundary_condition_upper, boundary_condition_left, boundary_condition_right]

# Решение уравнения Пуассона
x, y, u = solve_poisson_equation(f, Nx, Ny, Lx, Ly, boundary_conditions)

# Визуализация результата
visualize_solution(x, y, u)
