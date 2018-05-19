# Live Pressure Display and Plotting with the LPS25HB

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import smbus
#import random

bus = smbus.SMBus(1)
# LPS25HB address is 0x5C
# Write to CTRL_REG1(0x20)
#    Set active mode, continuse update at 1Hz (0x90)
bus.write_byte_data(0x5C, 0x20, 0x90)
time.sleep(0.1)

fig = plt.figure(figsize=(16,9), dpi=80)
ax1 = fig.add_subplot(1,1,1)

# Initialize pressure samples
# 24hrs of data, at 1min sample rate need 1440 samples
pressurePts = []
#for i in range(0,1440):
#    pressurePts.append(random.randrange(980, 1000)) #give bogus number

def animate(i):
    # read pressure from register 0x28 with command 0x80
    # 3 bytes of data, LSB
    data = bus.read_i2c_block_data(0x5C, 0x28 | 0x80, 3)

    # convert to hPa
    pressurePts.append((data[2]* 65536 + data[1] * 256 + data[0]) / 4096.0)
    
    if (len(pressurePts) > 1440):
        #remove oldest sample
        del pressurePts[0]

    #print to consol
    print pressurePts[-1]

    ax1.clear()
    ax1.plot(pressurePts)
    #ax1.set_ylim(990, 1005)

ani = animation.FuncAnimation(fig,animate, interval=60000)
plt.show()
