import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

def vizual(X, Y, xi_list, frame_interval):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    surf = ax.plot_surface(X, Y, xi_list[0], cmap = plt.cm.RdBu_r)

    def move(num):
        ax.clear()
        surface = ax.plot_surface(X/1000, Y/1000, xi_list[num], cmap = plt.cm.Blues)
        ax.set_title("Wave front $\\xi (x,y,t)$ for $t={}$ minutes".format(int(num*frame_interval/60)), fontsize = 15)
        ax.set_xlabel("$x, \ km$", fontsize = 15)
        ax.set_ylabel("$y, \ km$", fontsize = 15)
        ax.set_zlabel("$\\xi, \ m$", fontsize = 15)
        ax.set_xlim(X.min()/1000, X.max()/1000)
        ax.set_ylim(Y.min()/1000, Y.max()/1000)
        ax.set_zlim(-0.5, 0.5)
        plt.tight_layout()
        return surface

    viz = animation.FuncAnimation(fig, move, frames = len(xi_list), interval = 10, blit = False)
    return viz    # возвращем для визуализации


a = 1e+6
h_0 = 100
g = 9.81
n = 300
dx = a/(n-1)
dy = a/(n-1)
dt = 0.1*min(dx, dy)/np.sqrt(g*h_0) 
num_of_calc = 5000
X, Y = np.meshgrid(np.linspace(-a/2, a/2, n), np.linspace(-a/2, a/2, n)) 



u_now = np.zeros((n, n))    # скорость по х
u_next = np.zeros((n, n))
v_now = np.zeros((n, n))    # скорость по у
v_next = np.zeros((n, n))
xi_now = np.zeros((n, n))   # высота волны ось 0z
xi_next = np.zeros((n, n))
h = np.zeros((n, n))


h_e = np.zeros((n, n))
h_w = np.zeros((n, n))
h_n = np.zeros((n, n))
h_s = np.zeros((n, n))
uhwe = np.zeros((n, n)) 
vhns = np.zeros((n, n))

xi_list = list()              
anim_interval = 20

xi_now = -0.5*np.exp(-((X)**2/(2*(0.05E+6)**2) + (Y)**2/(2*(0.05E+6)**2)))

for i in range(1, num_of_calc):
    u_next[:-1, :] = u_now[:-1, :] - g*dt/dx*(xi_now[1:, :] - xi_now[:-1, :])
    v_next[:, :-1] = v_now[:, :-1] - g*dt/dy*(xi_now[:, 1:] - xi_now[:, :-1])
    
    h_e[:-1, :] = np.where(u_next[:-1, :] > 0, xi_now[:-1, :] + h_0, xi_now[1:, :] + h_0)
    h_e[-1, :] = xi_now[-1, :] + h_0

    h_w[0, :] = xi_now[0, :] + h_0
    h_w[1:, :] = np.where(u_next[:-1, :] > 0, xi_now[:-1, :] + h_0, xi_now[1:, :] + h_0)

    h_n[:, :-1] = np.where(v_next[:, :-1] > 0, xi_now[:, :-1] + h_0, xi_now[:, 1:] + h_0)
    h_n[:, -1] = xi_now[:, -1] + h_0

    h_s[:, 0] = xi_now[:, 0] + h_0
    h_s[:, 1:] = np.where(v_next[:, :-1] > 0, xi_now[:, :-1] + h_0, xi_now[:, 1:] + h_0)

    uhwe[0, :] = u_next[0, :]*h_e[0, :]
    uhwe[1:, :] = u_next[1:, :]*h_e[1:, :] - u_next[:-1, :]*h_w[1:, :]
    
    vhns[:, 0] = v_next[:, 0]*h_n[:, 0]
    vhns[:, 1:] = v_next[:, 1:]*h_n[:, 1:] - v_next[:, :-1]*h_s[:, 1:]

    xi_next[:, :] = xi_now[:, :] - dt*(uhwe[:, :]/dx + vhns[:, :]/dy)   

    u_now = np.copy(u_next)
    v_now = np.copy(v_next)
    xi_now = np.copy(xi_next)

    if (i % anim_interval == 0):
        print("Сделано {} из {}".format(i, num_of_calc))
        xi_list.append(xi_now)

xi_viz = vizual(X, Y, xi_list, anim_interval*dt)

plt.show()