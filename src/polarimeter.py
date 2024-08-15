from thorlabs_elliptec import ELLx
import redpitaya_scpi as scpi
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import pickle
import os

class PhotodiodeOversaturationError(Exception):
   pass
class Polarimeter:
    def __init__(self, pol_stage, pol_serial, qwp_stage, qwp_serial):
        self.p_stage_model = pol_stage
        self.p_stage_serialnumber = pol_serial
        self.qwp_stage_model = qwp_stage 
        self.qwp_stage_serialnumber = qwp_serial   
        self.qwp_calibrated_angle = self.load_qwp_calibration_angle()
        self.pol_calibrated_angle = self.load_polarizer_calibration_angle()


    def InitializeHardware(self):
        self.close_ports()
        # try:
        #     self.qwp_stage = ELLx(x = self.qwp_stage_model, device_serial = self.qwp_stage_serialnumber, serial_port='COM3')
        #     self.qwp_stage.home(blocking=True)
        #     self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking = True)
        #     print("QWP Mount Successfully initialized")
        # except Exception as L:
        #     print(f"QWP Mount Failed to Connect: {L}")
        
        for _ in range(3):  # Retry up to 3 times
            try:
                self.qwp_stage = ELLx(x=self.qwp_stage_model, device_serial=self.qwp_stage_serialnumber, serial_port='COM3')
                self.qwp_stage.home(blocking=True)
                self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking=True)
                print("QWP Mount Successfully initialized")
                break  # Exit the loop if successful
            except Exception as L:
                print(f"QWP Mount Failed to Connect: {L}")
                if "mechanical timeout" in str(L).lower():
                    print("Retrying QWP Mount Initialization...")
                    self.close_ports()
                else:
                    break
        
        try: 
            self.pol_stage = ELLx(x = self.p_stage_model, device_serial= self.p_stage_serialnumber, serial_port="COM4")
            self.pol_stage.home(blocking=True)
            self.pol_stage.move_absolute(self.pol_calibrated_angle , blocking = True)
            print("Polarizer Mount Succesfully initalized")
        except Exception as L:
            print(f"Polarizer Mount Failed to Connect: {L}")

        try:
            self.redpitaya = scpi.scpi('128.95.31.27')
            print("Red Pitaya Succesfully Connected")
        
        except ConnectionRefusedError as e:
            print(f"Red Pitaya Connection Failed. Ensure secure connection, visit RP-F071C2.LOCAL \nfrom a web browser and run the scpi server. \nError: {e}")
        
        except Exception as e:
            print(f"An unexpected error occured: {e}")


    def close_ports(self):
        try:
            if hasattr(self, 'qwp_stage') and self.qwp_stage:
                self.qwp_stage._port.close()
                time.sleep(0.1)
                # print("QWP Mount Port Closed Successfully")
        except Exception as e:
            print(f"Error closing QWP port: {e}")

        try:
            if hasattr(self, 'pol_stage') and self.pol_stage:
                self.pol_stage._port.close()
                time.sleep(0.1)
                # print("Polarizer Mount Port Closed Successfully")
        except Exception as e:
            print(f"Error closing Polarizer port: {e}")



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
    def getData(self,theta, type = None):
        
        if type is not None:
            mount = self.pol_stage
        
        else:
            mount = self.qwp_stage

        self.redpitaya.tx_txt('ACQ:RST')
        self.redpitaya.tx_txt('ACQ:DATA:UNITS VOLTS')
        self.redpitaya.tx_txt('ACQ:SOUR1:GAIN HV')
        self.redpitaya.tx_txt('ACQ:DEC 1')
        self.redpitaya.tx_txt('ACQ:START')
        time.sleep(.1)
        self.redpitaya.tx_txt('ACQ:STOP')
        
        mount.move_relative(theta)
        self.raw_data = self.redpitaya.acq_data(1)

    # Main driver for polarimeter
    def runPolarimeter(self, n_angles):
        # self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking = True)
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
            
        self.qwp_stage.move_absolute(self.qwp_calibrated_angle, blocking = True)
        
        
        # Returns qwp back to calibrated position
        # Timer helps reduce risk of mechanical timeout


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


    def polarizerCalibration(self):
        self.measurementParameters("pol")
        self.takeCalibrationData("pol")
        calibrated_angle = self.analyzePolData()
        self.update_polarizer_position(calibrated_angle)


    def qwpCalibration(self):
        self.measurementParameters("qwp")
        self.takeCalibrationData()
        calibrated_angle = self.analyzeQwpData()
        self.update_qwp_position(calibrated_angle)


    def measurementParameters(self, optic):
        if optic == "pol":
            self.data_points = 200
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 180/self.data_points
        if optic == "qwp":
            self.data_points = 100
            # self.data_points = int(input("enter data points: "))
            self.rotation_interval = 90/self.data_points


    def takeCalibrationData(self, type = None):
        self.Voltages = []
        self.actual_positions = []
        for _ in range(self.data_points):
            
            if type is not None:
                self.actual_positions.append(self.pol_stage.get_position())
                self.getData(self.rotation_interval, type)
            else:
                self.actual_positions.append(self.qwp_stage.get_position())
                self.getData(self.rotation_interval)
            data = self._formatRpData(self.raw_data)
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
        max_angle = np.rad2deg(max_angle)
        print(f"Calibrated angle: {(max_angle):.3f}")
        return max_angle

        
    def analyzeQwpData(self): 
        popt, pcov = curve_fit(self.qwpCalibrationModel, np.deg2rad(self.actual_positions), self.Voltages)
        optimized_omega, optimized_beta, optimized_chi, optimized_delta = popt

        model_angles = np.deg2rad(np.linspace(0,90,10000))
        model_values = self.qwpCalibrationModel(model_angles, optimized_omega, optimized_beta, optimized_chi, optimized_delta)

        max_index = np.argmax(model_values)
        max_angle = model_angles[max_index] 
        max_angle = np.rad2deg(max_angle)
        print(f"Calibrated angle: {(max_angle):.3f}")


        plt.figure(figsize=(10,6))
        plt.scatter(self.actual_positions, self.Voltages, label = 'raw data')
        plt.plot(np.rad2deg(model_angles), model_values, label = 'fitted curve', color = 'purple')
        plt.legend()
        plt.show()
        return max_angle

    def update_qwp_position(self, calibrated_theta):
        try:
            theta = float(f"{calibrated_theta:.3f}")
            self.save_qwp_calibration_angle(theta)  # Save the new position
            self.qwp_calibrated_angle = theta  
            self.home_qwp()
            print(f"QWP starting position has been updated to: {theta}")
        
        except Exception as e:
            print(f"Unknown error has occured, position failed to save/update: {e}")

    def update_polarizer_position(self, calibrated_theta):

        try:
            theta = float(f"{calibrated_theta:.3f}")  # Get user input as a float
            self.save_polarizer_calibration_angle(theta)  # Save the new position
            self.pol_calibrated_angle = theta
            self.home_polarizer()
            print(f"Polarizer starting position has been updated to: {theta}")
        except Exception as e:
            print(f"Unknown Error: {e}")

        

    def save_polarizer_calibration_angle(self, pol_angle, file_path='polarizer_calibration_data.pkl'):
        calibration_data = pol_angle
        #  self.pol_stage.move_absolute(pol_angle)
        with open(file_path, 'wb') as file:
            pickle.dump(calibration_data, file)
        print("polarizer calibration data has been saved")


    def load_polarizer_calibration_angle(self, file_path='polarizer_calibration_data.pkl'):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                calibration_data = pickle.load(file)
                return calibration_data


    def save_qwp_calibration_angle(self, qwp_angle, file_path = 'qwp_calibration_data.pkl'):
        calibration_data = qwp_angle
        #  self.qwp_stage.move_absolute(qwp_angle)
        with open (file_path, 'wb') as file:
            pickle.dump(calibration_data, file)
        print("qwp calibration data has been saved")


    def load_qwp_calibration_angle(self, file_path = 'qwp_calibration_data.pkl'):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                calibration_data = pickle.load(file)
                return calibration_data

    def home_polarizer(self):
        try: 
            self.pol_stage.home(blocking=True)
            time.sleep(.3)
            self.pol_stage.move_absolute(self.load_polarizer_calibration_angle(), blocking=True)
        except Exception as e:
            print(f"Hardware Error: {e}")

    def home_qwp(self):
        try:
            self.qwp_stage.home()
            time.sleep(.3)
            self.qwp_stage.move_absolute(self.load_qwp_calibration_angle(), blocking=True)
        except Exception as e:
            print(f"Hardware Error: {e}")
    
    def print_calibration_angles(self):
        print(f"Calibrated Polarizer Angle: {self.pol_calibrated_angle}")
        print(f"Calibrated Quarter Wave Plate Angle: {self.qwp_calibrated_angle}")
                






            


        
