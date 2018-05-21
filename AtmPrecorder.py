'''
Created on May 21, 2018

@author: samper
'''
i2c_avalible = False                            # if not running on raspberry pi then set to false for testing
new_data = True                                 # gloabal varable to detrmin if a new df should be created
display_yesterday = True                        # global varable to set display of yesterdays pressure recording
fake_pastdata = True

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dts
import matplotlib.animation as animation
from matplotlib import style
import matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'                #remove toolbar from figure display

if i2c_avalible:                                # if true import smbus for i2c communication
    import smbus                                # @UnresolvedImport
else:                                           # if false use random numbers generated by numpy to make up data
    import numpy.random as npr

def lps25hb_setup():
    bus = smbus.SMBus(1)
    bus.write_byte_data(0x5C, 0x20, 0x90)       # address is 0x5C, write to CTRL_REG1(0x20),
                                                # Set active mode, continuous update at 1Hz (0x90)

def lps25hb_read():
    raw_data = bus.read_i2c_block_data(0x5C,    # @UndefinedVariable
                                       0x28 | 0x80,
                                       3)       # read pressure from register 0x28 with command 0x80 3 bytes of data, LSB
    return ((raw_data[2]* 65536 
             + raw_data[1] * 256 
             + raw_data[0]) / 4096.0)           # convert to hPa

''' LPS25HB Setup and Initilation '''
if i2c_avalible:
    lps25hb_setup()
else:
    print "Testing mode, data will be randomly generated"

''' Matplotlib Settings '''
style.use('dark_background')                    # change the style of the plot to one of the predefined styles
two_hours = dts.HourLocator(interval=2)         # for major locater
one_hour = dts.HourLocator()                    # for minor locater
timeFmt = dts.DateFormatter('%H:%M')            # time format of the x-axis

fig = plt.figure('Atmospheric Pressure',        # name that will appear on the window title bar
                 figsize=(5,3),                 # figure size in inches
                 dpi=190)                       # figure resolution to fit nicely on 5" display, may look ugly on other displays
ax1 = fig.add_subplot(1,1,1)

''' fake past data for testing '''
if fake_pastdata:
    import numpy as np
    dt_array = [datetime.datetime(2018, 5, 20, 0, 0) + datetime.timedelta(minutes=x) for x in range(0, 1440)]
    pi2 = np.linspace(-2*np.pi, 2*np.pi, num=1440)
    a = [34*np.sin(p)+994.0 for p in pi2]
    df = pd.DataFrame({'datetime': dt_array,
                       'atm_pressure_hpa': a})
    
    df.to_hdf('PressureData-{}.h5'.format(datetime.date.today() - datetime.timedelta(days=1)), key='df')

def ani(i):                                     # @UnusedVariable
    global new_data                             # import global variables
    global i2c_avalible
    global display_yesterday
    
    if new_data:                                # have we collected data before?
        ani.df = pd.DataFrame({'datetime':[],   # create empty dataframe to append to
                            'atm_pressure_hpa':[]})
        ani.todays_date = datetime.date.today()
        ani.tomorrows_date = ani.todays_date + datetime.timedelta(days=1)
        new_data = False
        
        if display_yesterday:
            try:
                ani.df_past = pd.read_hdf('PressureData-{}.h5'.format(ani.todays_date - datetime.timedelta(days=1)),
                                          key='df')
            except IOError:
                print "No past data!"
    elif datetime.date.today() > ani.todays_date:
        ''' save data every day to new file '''
        ani.df.to_hdf('PressureData-{}.h5'.format(ani.todays_date), key='df')
        del ani.df
        new_data = True
    else:
        ''' get new data '''
        if i2c_avalible:                        # get data from pressure sensor
            ani.df = ani.df.append({'datetime':datetime.datetime.now(),
                            'atm_pressure_hpa':lps25hb_read()},
                            ignore_index=True)
        else:                                   # make shit up
            ani.df = ani.df.append({'datetime':datetime.datetime.now(),
                            'atm_pressure_hpa':npr.randint(96000, 102800)/100.0},
                            ignore_index=True)
        
        ''' Print to console for debugging stuff '''
        print "{}, {:.2f} hpa".format(ani.df['datetime'].iloc[-1], ani.df['atm_pressure_hpa'].iloc[-1])
        
        ''' Plotting '''
        ax1.clear()
        
        if display_yesterday:
            try:
                ax1.plot(ani.df_past['datetime'] + datetime.timedelta(days=1), ani.df_past['atm_pressure_hpa'],
                         color='gray',
                         linewidth=0.5)
            except Exception as e: 
                print(e)
                
        ax1.plot(ani.df['datetime'], ani.df['atm_pressure_hpa'])
        ax = plt.gca()
        
        ax.get_yaxis().get_major_formatter().set_useOffset(False)
        
        ''' Set the xaxis range from today midnight to tomorrow midnight '''
        ax1.set_xlim([datetime.datetime(ani.todays_date.year, ani.todays_date.month, ani.todays_date.day, 0, 0),
                      datetime.datetime(ani.tomorrows_date.year, ani.tomorrows_date.month, ani.tomorrows_date.day, 0, 0)])
    
        # format the ticks
        ax1.xaxis.set_major_locator(two_hours)
        ax1.xaxis.set_minor_locator(one_hour)
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
        
        # format the grid
        ax1.grid(color='grey', linestyle='dotted', linewidth=0.5)
        
        # annotate plot with new data
        ax1.text(0.99, 0.99,
                 '{:.0f} hPa'.format(ani.df['atm_pressure_hpa'].iloc[-1]),
                 transform=ax1.transAxes,
                 fontsize=10,
                 color='orange',
                 verticalalignment='top',
                 horizontalalignment='right')
        
        date_str = '{}/{:02d}/{}'.format(ani.df['datetime'].iloc[-1].month, ani.df['datetime'].iloc[-1].day, ani.df['datetime'].iloc[-1].year)
        time_str = '{}:{:02d}'.format(ani.df['datetime'].iloc[-1].hour, ani.df['datetime'].iloc[-1].minute)
        
        ax1.text(0.99, 0.94,
                 date_str,
                 transform=ax1.transAxes,
                 fontsize=6,
                 color='orange',
                 verticalalignment='top',
                 horizontalalignment='right')
        
        ax1.text(0.99, 0.91,
                 time_str,
                 transform=ax1.transAxes,
                 fontsize=6,
                 color='orange',
                 verticalalignment='top',
                 horizontalalignment='right')

ani = animation.FuncAnimation(fig, ani, interval=60000)  # plot every 60 seconds
plt.show()