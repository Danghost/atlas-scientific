#!/usr/bin/python 
 
import datetime
import plotly
import serial
import time
 
username = 'plotly_username_here'
api_key = 'plotly_api_key_here'
tokens = ['token1', 'token2']
token1 = 'token1'
token2 = 'token2'
 
p = plotly.plotly(username, api_key)
streams = [plotly.stream(token) for token in tokens]
 
p.plot([
    {'x': [],
    'y': [],
    'name': 'pH',
    'type': 'scatter',
    'stream': {
        'token': token1,
        'maxpoints': 20
        }
    },
    {'x':[],
    'y': [],
    'yaxis': 'y2',
    'name': 'dOxy',
    'type': 'scatter',
    'stream': {
        'token': token2,
        'maxpoints':20
        }
    }],
    layout= {
        'yaxis': {'title':'pH'},
        'yaxis2': {'title':'dOxy mg/L', 'overlaying': 'y', 'side':'right'}
        },
    filename='Atlas Streaming DO+PH',
    fileopt='overwrite')
 
# Serial code adapted from: https://www.atlas-scientific.com/_files/code/pi_sample_code.pdf
print "Plotly + Atlas Streaming"
uart1 = '/dev/ttyO1'
uart2 = '/dev/ttyO2'
ser1 = serial.Serial(uart1, 38400)
ser2 = serial.Serial(uart2, 38400)
 
# L1 turns on the LEDs
# C initiates continuous reading
ser1.write("L1\r")
ser1.write("C\r")
 
ser2.write("L1\r")
ser2.write("C\r")
 
line1 = ""
line2 = ""
while True:
    data1 = ser1.read()
    data2 = ser2.read()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    if(data1 == "\r"):
        print "Received from pH:" + line1
        # Parse the data
        try:
            line1 = float(line1)
        except:
            print "Couldn't parse float: ", line1
            continue
        streams[0].write({'x': time_now, 'y': line1})
        line1 = ""
    else:
        line1 = line1 + data1
    
    if(data2 == "\r"):
        print "Received from DO:" + line2
        try:
            line2 = float(line2)
        except: 
            print "Couldn't parse float: ", line2
            continue
        streams[1].write({'x': time_now, 'y': line2})
        line2 = ""
    else:
        line2 = line2 + data2
        
    time.sleep(5)
