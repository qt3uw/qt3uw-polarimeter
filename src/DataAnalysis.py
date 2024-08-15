import numpy as np
import scipy as sp
from py_pol.jones_vector import Jones_vector, create_Jones_vectors
from py_pol.stokes import Stokes

class PolarimeterAnalysis:
    def __init__(self):
        init = "init"



    def extract_stokes(self, input_data, number_of_angles):
        
        # creates corresponding array of angles with
        #
        #  respect to number of angles input
        angles = np.deg2rad(np.linspace(0,180 - 180/number_of_angles, number_of_angles))
        
        # Fourier Coefficients Computation 
        A = (2/number_of_angles) * np.sum(input_data)
        B = (4/number_of_angles) * np.sum(input_data * np.sin(2 * angles))
        C = (4/number_of_angles) * np.sum(input_data * np.cos(4 * angles))
        D = (4/number_of_angles) * np.sum(input_data * np.sin(4 * angles))

        # Stoke Parameter Computation
        self.S0 = A - C
        self.S1 = 2 * C
        self.S2 = 2 * D
        self.S3 = B

        # Normalize Stokes Parameters
        self.S1 = self.S1/self.S0
        self.S2 = self.S2/self.S0
        self.S3 = self.S3/self.S0
        self.S0 = self.S0/self.S0

    # ThorLabs Video Computations

    def Stokes2Efield(self):
        self.azimuth = .5 * np.arctan(self.S2/self.S1)
        self.elipticity = .5 * np.arcsin(self.S3)
        self.Ex = np.sqrt(.5 * (self.S0 + self.S1))
        self.Ey = np.sqrt(.5 * (self.S0 - self.S1))
        self.eField = [self.Ex, self.Ey]
    

    # Stokes to Jones manually 
    def stokes_to_jones(self, S):
        # Calculate the degree of polarization, not really necessary
        # but can serve to check error 
        p = np.sqrt(S[1]**2 + S[2]**2 + S[3]**2) / S[0]
        
        # Calculate the Jones vector components
        A = np.sqrt((1 + S[1]) / 2)
        if A == 0:
            B = 1  # B is set to 1 if A is zero to avoid division by zero
        else:
            B = (S[2] / (2 * A)) - 1j * (S[3] / (2 * A))  # Ensure B remains a scalar when A is not zero
        
        # Combine them into a vector with the amplitude of the polarized part
        Jv = np.sqrt(S[0] * p) * np.array([A, B], dtype=complex)  
        self.azimuth = 0.5 * np.arctan(self.S2/self.S1)
        print(f"Azimuth angle = {np.rad2deg(self.azimuth):.3f} Degrees")
        print(f"Jones Vector: {Jv[0]:.3f} , {Jv[1]:.3f}")
        print(f"Degree of Polarization: {p:.3f}")
        
        return Jv
