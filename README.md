# AtmPressure
Atmospheric Pressure Logging and Display using LPS25HB Sensor and Raspberry Pi

## The Hardware
A STEVAL-MKI165V1 evaulation board base on the LPS25HB atmospheric pressure sensor is connected to the Raspberry Pi using I2C. Power is provided by the raspberry Pi's onboard 3.3V rail.

Also connected is a DS3231 Precision RTC breakout for clock recovery after loss of power since for my aplication this will not be connected to the internet.
Follow this guide from Adafruit for configuring the RTC: https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi/overview

## The Software
