import numpy as np
import scipy as sp

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
        angles = np.linspace(0,np.deg2rad(180 - 180/12), 12)
        data_length = len(self.input_data)
        # Fourier Coefficients
        # A, B, C, D = (0,0,0,0)
        A = (2/data_length) * np.sum(self.input_data)
        B = (4/data_length) * np.sum(self.input_data * np.sin(2 * angles))
        C = (4/data_length) * np.sum(self.input_data * np.cos(4 * angles))
        D = (4/data_length) * np.sum(self.input_data * np.sin(4 * angles))
        
        
        
        
        # for i in range(data_length):
        #     A += self.input_data[i]
        #     B += self.input_data[i] * np.sin(2*angles[i])
        #     C += self.input_data[i] * np.cos(4*angles[i])
        #     D += self.input_data[i] * np.sin(4*angles[i])
        
        # A = A*(2/data_length)
        # B = B*(4/data_length)
        # C = C*(4/data_length)
        # D = D*(4/data_length)

        self.S0 = A - C
        self.S1 = 2 * C
        self.S2 = 2 * D
        self.S3 = B

        # Normalize 
        self.S1 = self.S1/self.S0
        self.S2 = self.S2/self.S0
        self.S3 = self.S3/self.S0
        self.S0 = self.S0/self.S0

    def Stokes2Efield(self):
        # self.azimuth = .5 * np.arctan2(self.S2, self.S1)
        # self.elipticity = .5 * np.arcsin(self.S3)
        self.Ex = np.sqrt(.5 * (self.S0 + self.S1 + 0j))
        # self.Ey = np.sqrt(.5 * (self.S0 - self.S1 + 0j))
        self.Ey = np.sqrt(0.5 * (self.S0 - self.S1 + 0j)) * np.exp(1j * self.azimuth)
        self.eField = [self.Ex, self.Ey]

        

