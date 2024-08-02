import numpy as np
import scipy as sp
from py_pol.jones_vector import Jones_vector, create_Jones_vectors
from py_pol.stokes import Stokes

class PolarimeterAnalysis:
    def __init__(self, input_data):
        self.jones = None
        self.input_data = input_data
        self.data_length = None
        self.S0 = None
        self.S1 = None
        self.S2 = None
        self.S3 = None


    def extract_stokes(self):
        angles = np.deg2rad(np.linspace(0,180 - 180/15,15))
        data_length = len(self.input_data)
        # Fourier Coefficients Computation 
        print(f"list of angles {np.rad2deg(angles)}")
        # print(f"data length = {data_length}")
        A = (2/data_length) * np.sum(self.input_data)
        B = (4/data_length) * np.sum(self.input_data * np.sin(2 * angles))
        C = (4/data_length) * np.sum(self.input_data * np.cos(4 * angles))
        D = (4/data_length) * np.sum(self.input_data * np.sin(4 * angles))

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

    # Takes in Stokes and comptues Efield and 
    # other componenets
    def Stokes2Efield(self):
        self.azimuth = .5 * np.arctan(self.S2/self.S1)
        self.elipticity = .5 * np.arcsin(self.S3)
        self.Ex = np.sqrt(.5 * (self.S0 + self.S1))
        self.Ey = np.sqrt(.5 * (self.S0 - self.S1))
        self.eField = [self.Ex, self.Ey]
    


    # # Alternative test computations
    # def extract_stokestwo(self):
    #     angles = np.linspace(0,np.deg2rad(180 - 180/12), 12)
    #     N = len(self.input_data)
        
    #     # Fourier Coefficients
    #     A0 = (2 / N) * (np.sum(self.input_data))
    #     A2 = (4 / N) * (np.sum(self.input_data * np.cos(2 * angles)))
    #     A4 = (4 / N) * (np.sum(self.input_data * np.cos(4 * angles)))

    #     # Calculate Stokes Parameters
    #     S0 = A0 - A4
    #     S1 = 2 * A4
    #     S2 = 2 * A2
    #     S3 = A2

    #     # Normalize Stokes Parameters
    #     S0_norm = 1
    #     S1_norm = S1 / S0
    #     S2_norm = S2 / S0
    #     S3_norm = S3 / S0

    #     # Calculate Polarization Parameters
    #     psi = 0.5 * np.arctan2(S2, S1)
    #     epsilon = 0.5 * np.arcsin(S3 / S0)

    #     self.Ex = np.sqrt((S0_norm + S1_norm) / 2 + 0j)
    #     self.Ey = np.sqrt((S0_norm - S1_norm) / 2 + 0j)

    #     # Calculate phase difference
    #     delta = np.arctan2(S3, S2)
    #     self.eFieldvector = np.array([self.Ex, self.Ey * np.exp(1j * delta)])

    
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
        # print(p)
        return Jv

    # # Takes in Stokes parameters as a list 
    # def StokestoJonesTwo(self, S):
    #     E = Jones_vector("Source 1")
    #     print("is this even working")
    #     stokes = Stokes().from_components(S)
    #     self.jv = E.from_Stokes(stokes)
    #     print(self.jv)
    #     # return self.jv
