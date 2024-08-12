import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib import colors as mcolors

class plotting:
    def __init__(self):
        # Initialize fig and ax
        self.fig, self.ax = plt.subplots(1, 1, figsize=(5,2.75))        
        self.ax.set_title(("Polarization"))
        self.ax.set_xlabel('E_x (a.u)')
        self.ax.set_ylabel('E_y (a.u)')
        self.ax.axhline(0, color='gray', lw=0.5)
        self.ax.axvline(0, color='gray', lw=0.5)
        self.ax.grid(True)
        self.ax.axis('equal')
        plt.tight_layout()
        
        # Initialize list of lines for plotting 
        self.lines = []

    # Updates plot with current data
    def update_plot(self, input_Ex, input_Ey):
        
        t = np.linspace(0, 2*np.pi, 180)
        Ex, Ey = input_Ex , input_Ey 
        Ex = Ex.real * np.cos(t) - Ex.imag * np.sin(t)
        Ey = Ey.real * np.cos(t) - Ey.imag * np.sin(t)
        
        # gray scale effect
        for line in self.lines:
            color = np.array(mcolors.to_rgba(line.get_color()))
            color[-1] *= .5
            line.set_color(color)
        
        new_line, = self.ax.plot(Ex, Ey, lw=2, color='black')
        self.lines.append(new_line)

        self.fig.canvas.draw_idle()
    
    # Plots average components of all lines
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
        #     change to if instead of while to only clear last line
        #     if self.lines: 
        while self.lines:
            line = self.lines.pop()
            line.remove()
        # Redraw the canvas
        self.fig.canvas.draw_idle()
        
    def show(self):
        plt.show()
