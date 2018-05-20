#!/usr/bin/python
# Atmospheric Pressure Chart Recorder and Live Display using LPS25HB connected to i2c

i2c_avalible = False    # if not using the Raspi, need to emulate i2c bus for testing purposes

import csv
import numpy as np
if i2c_avalible:
    import smbus  # dont import if we are testing not on a raspi

import time
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import matplotlib.animation as animation
from datetime import datetime
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None' #remove toolbar from figure display

def lps25hb_setup():
    bus = smbus.SMBus(1)
    # address is 0x5C, write to CTRL_REG1(0x20), Set active mode, continuous update at 1Hz (0x90)
    bus.write_byte_data(0x5C, 0x20, 0x90)

def lps25hb_read():
    # read pressure from register 0x28 with command 0x80 3 bytes of data, LSB
    raw_data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)
    return ((data[2]* 65536 + data[1] * 256 + data[0]) / 4096.0) # convert to hPa

# ===USER SETTINGS AND VARIABLES===
sampleSize = 1440

# ===MATPLOTLIB DATES SETTINGS===
hours = dts.HourLocator(interval=2)
minutes = dts.MinuteLocator()
timeFmt = dts.DateFormatter('%H:%M')

# ===READ IN PAST DATA===
# read in CSV file that pressure data is stored into

''' NUL Check '''
with open('PressureData.csv', 'rb') as data_fileA:
    data_contents = data_fileA.read()

''' check for NUL bytes '''
with open('PressureData.csv', 'wb') as data_fileB:
    data_fileB.write(data_contents.replace('\x00', ''))

PressureHistory = []
with open('PressureData.csv', 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for row in data:
        PressureHistory.append(row)

timePts = []
pressurePts = []

if len(PressureHistory) > 0:
    for x in PressureHistory:
        try:
            timePts.append(float(x[0]))
            pressurePts.append(float(x[1]))
        except:
            pass
           
# ===LPS25HB SETUP AND INITIALIZATION===

time.sleep(0.1)

fig = plt.figure('Atmospheric Pressure', figsize=(5,3), dpi=190)
ax1 = fig.add_subplot(1,1,1)
#ax1.ticklabel_format(useOffset=False)

def animate(i):
    if i2c_avalible:
        # read pressure
        data = lps25hb_read()
    else:
        # make shit up if i2c is not available
        data = np.random.randint(900, 1020)
        
    timePts.append(dts.date2num(datetime.now()))
    pressurePts.append(data)
    print str(datetime.now()) + ' ' + str(pressurePts[-1])
    
    # ===APPEND DATA TO CSV===
    with open('PressureData.csv', 'ab') as csvfile:
        rowappend = csv.writer(csvfile, delimiter=',')
        rowappend.writerow([timePts[-1], pressurePts[-1]])

    # ===PLOTTING===
    #while len(pressurePts) > sampleSize:
    #    del pressurePts[0]
    #    del timePts[0]
    if (len(pressurePts) > sampleSize):
        del pressurePts[0:-sampleSize]
        del timePts[0:-sampleSize]

    #fig, ax = plt.subplots()
    ax1.clear()
    ax1.plot(timePts, pressurePts)
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    # format the ticks
    ax1.xaxis.set_major_locator(hours)
    ax1.xaxis.set_major_formatter(timeFmt)
    
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize('xx-small')
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize('xx-small')
    
    # axis labels
    ax1.set_xlabel("Past 24 Hours", fontsize="xx-small")
    ax1.set_ylabel("Atmospheric Pressure [hPa]", fontsize="xx-small")

    #ax.xaxis.set_minor_locator(minutes)

    ax1.format_xdata = dts.DateFormatter('%H:%M')
    fig.autofmt_xdate()
    fig.tight_layout()

ani = animation.FuncAnimation(fig,animate, interval=60000)
plt.show()
