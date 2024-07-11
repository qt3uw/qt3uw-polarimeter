import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.figure import Figure





class guitester:
    def __init__(self):
        self.test = "Hardware has been initalized"
        self.fig = None
        self.ani = None

    def Initialize_hardware(self):
        print(self.test)

    def run_polarimeter(self):
        self.data = np.random.rand(10)
        self.A = "polarimeter succesfully ran"
        print(self.A)
        print(self.data)
    
    def measurerange(self):
        range = (np.max(self.data) - np.min(self.data))/np.average(self.data)
        percent = range*100
        print(f"Fluctuating by {percent}%")

    def visualization(self):
        plt.rcParams["font.size"] = 18
        plt.rcParams["axes.linewidth"] = 3
        self.fig = Figure(figsize=(5,5))

        FPS = 16
        ASPECT = 3
        LIM = 1.5

        states = {
            "Special case 1": 1/np.sqrt(2) * np.array([1j, 1]),
            "Special case 2": 1/np.sqrt(2) * np.array([1, 1])
        }

        Nstates = len(states)
        N_per_period = 24
        N_periods_per_state = 5
        N_periods_per_view = 5

        N_per_view = N_periods_per_view * N_per_period

        k = 2 * np.pi / N_per_period

        N = Nstates * N_per_period * N_periods_per_state + N_per_view

        # Data setup
        z = np.linspace(0, N, N)

        E = np.zeros(shape=(N, 2), dtype=complex)
        pol_state = np.empty(N, dtype=object)

        for i in range(N):
            nstate = (i // (N_per_period * N_periods_per_state)) % Nstates
            pol_state[i] = list(states.keys())[nstate]
            E[i] = states[pol_state[i]]

        b, a = signal.butter(N=2, Wn=0.1)
        E = signal.filtfilt(b, a, E, axis=0)

        xs = np.real(E[:, 0] * np.exp(1j * (k * z)))
        ys = np.real(E[:, 1] * np.exp(1j * (k * z)))
        # Plot setup
        ax = self.fig.add_subplot(111, projection='3d')
        thislw = 3
        qw = 2

        xcurve, = ax.plot([], [], [], color="tab:orange", lw=thislw, alpha=0.4)
        ycurve, = ax.plot([], [], [], color="tab:orange", lw=thislw, alpha=0.4)
        xycurve, = ax.plot([], [], [], color="tab:orange", lw=thislw, alpha=0.4)
        curve, = ax.plot([], [], [], color="tab:blue", lw=thislw)
        quiver = ax.quiver([], [], [], [], [], [], lw=qw, alpha=0.2)
        title = ax.set_title("")

        ax.set_box_aspect((1, 1, ASPECT))
        ax.set(xlabel="x", ylabel="y", zlabel="z")
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        ax.set_xlim([-LIM, LIM])
        ax.set_ylim([-LIM, LIM])
        ax.set_zlim(0, z[N_per_period])

        def update(iframe):
            i,frame = iframe
            if title.get_text() != pol_state[frame]:
                title.set_text(pol_state[frame])
            
            
            _x = xs[frame:frame + N_per_view]
            _y = ys[frame:frame + N_per_view]
            _z = z[:N_per_view]  # Correct length for the z values
            
            xcurve.set_data_3d(_x, np.full_like(_x,2), _z)
            ycurve.set_data_3d(np.full_like(_y,-2), _y, _z)
            xycurve.set_data_3d(_x[:N_per_period], _y[:N_per_period], np.full_like(_y[:N_per_period], 0))
            curve.set_data_3d(_x,_y,_z)

            # quiver.set_segments([])

            quiver.set_segments([np.array([[0, 0, z[i-frame]],[xs[i], ys[i], z[i] - frame]])for i in range(frame, frame+N_per_view, 1)])
            print("Updating frame:", frame)
            return ()

        # Directly pass the generator function to FuncAnimation
        self.ani = FuncAnimation(self.fig, update, interval=1000 / FPS, frames=enumerate(np.arange(N - N_per_view - 1, 0, -1)), repeat=True , blit=False, cache_frame_data=False)
        

    def get_figure(self):
        return self.fig