import numpy as np
from thorlabs_elliptec import ELLx, ELLError, ELLStatus, list_devices
import redpitaya_scpi as scpi
import time
from polarimeter import Polarimeter
from scipy.optimize import curve_fit

#Inherits the Polarimeter class to reduce 
#redundancy 
class calibration(Polarimeter):
    def __init__(self):
        super().__init__(14,14,14,11400540)
    
    def polarizerCalibrationModel(self, alpha, delta, constant, beta):
        return (constant*(np.cos(alpha - delta)**2)) + beta
    
    def qwpCalibrationModel(self, alpha, beta, chi ,delta ):
        return alpha * np.sin((2 * alpha - beta) + delta )**2 + chi

    def polarizerCalibration(self):
        self.measurementParameters(180,"pol")
        self.analyzePolData(10)


    def testfunction(self):
        print("no errors!!!")


    def runHardware(self, data_points):
        Voltages = []
        actual_positions = []

        for _ in range(data_points+1):

            position = (self.p_stage_model.get_position())

    

    def analyzePolData(self, data):
        data = data




    def measurementParameters(self, theta, optic):
        if optic == "qwp":
            data_points = 200
        if optic == "pol":
            data_points = 100
        
        self.rotation_interval = theta/data_points





if __name__ == "__main__":
    g = calibration()
    g.testfunction()
