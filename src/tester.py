from Visualization import PolarimeterVisualization
from polarimeter import Polarimeter
from DataAnalysis import PolarimeterAnalysis
import numpy as np

p = Polarimeter(14,14,14,11400540)
p.InitializeHardware()
p.runPolarimeter()
data = p.data

da = PolarimeterAnalysis(data)
da.extract_stokes()
da.Stokes2Jones()
vector = da.jones
# vector = 1/np.sqrt(2) * np.array([1j, 1])
pv = PolarimeterVisualization(vector)
pv.pointSetup()
pv.plotSetup()
pv.animate()