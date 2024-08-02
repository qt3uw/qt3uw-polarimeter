from Visualization import PolarimeterVisualization
from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np
import time
import Plotting as t
import RetardanceModel as rm

class driver:
    def __init__(self):
        self.p = Polarimeter(14,11400938,14,11400540)
        # self.p.InitializeHardware()
        self.Ex = None
        self.Ey = None
        # self.p.InitializeHardware()
        # self.random = t.plotting()
        

    def main(self):
        
        self.p.runPolarimeter(15)
        self.data = self.p.data
        da = PolarimeterAnalysis(self.data)
        da.extract_stokes()
        # da.Stokes2Efield()
        self.Stokes = [da.S0,da.S1,da.S2,da.S3]
        self.jones_vector = da.stokes_to_jones(self.Stokes)
        # print(self.jones_vector)
        self.Ex, self.Ey = self.jones_vector[0], self.jones_vector[1]
        # self.random.plot_polarization(Ex, Ey)
        
        

    def collect_data(self):  
        # p.MeasureLaserFluctuation()
        self.p.runPolarimeter(15)
        self.data = self.p.data
    # Polarimeter
    
    def analyze_data(self):
        da = PolarimeterAnalysis(self.data)
        da.extract_stokes()
        # da.Stokes2Efield()
        self.Stokes = [da.S0,da.S1,da.S2,da.S3]
        self.jones_vector = da.stokes_to_jones(self.Stokes)
        print(self.jones_vector)
        Ex, Ey = self.jones_vector[0], self.jones_vector[1]
        # self.random.plot_polarization(Ex, Ey)
        
    
if __name__ == "__main__":
    # d = driver()
    # d.collect_data()
    # d.analyze_data()
    # d.p.MeasureLaserFluctuation()
    #gets Jones Vector 
    

    # Plots Polarization state over time
    
    # rm.main()



    # vector = 1/np.sqrt(2) * np.array([1j, 1])
    pv = PolarimeterVisualization(d.jones_vector)  
    pv.pointSetup()
    pv.plotSetup()
    pv.animate()