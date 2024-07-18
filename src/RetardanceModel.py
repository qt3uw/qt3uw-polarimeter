import numpy as np
import matplotlib.pyplot as plt

def waveplate_matrix(retardance_waves, theta):
    """ Return the Jones matrix for a wave plate with given retardance (in waves) and orientation angle theta. """
    delta = retardance_waves * 2 * np.pi  # Convert waves to radians
    theta = np.radians(theta)
    cos2 = np.cos(theta)**2
    sin2 = np.sin(theta)**2
    sin2cos2 = np.sin(2 * theta) / 2
    return np.array([
        [cos2 + np.exp(1j * delta) * sin2, (1 - np.exp(1j * delta)) * sin2cos2],
        [(1 - np.exp(1j * delta)) * sin2cos2, sin2 + np.exp(1j * delta) * cos2]
    ])

def polarization_ellipse(retardance_waves, input_angle, waveplate_angle):
    """ Return the electric field components over time """
    E0x = np.cos(np.radians(input_angle))
    E0y = np.sin(np.radians(input_angle))
    E_in = np.array([E0x, E0y], dtype=complex)
    
    # Get wave plate matrix
    wp_matrix = waveplate_matrix(retardance_waves, waveplate_angle)
    
    # Apply wave plate matrix to input field
    E_out = np.dot(wp_matrix, E_in)
    
    # Time array for one period
    t = np.linspace(0, 2 * np.pi, 100)
    
    # Calculate electric field components over time
    Ex = E_out[0].real * np.cos(t) - E_out[0].imag * np.sin(t)
    Ey = E_out[1].real * np.cos(t) - E_out[1].imag * np.sin(t)
    
    return Ex, Ey

def plot_polarization_ellipse(retardance_waves, input_angle, waveplate_angles, ax):
    """ Plot polarization ellipse for different waveplate angles. """
    for waveplate_angle in waveplate_angles:
        Ex, Ey = polarization_ellipse(retardance_waves, input_angle, waveplate_angle)
        ax.plot(Ex, Ey, label=f'{waveplate_angle}°')
    
    ax.set_title(f'Retardance at my Wavelength (635nm)')
    ax.set_xlabel('E_x')
    ax.set_ylabel('E_y')
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.grid(True)
    ax.axis('equal')
    ax.legend()

def main():
    effective_retardance_waves = 0.325  # arbitrary waves

    input_angle = 0  # Horizontally polarized light
    waveplate_angles = [0, 22.5, 45, 67.5, 90]  # Rotation angles of the waveplate

    fig, ax = plt.subplots(figsize=(10, 5))
    plot_polarization_ellipse(effective_retardance_waves, input_angle, waveplate_angles, ax)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
