import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import matplotlib.animation as animation


fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'k-', animated=True)  


fs = 1000 
t = np.arange(0, 10, 1/fs)  


def generate_ecg_signal(t):
   
    heart_rate = 75  
    period = 60 / heart_rate  


    signal = (
        0.2 * np.sin(2 * np.pi * 1.0 * t) +  # Onda P
        1.0 * (np.sin(2 * np.pi * 1.0 * t) * ((t % period) < (0.15 * period))) +  # Onda QRS
        0.5 * (np.sin(2 * np.pi * 0.5 * t) * (((t % period) > (0.5 * period)) & ((t % period) < (0.65 * period))))  # Onda T
    )
    
    signal += 0.1 * np.random.randn(len(t))
    return signal


ecg_signal = generate_ecg_signal(t)

#
def init():
    ax.set_xlim(0, 100)
    ax.set_ylim(-2, 2)
    ax.grid(True, which='both', linestyle='--', color='gray', alpha=0.7)  
    ax.set_xlabel('Tiempo (ms)')
    ax.set_ylabel('Voltaje (mV)')
    return ln,


def update(frame):
    
    ydata.append(ecg_signal[frame % len(ecg_signal)])
    xdata.append(frame)
    if len(ydata) > 100:
        ax.set_xlim(xdata[-100], xdata[-1])  
    ln.set_data(xdata, ydata)
    return ln,


def animate(*args):
    ani = animation.FuncAnimation(fig, update, init_func=init, blit=True, interval=10)
    canvas.draw()


root = tk.Tk()
root.title("Simulación de Señal ECG en Tiempo Real")


canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


btn_start = tk.Button(root, text="Iniciar", command=animate)
btn_start.pack(side=tk.BOTTOM)

tk.mainloop()
