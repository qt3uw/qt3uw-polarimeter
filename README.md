# __qt3uw-polarimeter__
## __Introduction__:
This project is designed to measure and analyze the polarization state of a coherant light source entering the system (i.e a laser). Using a combination of hardware control, and data acquisition components, this system allows for calibration and real-time measurements of Polarization.

###   Key Features: 
* __Automated Calibration__: The system can automatically calibrate both the polarizer and quarter wave plate and save their calibration data for future use

* __Polarization Measurement__: Built in algorithms extract parameters from raw data used to compute and visualize the polarization state of incoming light

* __User-Friendly Interface__: This project is accompanied with a simple GUI that allows for easy control of the system include initialization, calibration, data collection, and visualization

 * __Visualization__: The interface provides a plotting feature to visualize the polarization state over time, allowing for multiple plots at once combined with a greyscale feature to denote newer data

This project is ideal for researchers and engineers working in optical expirementation requiring a solution for a polarimeter measurement and calibration of lasers

## __Hardware Setup__

#### Components
_Thorlabs_
*  1x L202 Laser 635nm
*  1x PDA36A2 PhotoDiode
*  2x Ell14K Mount Bundle
*  1x WP25M-VIS Wire Grid Polarizer 420-700nm
*  1x AQWP05M-600 Quarter-Wave Plate 400-800nm
*  Mounting Components

_Red Pitaya_
*  125-10 FGPA

_Miscallaneous_
*  3x USB to MicroUSB Data Cables
*  3x Ethernet Cables
*  1x Ethernet Switch
*  1x Polarizing Beam Splitter Cube (for calibration)
*  COAX BNC Cable
*  BNC Adapter

## Configuration


Driver.py ---- > def main() ---- > number_of_increments

Changing this value changes the number of steps that power is measured as the quarter wave plate is rotated. There is a tradeoff between speed and accuracy. Depending on your needs, this can and should be changed. The most that I used with great accuracy was 120. Minimum for the algorithms to function, but not reccommended, is 8 steps. 

###  Calibration:
For the first step of calibration, ensure that you only have the polarizer + your calibrating polarizer element, we used a beam slitter cube. The purpose of this calibration is to align the mounted optics axis horizontally. For the second step, reintroduce the quarter wave plate in between the calibration element and the mounted polarizer. After going through these steps in the GUI it your optics will be properly calibrated and the data should be saved for future use. 
