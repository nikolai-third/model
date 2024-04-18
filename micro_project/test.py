import numpy as np

# Создаем одномерные массивы координатных значений
x = np.linspace(0, 1, 3)  # [0. 0.5 1.]
y = np.linspace(0, 1, 2)  # [0. 1.]

# Создаем координатные сетки
X, Y = np.meshgrid(x, y)

# Выводим результат
print(X[0][2])
#print(Y)