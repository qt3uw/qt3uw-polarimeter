from thorlabs_elliptec import ELLx
import redpitaya_scpi as scpi
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
class PhotodiodeOversaturationError(Exception):
   pass
class Polarimeter:
   def __init__(self, pol_stage, pol_serial, qwp_stage, qwp_serial):
      self.p_stage_model = pol_stage
      self.p_stage_serialnumber = pol_serial
      self.qwp_stage_model = qwp_stage 
      self.qwp_stage_serialnumber = qwp_serial   
      self.qwp_calibrated_angle = 69.56795679567956
   

   def InitializeHardware(self):
      self.qwp_stage = ELLx(x = self.qwp_stage_model, device_serial = self.qwp_stage_serialnumber)
      self.qwp_stage.home()
      self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking = True)
      self.redpitaya = scpi.scpi('128.95.31.27')
   
   
   def adjustPolarizermount(self, angle):
      pass
      
   # Parses and stores raw data 
   def _formatRpData(self, raw_data):
      raw_data = raw_data.replace("{", " ").replace("}", "")
      raw_data = raw_data.replace("VOLTS\r\n ","         ")
      raw_data = raw_data.split(",")
      
      raw_data_list = []

      for data in raw_data:
         float_data = float(data)
         raw_data_list.append(float_data)
      
      
      
      return raw_data_list

   # Data acquisition 
   def getData(self,theta):
      self.redpitaya.tx_txt('ACQ:RST')
      self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
      self.redpitaya.tx_txt('ACQ:SOUR1:GAIN HV')
      self.redpitaya.tx_txt('ACQ:DEC 1')
      self.redpitaya.tx_txt('ACQ:START')
      self.redpitaya.tx_txt('ACQ:STOP')
      self.qwp_stage.move_relative(theta)
      self.raw_data = self.redpitaya.acq_data(1)
   
   # Main driver code for polarimeter
   def runPolarimeter(self, n_angles):
      self.data = []

      for i in range (int(n_angles)):
         # data acquisition
         rotation_angle = 180/n_angles
         self.getData(rotation_angle)

         # Formats data for processing
         data = self._formatRpData(self.raw_data)
         
         # checks for values above oversaturation
         # threshold (10 Volts)
         for item in data:
            self.check_for_oversaturation(item)
         
         # Takes average of data at respective angle
         data = np.average(data)

         self.data.append(data)
      
      
      # Returns qwp back to calibrated position
      time.sleep(0.2) # Timer helps reduce risk of mechanical timeout
      self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking=True)
   

   def check_for_oversaturation(self,output_voltage):
      if output_voltage >= 10.0:
         raise PhotodiodeOversaturationError(f"Photodiode signal is oversaturated")

   def MeasureLaserFluctuation(self):
      # Takes data at a fixed position 
      # and prints the range of fluctuation
      # as a percentage
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


   #############################################################################
   ########################      CALIBRATION      ##############################
   #############################################################################

   def polarizerCalibrationModel(self, alpha, delta, constant, beta):
        return (constant*(np.cos(alpha - delta)**2)) + beta
    
    
   def qwpCalibrationModel(self, alpha, omega, beta, chi, delta):
        return omega * np.cos((2*alpha - beta) + delta)**2 + chi


   def polarizereCalibration(self):
        self.measurementParameters("pol")
        self.takeCalibrationData()
        self.analyzePolData()

    
   def qwpCalibration(self):
        self.measurementParameters("qwp")
        self.takeCalibrationData()
        self.analyzeQwpData()
   

   def measurementParameters(self, optic):
        if optic == "pol":
            self.data_points = 200
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 180/self.data_points
        if optic == "qwp":
            self.data_points = 100
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 90/self.data_points


   def takeCalibrationData(self):
        self.Voltages = []
        self.actual_positions = []
        for _ in range(self.data_points):
            self.actual_positions.append(self.qwp_stage.get_position())
            raw_data = self.getData(self.rotation_interval)
            data = self._formatRpData(raw_data)
            data = np.average(data)
            self.Voltages.append(data)
        return self.actual_positions, self.Voltages
    

   def analyzePolData(self):
        popt, pcov = curve_fit(self.polarizerCalibrationModel, np.deg2rad(self.actual_positions), self.Voltages)
        optimized_delta, optimized_constant, optimized_beta = popt
      
      #   cov_constant, cov_delta, cov_beta = np.sqrt(np.diag(pcov))

      #   table_text = f"""
      #   Optimized Parameters:
      #   Constant: {optimized_constant:.2e} ± {cov_constant:.2e}
      #   Delta: {optimized_delta:.2e} ± {cov_delta:.2e}
      #   Beta: {optimized_beta:.2e} ± {cov_beta:.2e}
      #   """
      #   plt.text(0.5, 1.075 ,table_text,transform=plt.gca().transAxes, fontsize=6,
      #       verticalalignment='center', bbox=dict(boxstyle="round,pad=0.2", edgecolor='black', facecolor='white'))


        model_angles = np.deg2rad(np.linspace(0,180,10000))
        model_values = self.polarizerCalibrationModel(model_angles, optimized_delta,  optimized_constant, optimized_beta)

        plt.figure(figsize=(10,6))
        plt.scatter(self.actual_positions, self.Voltages, color = 'g', label = 'raw data')
        plt.plot(np.rad2deg(model_angles), model_values, label = 'fitted data')
        plt.legend()
        plt.show()

        max_index = np.argmax(model_values)
        max_angle = model_angles[max_index] 
        print(f"Calibrated angle: {np.rad2deg(max_angle):.3f}")

     
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
   
   

           
   

      
