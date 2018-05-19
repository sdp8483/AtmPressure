# AtmPressure
Atmospheric Pressure Logging and Display using LPS25HB Sensor and Raspberry Pi

A STEVAL-MKI165V1 evaluation board based on the LPS25HB atmospheric pressure sensor is connected to the Raspberry Pi using I2C. Power is provided by the raspberry Pi's onboard 3.3V rail.

Also connected is a DS3231 Precision RTC breakout for clock recovery after loss of power since this will not be connected to the Internet 24/7.
Follow this guide from Adafruit for configuring the RTC: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/overview

A 5" HDMI 800x480 TFT Display with XPT2046 Touch Controller is used as the display. The touch controller is not used. It is required to modify `/boot/config.txt` so that the full display can be used:
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

clone this repository to `/home/pi/`
 ```
 cd /home/pi
 git clone https://github.com/sdp8483/AtmPressure
 ```
 
 Matplotlib for Python 2 will need to be installed. Using the terminal on the Pi install Matplotlib using the following command:
 ``` 
 sudo apt-get install python-matplotlib 
 ```
 
 To disable the display going black I have found the easiest option is to install xscreensaver
 ```
 sudo apt-get install xscreensaver
 ```
 after installing, on the RPI desktop got the the raspberry start icon -> preference -> screensaver and select disable screensaver.
 Source: https://www.raspberrypi.org/documentation/configuration/screensaver.md
 
 The display will look better if the mouse cursor is hidden when not in use.
 ```
 sudo apt-get install unclutter
 ```
 Then edit the LXDE Autostart script
 ```
 nano ~/.config/lxsession/LXDE-pi/autostart
 ```
 and add this line to the startup script
 ```
 @unclutter -idle 0
 ```
 source: https://jackbarber.co.uk/blog/2017-02-16-hide-raspberry-pi-mouse-cursor-in-raspbian-kiosk
 
 Hiding the taskbar is useful since it is not needed. Right click the taskbar and select *Panel Settings* click on the *Advanced* tab and check *Minimize panel when not in use* and set the size to a pixel or two.
 
 To start the python script on boot you will need to use the `launcher.sh` script that was cloned into the AtmPressure directory from the GitHub repository.
 Start by changing the file permissions of `launcher.sh` and `AtmposphericPressureRecorder.py`
 ```
 cd /home/pi/AtmPressure
 chmod +x launcher.sh
 chmod +x AtmposphericPressureRecorder.py
 
 sudo nano /etc/profile
 ```
 add the following line to the end of the file
 ```
 /home/pi/AtmPressure/launcher.sh
 ```
 
 reboot the raspberry pi to enable all changes and to start the script
 it may look ugly at first but give it minute to catch up