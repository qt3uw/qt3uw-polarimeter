import numpy as np 
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

class PolarimeterVisualization:
    def __init__(self, input_vector):
        self.input_vector = input_vector
        self.fontsize = None
        self.axesLineWidth = None
        self.FPS = None
        self.LIM = None
        self.aspect_ratio = None
        self.state = None

        self.pointsPerPeriod = None
        self.periodsPerState = None
        self.visualPeriods = None
        self.pointsPerview = None
        self.waveVector = None
        self.totalPoints = None

        self.z = None
        self.eField = None

    
    def pointSetup(self):
        self.fontsize = 18
        self.axesLineWidth = 3
        self.FPS = 16
        self.LIM = 1.5
        self.aspect_ratio = 3
        
        self.pointsPerPeriod = 24
        self.periodsPerState = 5
        self.visualPeriods = 5
        self.pointsPerview = (self.visualPeriods * self.pointsPerPeriod)
        self.waveVector = 2 * np.pi / self.pointsPerPeriod
        self.totalPoints = self.pointsPerPeriod * self.periodsPerState + self.pointsPerview
        self.z = np.linspace(0, self.totalPoints, self.totalPoints)

        self.eField = np.zeros(shape=(self.totalPoints, 2), dtype=complex)
        self.eField[:] = self.input_vector
       
        # applies a filter to smoothen animation when it repeats
        b, a = signal.butter(N=2, Wn=0.1) 
        self.efield = signal.filtfilt(b, a, self.eField, axis = 0)

        self.xs = np.real(self.eField[:, 0] * np.exp(1j * (self.waveVector * self.z)))
        self.ys = np.real(self.eField[:, 1] * np.exp(1j * (self.waveVector * self.z)))


    def plotSetup(self):
        self.fig = plt.figure(figsize = (7,7))
        self.ax = self.fig.add_subplot(111, projection = '3d')
        self.thislw = 3
        self.qw = 2

        self.xcurve, = self.ax.plot([], [], [], color="tab:orange", lw=self.thislw, alpha=0.4)
        self.ycurve, = self.ax.plot([], [], [], color="tab:orange", lw=self.thislw, alpha=0.4)
        self.xycurve, = self.ax.plot([], [], [], color="tab:orange", lw=self.thislw, alpha=0.4)
        self.curve, = self.ax.plot([], [], [], color="tab:blue", lw=self.thislw)
        self.quiver = self.ax.quiver([], [], [], [], [], [], lw=self.qw, alpha=0.2)
        self.title = self.ax.set_title("")

        self.ax.set_box_aspect((1, 1, self.aspect_ratio))
        self.ax.set(xlabel="x", ylabel="y", zlabel="z")
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_zticks([])
        self.ax.set_xlim([-self.LIM, self.LIM])
        self.ax.set_ylim([-self.LIM, self.LIM])
        self.ax.set_zlim(0, self.z[self.pointsPerPeriod])

    def update(self, iframe):
        i,frame = iframe
        self.title.set_text("Polarization")

        _x = self.xs[frame:frame + self.pointsPerview]
        _y = self.ys[frame:frame + self.pointsPerview]
        _z = self.z[:self.pointsPerview]  # 

        self.xcurve.set_data_3d(_x, np.full_like(_x,2), _z)
        self.ycurve.set_data_3d(np.full_like(_y,-2), _y, _z)
        self.xycurve.set_data_3d(_x[:self.pointsPerPeriod], _y[:self.pointsPerPeriod], np.full_like(_y[:self.pointsPerPeriod], 0))
        self.curve.set_data_3d(_x,_y,_z)

        self.quiver.set_segments([np.array([[0, 0, self.z[i-frame]],[self.xs[i], self.ys[i], self.z[i] - frame]])for i in range(frame, frame+self.pointsPerview, 1)])

    def animate(self):
        ani = FuncAnimation(self.fig, self.update, interval = 1000 / self.FPS, frames = enumerate(np.arange(self.totalPoints - self.pointsPerview -1, 0, -1)), repeat = True, blit = False, cache_frame_data = False)
        plt.show()

        

