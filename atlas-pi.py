#!/usr/bin/python 

import datetime
import plotly.plotly as py
import serial
 
token = 'stream_token'
username = 'plotly_username_here'
api_key = 'plotly_api_key_here'
 
py.sign_in(username, api_key)
stream = py.Stream(token)
stream.open()

url = py.plot([
    {'x': [],
    'y': [],
    'type': 'scatter',
    'stream': {
        'token': token,
        'maxpoints': 100
        }
    }],
    filename='Atlas Streaming dOxy',
    fileopt='overwrite')
 
# Serial code adapted from: https://www.atlas-scientific.com/_files/code/pi_sample_code.pdf
print "Atlas is now Streaming to Plotly!"
print "View your plot here: ", url
usbport = '/dev/ttyAMA0'
ser = serial.Serial(usbport, 38400)
# turn on the LEDs
ser.write("L1\r")
ser.write("C\r")
line = ""
while True:
    data = ser.read()
    if(data == "\r"):
        print "Received from sensor:" + line
        # Parse the data
        try:
            line = float(line)
        except:
            print "Couldn't parse float: ", line
            continue
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # Write the data to your plotly stream
        stream.write({'x': time_now, 'y': line})        
        line = ""
    else:
        line = line + data 
