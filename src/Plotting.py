import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import colors as mcolors
import Driver

class plotting:
    def __init__(self):
        # Initialize fig and ax
        self.fig, self.ax = plt.subplots(1, 1, figsize=(5,3))        
        self.ax.set_title(("Polarization"))
        self.ax.set_xlabel('E_x')
        self.ax.set_ylabel('E_y')
        self.ax.axhline(0, color='gray', lw=0.5)
        self.ax.axvline(0, color='gray', lw=0.5)
        self.ax.grid(True)
        self.ax.axis('equal')

        # Initialize list of lines for plotting 
        self.lines = []

        # Create Update Button
        self.ax_button = plt.axes([.8, .05, .1, .075])
        self.button = Button(self.ax_button, 'Update')
        self.button.on_clicked(self.update_plot)

        # init hardware
        self.D = Driver.driver()

        # self.initial_plot()
        # plt.show()

    def initial_plot(self):
        Ex, Ey = self.getData()
        line, = self.ax.plot(Ex, Ey, lw=2, color='black')
        self.lines.append(line)

    def update_plot(self, event):
        # Grayscale Gradient
        t = np.linspace(0, 2*np.pi, 180)
        Ex, Ey = self.getData()
        Ex = Ex.real * np.cos(t) - Ex.imag * np.sin(t)
        Ey = Ey.real * np.cos(t) - Ey.imag * np.sin(t)
        for line in self.lines:
            color = np.array(mcolors.to_rgba(line.get_color()))
            color[-1] *= .6
            line.set_color(color)
        
        new_line, = self.ax.plot(Ex, Ey, lw=2, color='black')
        self.lines.append(new_line)

        self.fig.canvas.draw_idle()
        

    
    def getData(self):
        self.D.collect_data()
        self.D.analyze_data()

        return self.D.jones_vector

    def plot_polarization(self, thetas, vectors):
        # Grayscale Gradient

        
        # thetas = np.rad2deg(thetas)
        E_out = vectors
        t = np.linspace(0, 2*np.pi, 180)

        if type(vectors) == list:
            for theta, vector in zip(thetas, vectors):
                Ex = vector[0].real * np.cos(t) - vector[0].imag * np.sin(t)
                Ey = vector[1].real * np.cos(t) - vector[1].imag * np.sin(t)

        else:
            Ex = vectors[0].real * np.cos(t) - vectors[0].imag * np.sin(t)
            Ey = vectors[1].real * np.cos(t) - vectors[1].imag * np.sin(t)

        self.fig, self.ax = plt.subplots(1, 1, figsize=(5,3))

        self.ax.plot(Ex, Ey)
        # ax.set_title(f'QWP at {thetas}°')
        
    def jones_vector(theta):
        # Initial horizontal polarization
        E_in = np.array([1, 0], dtype=complex)
        
        # QWP Jones matrix at angle theta
        qwp_matrix = np.array([
            [np.cos(theta)**2 + 1j*np.sin(theta)**2, (1 - 1j) * np.sin(theta) * np.cos(theta)],
            [(1 - 1j) * np.sin(theta) * np.cos(theta), np.sin(theta)**2 + 1j*np.cos(theta)**2]
        ])
        
        # Output Jones vector after QWP
        E_out = np.dot(qwp_matrix, E_in)
        return E_out

    def show(self):
        plt.show()


if __name__ == '__main__':
    p = plotting()
    p.show()