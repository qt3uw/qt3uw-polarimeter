from Visualization import PolarimeterVisualization
from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np
import time
import Plotting as t
import RetardanceModel as rm

class driver:
    def __init__(self):
        self.p = Polarimeter(14,14,14,11400540)
        self.p.InitializeHardware()
    
    def collect_data(self):  
        # p.MeasureLaserFluctuation()
        self.p.runPolarimeter()
        self.data = self.p.data
    # Polarimeter
    
    def analyze_data(self):
        da = PolarimeterAnalysis(self.data)
        da.extract_stokes()
        da.Stokes2Efield()
        self.Stokes = [da.S0,da.S1,da.S2,da.S3]
        self.jones_vector = da.stokes_to_jones(self.Stokes)
        print(self.jones_vector)
        # t.plot_polarization(0,jones_vector)
    
    
    #gets Jones Vector 
    

    # Plots Polarization state over time
    
    # rm.main()



    # vector = 1/np.sqrt(2) * np.array([1j, 1])
    # pv = PolarimeterVisualization(jones_vector)  
    # pv.pointSetup()
    # pv.plotSetup()
    # pv.animate()