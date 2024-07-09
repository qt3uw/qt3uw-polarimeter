from thorlabs_elliptec import ELLx
import redpitaya_scpi as scpi
import time
import numpy as np

class Polarimeter:
   def __init__(self, p_model, p_serial, qwp_stage, qwp_serial, *args):
      self.p_stage_model = p_model
      self.p_stage_serialnumber = p_serial
      self.qwp_stage_model = qwp_stage 
      self.qwp_stage_serialnumber = qwp_serial
      # self.theta = 22.5
      self.n_angles = 12
      self.pstage = None
      self.redpitaya = None
      self.data = None
      self.theta = 180/self.n_angles

   # future built in calibration 
   # def CalibratePolarizer(self):
   


   # Initializes hardware components to get ready for
   # data acquisition, must run before running polarimeter
   def InitializeHardware(self):
      self.qwp_stage = ELLx(x = self.qwp_stage_model, device_serial = self.qwp_stage_serialnumber)
      self.qwp_stage.home(blocking = True)
      self.qwp_stage.move_relative(62.283, blocking = True)
      self.redpitaya = scpi.scpi('128.95.31.27')
   
   # Collects, Parses, and Stores Data

   def formatRpData(self, raw_data):
      raw_data = raw_data.replace("{", " ").replace("}", "")
      raw_data = raw_data.replace("VOLTS\r\n ","         ")
      raw_data = raw_data.split(",")
      
      raw_data_list = []

      for data in raw_data:
         float_data = float(data)
         raw_data_list.append(float_data)
      
      
      
      return raw_data_list

   def runPolarimeter(self):
      self.data = []
      for i in range (self.n_angles):
         # data acquisition
         self.redpitaya.tx_txt('ACQ:RST')
         self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
         self.redpitaya.tx_txt('ACQ:DEC 1')
         self.redpitaya.tx_txt('ACQ:START')
         time.sleep(.5)
         self.redpitaya.tx_txt('ACQ:STOP')
         self.qwp_stage.move_relative(self.theta)
         time.sleep(.5)
         raw_data = self.redpitaya.acq_data(1)
         
         # converts output from 
         # string to a list of floats
         
         data = self.formatRpData(raw_data)
         data = np.average(data)

         self.data.append(data)
      

   def MeasureLaserFluctuation(self):
      self.redpitaya.tx_txt('ACQ:RST')
      self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
      self.redpitaya.tx_txt('ACQ:DEC 1')
      self.redpitaya.tx_txt('ACQ:START')
      time.sleep(5)
      self.redpitaya.tx_txt('ACQ:STOP')

      raw_data = self.redpitaya.acq_data(1)

      data = self.formatRpData(raw_data)
      max = np.max(data)
      min = np.min(data)

      range = max - min

      data = np.average(data)

      fluctuation = range/data
      fluctuation = "{:.2%}".format(fluctuation)
      print(f"Your laser is fluctuating by: {fluctuation}")



           
   

      
