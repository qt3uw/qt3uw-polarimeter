from thorlabs_elliptec import ELLx
import redpitaya_scpi as scpi
import time
import numpy as np

class PhotodiodeOversaturationError(Exception):
   pass
class Polarimeter:
   def __init__(self, pol_stage, pol_serial, qwp_stage, qwp_serial):
      self.p_stage_model = pol_stage
      self.p_stage_serialnumber = pol_serial
      self.qwp_stage_model = qwp_stage 
      self.qwp_stage_serialnumber = qwp_serial
      self.n_angles = 200
      self.pstage = None

      self.data = None
      self.theta = 180/self.n_angles
      
   

   # Initializes hardware components to get ready for
   # data acquisition, must run before running polarimeter
   def InitializeHardware(self):
      self.qwp_stage = ELLx(x = self.qwp_stage_model, device_serial = self.qwp_stage_serialnumber)
      self.qwp_stage.home()
      self.qwp_stage.move_relative(71.55565556555656, blocking = True)
      self.redpitaya = scpi.scpi('128.95.31.27')
   
   #  Parses, and Stores Data

   def _formatRpData(self, raw_data):
      raw_data = raw_data.replace("{", " ").replace("}", "")
      raw_data = raw_data.replace("VOLTS\r\n ","         ")
      raw_data = raw_data.split(",")
      
      raw_data_list = []

      for data in raw_data:
         float_data = float(data)
         raw_data_list.append(float_data)
      
      
      
      return raw_data_list

   def getData(self,theta):
      self.redpitaya.tx_txt('ACQ:RST')
      self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
      self.redpitaya.tx_txt('ACQ:SOUR1:GAIN HV')
      self.redpitaya.tx_txt('ACQ:DEC 1')
      self.redpitaya.tx_txt('ACQ:START')
      time.sleep(.2)
      self.redpitaya.tx_txt('ACQ:STOP')
      self.qwp_stage.move_relative(theta)
      self.raw_data = self.redpitaya.acq_data(1)
      return self.raw_data
   
   def runPolarimeter(self, n_angles):
      self.data = []
      for i in range (n_angles):
         # data acquisition
         self.getData(180/n_angles)

         # Formats data for processing
         data = self._formatRpData(self.raw_data)
         for item in data:
            self.check_for_oversaturation(item)
            
         data = np.average(data)

         self.data.append(data)
      # self.qwp_stage.home(blocking=True)
      time.sleep(0.2)
      self.qwp_stage.home(blocking = True)
      self.qwp_stage.move_absolute(71.556, blocking=True)
   
   def testfunction(self):
      print("Your inheritance is working")

   def check_for_oversaturation(self,output_voltage):
      if output_voltage >= 10.0:
         raise PhotodiodeOversaturationError(f"Photodiode signal is oversaturated")

   def MeasureLaserFluctuation(self):
      # Takes data at a fixed position 
      # and prints the range of fluctuation
      # As a percentage
      self.redpitaya.tx_txt('ACQ:RST')
      self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
      self.redpitaya.tx_txt('ACQ:DEC 1')
      self.redpitaya.tx_txt('ACQ:START')
      time.sleep(5)
      self.redpitaya.tx_txt('ACQ:STOP')

      raw_data = self.redpitaya.acq_data(1)

      data = self._formatRpData(raw_data)
      max = np.max(data)
      min = np.min(data)

      range = max - min

      data = np.average(data)

      fluctuation = range/data
      fluctuation = "{:.2%}".format(fluctuation)
      print(f"Your laser is fluctuating by: {fluctuation}")



           
   

      
