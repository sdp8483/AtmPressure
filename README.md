# AtmPressure
Atmospheric Pressure Logging and Display using LPS25HB Sensor and Raspberry Pi

## The Hardware
A STEVAL-MKI165V1 evaulation board base on the LPS25HB atmospheric pressure sensor is connected to the Raspberry Pi using I2C. Power is provided by the raspberry Pi's onboard 3.3V rail.

Also connected is a DS3231 Precision RTC breakout for clock recovery after loss of power since for my aplication this will not be connected to the internet.
Follow this guide from Adafruit for configuring the RTC: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/overview

Also used in my setup is a 5" HDMI 800x480 TFT Display with XPT2046 Touch Controller. The touch controller is not used. It is reqired to modify `/boot/config.txt` so that the full dispay can be used:

```
# uncomment if you get no picture on HDMI for a default "safe" mode
#hdmi_safe=1

# uncomment this if your display has a black border of unused pixels visible
# and your display can output without overscan
disable_overscan=0

# uncomment if hdmi display is not detected and composite is being output
#hdmi_force_hotplug=1

# uncomment to force a specific HDMI mode (this will force VGA)
hdmi_group=2
hdmi_mode=1
hdmi_mode=87
hdmi_cvt=800 480 60 6 0 0 0
```
Source: https://www.jeffgeerling.com/blog/2016/review-elecrow-hdmi-5-800x480-tft-display-xpt2046-touch-controller

## The Software
clone this repository to ```/home/pi/```
 
 ```
 cd /home/pi
 git clone https://github.com/sdp8483/AtmPressure
 ```
 
 to start the python script on boot edit ```/etc/rc.local``` by adding the following line before ```exit 0```
 ```
 python /home/pi/AtmPressure/AtmosphericPressureRecorder.py &
 ```
 
 **Dont forget the ```&``` or your pi will not boot**
 See: https://www.raspberrypi.org/documentation/linux/usage/rc-local.md for more info
