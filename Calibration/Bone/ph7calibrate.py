import serial
import sys
print "pH calibrated to 7"

usbport = '/dev/ttyO1'
ser = serial.Serial(usbport, 38400)

# turn on the LEDs
ser.write("L1\r")
ser.write("S\r")

sys.exit(0)
