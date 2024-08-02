import numpy as np
from thorlabs_elliptec import ELLx, ELLError, ELLStatus, list_devices
import redpitaya_scpi as scpi
import time
from polarimeter import Polarimeter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

#Inherits the Polarimeter class to reduce 
#redundancy 
class calibration(Polarimeter):
    def __init__(self):
        super().__init__(14,11400938,14,11400540)
        super().InitializeHardware()
        pass
    
    def polarizerCalibrationModel(self, alpha, delta, constant, beta):
        return (constant*(np.cos(alpha - delta)**2)) + beta
    
    def qwpCalibrationModel(self, alpha, omega, beta, chi, delta):
        return omega * np.cos((2*alpha - beta) + delta)**2 + chi

    def polarizerCalibrationNoCube(self):
        self.measurementParameters(180,"pol")
        self.analyzePolData(10)
        positions1 , voltages1 = self.takeData()
        input("Press enter when you are ready")
        positions2 , voltages2 = self.takeData()

    def polarizereCalibration(self):
        self.measurementParameters("pol")
        self.takeData()
        self.analyzePolData()
    
    def qwpCalibration(self):
        self.measurementParameters("qwp")
        self.takeData()
        self.analyzeQwpData()
        




    def testfunction(self):
        print("no errors!!!")


    def takeData(self):
        self.Voltages = []
        self.actual_positions = []
        for _ in range(self.data_points):
            self.actual_positions.append(self.qwp_stage.get_position())
            raw_data = super().getData(self.rotation_interval)
            data = super()._formatRpData(raw_data)
            data = np.average(data)
            self.Voltages.append(data)
        return self.actual_positions, self.Voltages
    
####### DRIVER #######
    def analyzePolData(self):
        popt, pcov = curve_fit(self.polarizerCalibrationModel, np.deg2rad(self.actual_positions), self.Voltages)
        optimized_delta, optimized_constant, optimized_beta = popt
        cov_constant, cov_delta, cov_beta = np.sqrt(np.diag(pcov))

        # table_text = f"""
        # Optimized Parameters:
        # Constant: {optimized_constant:.2e} ± {cov_constant:.2e}
        # Delta: {optimized_delta:.2e} ± {cov_delta:.2e}
        # Beta: {optimized_beta:.2e} ± {cov_beta:.2e}
        # """
        # plt.text(0.5, 1.075 ,table_text,transform=plt.gca().transAxes, fontsize=6,
        #     verticalalignment='center', bbox=dict(boxstyle="round,pad=0.2", edgecolor='black', facecolor='white'))


        model_angles = np.deg2rad(np.linspace(0,180,10000))
        model_values = self.polarizerCalibrationModel(model_angles, optimized_delta,  optimized_constant, optimized_beta)

        plt.figure(figsize=(10,6))
        plt.scatter(self.actual_positions, self.Voltages, color = 'g', label = 'raw data')
        plt.plot(np.rad2deg(model_angles), model_values, label = 'fitted data')
        plt.legend()
        plt.show()

        max_index = np.argmax(model_values)
        max_angle = model_angles[max_index] 
        print(np.rad2deg(max_angle))

     
    def analyzeQwpData(self): 
        popt, pcov = curve_fit(self.qwpCalibrationModel, np.deg2rad(self.actual_positions), self.Voltages)
        optimized_omega, optimized_beta, optimized_chi, optimized_delta = popt

        model_angles = np.deg2rad(np.linspace(0,90,10000))
        model_values = self.qwpCalibrationModel(model_angles, optimized_omega, optimized_beta, optimized_chi, optimized_delta)

        max_index = np.argmax(model_values)
        max_angle = model_angles[max_index] 
        print((np.rad2deg(max_angle)))


        plt.figure(figsize=(10,6))
        plt.scatter(self.actual_positions, self.Voltages, label = 'raw data')
        plt.plot(np.rad2deg(model_angles), model_values, label = 'fitted curve', color = 'purple')
        plt.plot()
        plt.legend()
        plt.show()






    def measurementParameters(self, optic):
        if optic == "pol":
            self.data_points = 200
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 180/self.data_points
        if optic == "qwp":
            self.data_points = 100
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 90/self.data_points
        





if __name__ == "__main__":
    g = calibration()
    g.testfunction()
    # g.polarizereCalibration()
    g.qwpCalibration()
