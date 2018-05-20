#!/usr/bin/python
# Atmospheric Pressure Chart Recorder and Live Display using LPS25HB connected to i2c

''' User Settings - Modify to for code testing or normal use '''
i2c_avalible = False    # if not using the Raspi, need to emulate i2c bus for testing purposes
save_interval = 5       # interval in minutes to save df to sd card

import numpy as np
import pandas as pd
import datetime
if i2c_avalible:
    import smbus  # don't import if we are testing not on a raspi

import matplotlib.pyplot as plt
import matplotlib.dates as dts
import matplotlib.animation as animation
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

# ===MATPLOTLIB DATES SETTINGS===
hours = dts.HourLocator(interval=2) # for major locater
hour = dts.HourLocator()    # for minor locater
timeFmt = dts.DateFormatter('%H:%M')

# ===READ IN PAST DATA===
try:
    df = pd.read_hdf('PressureData.h5', key='df')
except IOError:
    print('No Past Data, Creating New!')
    df = pd.DataFrame() # create empty dataframe to append to

# ===LPS25HB SETUP AND INITIALIZATION===
if i2c_avalible:
    lps25hb_setup()

fig = plt.figure('Atmospheric Pressure Over Time', figsize=(5,3), dpi=190)
ax1 = fig.add_subplot(1,1,1)
#ax1.ticklabel_format(useOffset=False)

count_to_save = save_interval

def animate(i):
    #get new data!
    if i2c_avalible:
        # read pressure
        data = pd.DataFrame({'datetime': [datetime.datetime.now()],
                            'atm_pressure_hpa':[lps25hb_read()]})
    else:
        # make shit up if i2c is not available
        data = pd.DataFrame({'datetime': [datetime.datetime.now()],
                            'atm_pressure_hpa':[np.random.randint(900, 1020)]})
    
    df = df.append(data, ignore_index=True) # append to df so that it can be saved
    
    if (count_to_save == save_interval):
        df.to_hdf('PressureData.h5', key='df', mode='w')    # save to sd card
        count_to_save = 0
    else:
        count_to_save+=1                                    # increment by one
    
    print "{} {:.2f}hPa".format(df['datetime'], df['atm_pressure_hpa'])

    # ===PLOTTING===
    ax1.clear()
    ax1.plot(df['datetime'], df['atm_pressure_hpa'])
    ax = plt.gca()
    ax.get_yaxis().get_major_formatter().set_useOffset(False)

    # format the ticks
    ax1.xaxis.set_major_locator(hours)
    ax1.xasix.set_minor_locator(hour)
    ax1.xaxis.set_major_formatter(timeFmt)
    ax1.grid(True)
    
    for tick in ax1.xaxis.get_major_ticks():
        tick.label.set_fontsize('xx-small')
    for tick in ax1.yaxis.get_major_ticks():
        tick.label.set_fontsize('xx-small')
    
    # axis labels
    ax1.set_ylabel("Atmospheric Pressure [hPa]", fontsize="xx-small")

    ax1.format_xdata = dts.DateFormatter('%H:%M')
    fig.autofmt_xdate()
    fig.tight_layout()

ani = animation.FuncAnimation(fig,animate, interval=60000)  # plot every 60 seconds
plt.show()
