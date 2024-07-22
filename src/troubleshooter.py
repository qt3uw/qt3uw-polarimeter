import numpy as np
import matplotlib.pyplot as plt


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

def plot_polarization(thetas, vectors):
    # thetas = np.rad2deg(thetas)
    E_out = vectors
    t = np.linspace(0, 2*np.pi, 180)

    if type(vectors) == list:
        for theta, vector in zip(thetas, vectors):
            Ex = E_out[0].real * np.cos(t) - E_out[0].imag * np.sin(t)
            Ey = E_out[1].real * np.cos(t) - E_out[1].imag * np.sin(t)

    else:
        Ex = E_out[0].real * np.cos(t) - E_out[0].imag * np.sin(t)
        Ey = E_out[1].real * np.cos(t) - E_out[1].imag * np.sin(t)

    fig, ax = plt.subplots(1, 1, figsize=(5,3))

    ax.plot(Ex, Ey)
    # ax.set_title(f'QWP at {thetas}°')
    ax.set_title(input("label"))
    ax.set_xlabel('E_x')
    ax.set_ylabel('E_y')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.grid(True)
    ax.axis('equal')
    plt.show()

