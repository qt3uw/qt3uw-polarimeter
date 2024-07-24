# from Visualization import PolarimeterVisualization
# from polarimeter import Polarimeter
# from DataAnalysis import PolarimeterAnalysis
import numpy as np
# import time
# import matplotlib.pyplot as plt

# class tester:
#     def __init__(self):
#         self.data = None
#     def init_hardware(self):
#         self.p = Polarimeter(14,14,14,11400540)
#         self.p.InitializeHardware()

#     def run_p(self):
#         # p.MeasureLaserFluctuation()
#         self.p.runPolarimeter()
#         self.data = self.p.data
#         print(f"photodiode data {self.data}")
#         # print(p.theta)
#         da = PolarimeterAnalysis(self.data)
#         # print(len(self.data))
#         da.extract_stokes()
#         da.Stokes2Efield()
#         vector = da.eField
#         Stokes = [da.S0,da.S1,da.S2,da.S3]
#         print(f"Stokes Paramaters {Stokes}")
#         print(f"X component {da.Ex}")
#         print(f"Y component {da.Ey}")
#         print(f"eField vector {vector}")

#     def measurelaser(self):
#         self.p.MeasureLaserFluctuation()

    
#     def DA(self):
#         da = PolarimeterAnalysis(self.data)
#         print(len(self.data))
#         da.extract_stokes()
#         da.Stokes2Efield()
#         vector = da.eField
#         Stokes = [da.S0,da.S1,da.S2,da.S3]
#         print(Stokes)
#         print(da.Ex)
#         print(da.Ey)
#         print(vector)
    
#     # Animation driver code
    
#     # vector = 1/np.sqrt(2) * np.array([1j, 1])
#     # pv = PolarimeterVisualization(vector)
#     # pv.pointSetup()
#     # pv.plotSetup()
#     # pv.animate()

# a, l = np.average([20.01800180018002, 20.0, 20.036003600360036, 20.09000900090009, 19.981998199819984, 20.054005400540056]), np.std([[20.01800180018002, 20.0, 20.036003600360036, 20.09000900090009, 19.981998199819984, 20.054005400540056]])
# print(f"calibrated polarizer angle: {a}") ; print(f"std: {l}")

# calibrated polarizer angle: 20.030003000300027
# std: 0.035500028701467394

d, x = np.average([71.5031503150315 , 71.53015301530154 , 71.57515751575157 , 71.58415841584159 , 71.52115211521152 , 71.62016201620162]) , np.std([71.5031503150315 , 71.53015301530154 , 71.57515751575157 , 71.58415841584159 , 71.52115211521152 , 71.62016201620162])
print(f"calibrated qwp angle: {d}") ; print(f'std: {x}')

# calibrated qwp angle: 71.55565556555656
# std: 0.04072568845033806