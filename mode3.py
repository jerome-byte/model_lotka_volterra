import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from matplotlib.widgets import Slider

# -----------------------------
# Modèle Lotka-Volterra
# -----------------------------
def lotka_volterra(pop, t, alpha, beta, delta, gamma):
    x, y = pop
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

# -----------------------------
# Paramètres initiaux
# -----------------------------
alpha0 = 1.0
beta0 = 0.1
delta0 = 0.1
gamma0 = 1.5
x0, y0 = 10, 5
initial_conditions = [x0, y0]
t = np.linspace(0, 50, 1000)

# -----------------------------
# Création figure
# -----------------------------
fig, ax = plt.subplots(2, 1, figsize=(10,8))
plt.subplots_adjust(left=0.1, bottom=0.35, right=0.95, top=0.95)

# Graphique populations
line1, = ax[0].plot(t, np.zeros_like(t), label='Proies', color='blue')
line2, = ax[0].plot(t, np.zeros_like(t), label='Prédateurs', color='red')
ax[0].set_xlabel('Temps')
ax[0].set_ylabel('Population')
ax[0].set_title('Dynamique proies-prédateurs')
ax[0].legend()
ax[0].grid(True)

# Diagramme de phase
phase_line, = ax[1].plot([], [], color='purple')
ax[1].set_xlabel('Proies')
ax[1].set_ylabel('Prédateurs')
ax[1].set_title('Diagramme de phase')
ax[1].grid(True)

# -----------------------------
# Sliders pour tous les paramètres
# -----------------------------
slider_ax = []
slider_list = []
param_info = [('alpha', 0.1, 3.0, alpha0),
              ('beta', 0.01, 1.0, beta0),
              ('delta', 0.01, 1.0, delta0),
              ('gamma', 0.1, 3.0, gamma0)]

for i, (name, vmin, vmax, valinit) in enumerate(param_info):
    ax_slider = plt.axes([0.25, 0.25 - i*0.05, 0.65, 0.03])
    slider = Slider(ax_slider, name, vmin, vmax, valinit=valinit)
    slider_ax.append(ax_slider)
    slider_list.append(slider)

# -----------------------------
# Fonction de mise à jour
# -----------------------------
def update(val):
    alpha_val = slider_list[0].val
    beta_val  = slider_list[1].val
    delta_val = slider_list[2].val
    gamma_val = slider_list[3].val

    solution = odeint(lotka_volterra, initial_conditions, t, args=(alpha_val, beta_val, delta_val, gamma_val))
    x, y = solution[:,0], solution[:,1]

    line1.set_ydata(x)
    line2.set_ydata(y)
    phase_line.set_data(x, y)

    ax[0].relim()
    ax[0].autoscale_view()
    ax[1].relim()
    ax[1].autoscale_view()
    fig.canvas.draw_idle()

for slider in slider_list:
    slider.on_changed(update)

# -----------------------------
# Simulation initiale
# -----------------------------
update(None)
plt.show()