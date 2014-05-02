import serial
import sys
print "Your Dissolved Oxygen Sensor is now Calibrated."

usbport = '/dev/ttyO2'
ser = serial.Serial(usbport, 38400)

# turn on the LEDs
ser.write("L1\r")
ser.write("M\r")

line = ""

while True:
  data = ser.read()
  if(data == "\r"):
    print "Received from sensor:" + line
    line = ""
    sys.exit(0)
  else:
    line = line + data
