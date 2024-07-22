from Visualization import PolarimeterVisualization
from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np
import time
import troubleshooter as t
import RetardanceModel as rm

# runs polarimeter, collects and stores data
p = Polarimeter(14,14,14,11400540)
p.InitializeHardware()
# p.MeasureLaserFluctuation()
p.runPolarimeter()
data = p.data
# Polarimeter
da = PolarimeterAnalysis(data)
da.extract_stokes()
da.Stokes2Efield()

Stokes = [da.S0,da.S1,da.S2,da.S3]

#gets Jones Vector 
jones_vector = da.stokes_to_jones(Stokes)

print(jones_vector)
print()
# Plots Polarization state over time
t.plot_polarization(0,jones_vector)
# rm.main()



# vector = 1/np.sqrt(2) * np.array([1j, 1])
# pv = PolarimeterVisualization(jones_vector)  
# pv.pointSetup()
# pv.plotSetup()
# pv.animate()