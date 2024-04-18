import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def vizual(X, Y, xi_list):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    surf = ax.plot_surface(X, Y, xi_list[0], cmap = plt.cm.RdBu_r)

    def move(num):
        ax.clear()
        surface = ax.plot_surface(X/1000, Y/1000, xi_list[num], cmap = plt.cm.RdBu_r)
        ax.set_zlim(0, 4e+8)
        plt.tight_layout()
        return surface

    viz = animation.FuncAnimation(fig, move, frames = len(xi_list), interval = 10, blit = False)
    return viz    # возвращем для визуализации


a = 1e+6
h = 100
g = 9.81
n = 300
dx = a/(n-1)
dy = a/(n-1)
dt = 0.1
num_of_calc = 500
X, Y = np.meshgrid(np.linspace(-a/2, a/2, n), np.linspace(-a/2, a/2, n)) 



xi = np.zeros((n, n))

xi_list = list()              
anim_interval = 20

for i in range(1, num_of_calc):
    xi = (num_of_calc-i)*np.sqrt(X**2 + Y**2)
    xi_list.append(xi)

xi_viz = vizual(X, Y, xi_list)

plt.show()