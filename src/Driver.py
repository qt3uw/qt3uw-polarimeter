from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np
from Plotting import plotting

class driver(Polarimeter, PolarimeterAnalysis, plotting):
    def __init__(self):
        Polarimeter.__init__(self,14,11400938,14,11400540)
        PolarimeterAnalysis.__init__(self)
        plotting.__init__(self)
        
    # Drives the polarimeter, collects data, formats, analyzes,
    # and creates jone vector 
    def main(self):
        number_of_increments = 120
        self.runPolarimeter(number_of_increments)
        self.extract_stokes(self.data, number_of_increments)
        self.Stokes = [self.S0, self.S1, self.S2, self.S3]
        self.jones_vector = self.stokes_to_jones(self.Stokes)
        self.Ex, self.Ey = self.jones_vector[0], self.jones_vector[1]