import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import colors as mcolors
import Driver

class plotting:
    def __init__(self):
        # Initialize fig and ax
        self.fig, self.ax = plt.subplots(1, 1, figsize=(4.8,2.75))        
        # self.ax.set_title(("Polarization"))
        self.ax.set_xlabel('E_x')
        self.ax.set_ylabel('E_y')
        self.ax.axhline(0, color='gray', lw=0.5)
        self.ax.axvline(0, color='gray', lw=0.5)
        self.ax.grid(True)
        self.ax.axis('equal')

        # Initialize list of lines for plotting 
        self.lines = []

        # Create Update Button
        # self.ax_button = plt.axes([.9, .05, .1, .075])
        # self.button = Button(self.ax_button, 'Update')
        # self.button.on_clicked(self.update_plot)

        # # Create Clear Button
        # self.clear_button = plt.axes([.9, .15, .1, .075])
        # self.clear_button = Button(self.clear_button,'Clear')
        # self.clear_button.on_clicked(self.clear_plot)

        # # Create avg button
        # self.avg_button = plt.axes([.9, .25, .1, .075])
        # self.avg_button = Button(self.avg_button, 'Average')
        # self.avg_button.on_clicked(self.average_plot)



        # init hardware
        self.D = Driver.driver()

        # self.initial_plot()
        # plt.show()

    def initial_plot(self):
        Ex, Ey = self.D.Ex, self.D.Ey
        line, = self.ax.plot(Ex, Ey, lw=2, color='black')
        self.lines.append(line)

    def update_plot(self):
        
        t = np.linspace(0, 2*np.pi, 180)
        Ex, Ey = self.D.Ex , self.D.Ey 
        Ex = Ex.real * np.cos(t) - Ex.imag * np.sin(t)
        Ey = Ey.real * np.cos(t) - Ey.imag * np.sin(t)
        for line in self.lines:
            color = np.array(mcolors.to_rgba(line.get_color()))
            color[-1] *= .5
            line.set_color(color)
        
        new_line, = self.ax.plot(Ex, Ey, lw=2, color='black')
        self.lines.append(new_line)

        self.fig.canvas.draw_idle()
        
    def average_plot(self):
        if not self.lines:
            return
        
        # Initialize lists to store all x and y data points
        all_x_data = []
        all_y_data = []
        
        # Collect all x and y data points from the lines
        for line in self.lines:
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            all_x_data.append(x_data)
            all_y_data.append(y_data)
        
        # Convert to numpy arrays for easier manipulation
        all_x_data = np.array(all_x_data)
        all_y_data = np.array(all_y_data)
        
        # Calculate the average x and y values
        avg_x = np.mean(all_x_data, axis=0)
        avg_y = np.mean(all_y_data, axis=0)
        
        # Clear the plot
        self.clear_plot()
        
        # Plot the average line as a regular line
        avg_line, = self.ax.plot(avg_x, avg_y, color='red')
        
        # Add the average line to the list of lines
        self.lines.append(avg_line)
        
        # Redraw the canvas
        self.fig.canvas.draw_idle()

        


    def clear_plot(self):
        while self.lines:
            line = self.lines.pop()
            line.remove()
        # Redraw the canvas
        self.fig.canvas.draw_idle()

    def getData(self):
        self.D.collect_data()
        self.D.analyze_data()

        return self.D.jones_vector

    def plot_polarization(self, Ex, Ey):
            
        # thetas = np.rad2deg(thetas)
        Ex = Ex
        Ey = Ey
        t = np.linspace(0, 2*np.pi, 180)

        Ex = Ex.real * np.cos(t) - Ex.imag * np.sin(t)
        Ey = Ey.real * np.cos(t) - Ey.imag * np.sin(t)

        self.fig, self.ax = plt.subplots(1, 1, figsize=(5,3))

        self.ax.plot(Ex, Ey)
        self.ax.set_title(f'polarization')
        plt.show()
        
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