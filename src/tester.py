from Visualization import PolarimeterVisualization
from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np
import time

p = Polarimeter(14,14,14,11400540)
p.InitializeHardware()
p.runPolarimeter()
data = p.data
time.sleep(1)
p.MeasureLaserFluctuation()

da = PolarimeterAnalysis(data)
da.extract_stokes()
da.Stokes2Efield()
vector = da.eField
Stokes = [da.S0,da.S1,da.S2,da.S3]
print(Stokes)
print(vector)
# vector = 1/np.sqrt(2) * np.array([1j, 1])
pv = PolarimeterVisualization(vector)
pv.pointSetup()
pv.plotSetup()
pv.animate()