import serial.tools.list_ports

def check_used_ports():
    ports = serial.tools.list_ports.comports()
    used_ports = []
    
    for port in ports:
        try:
            ser = serial.Serial(port.device, baudrate=9600, timeout=1)
            ser.close()  # If it opens successfully, it's not in use
        except (OSError, serial.SerialException):
            used_ports.append(port.device)  # If it fails, it's likely in use

    if used_ports:
        print("The following COM ports are currently in use:")
        for port in used_ports:
            print(f" {port}")
    else:
        print("No COM ports are currently in use.")

# Run the function
check_used_ports()
