# digital-walkman
Micropython code for the Walkman project on Printables

## Introduction
This repo was made to share the python source code for my Digital Walkman Project over on [Printables]("https://www.printables.com/model/866022-walkman-inspired-mp3-player")

It is not under active development, but if there is an issue I will try my best to fix it.

The project uses a Raspberry Pi Pico, a DFPlayer mini and an ssd1306 (optional) OLED display, so this code will only work with those.

## Usage

### Wiring
For the wiring of the Pico, consult the code and change it to fit your specific setup. Keep in mind, that I am referencing the logical pin numbers, rather than the physical ones, consult the Pico documentation for more information. The pins I have used are as follows:

- ```GPIO 12``` - UART TX pin for the DFPlayer
- ```GPIO 13``` - UART RX pin for the DFPlayer
- ```GPIO 0``` - SDA pin for the i2c display
- ```GPIO 1``` - SCL pin for the i2c display
- ```GPIO 2``` - Busy pin for the DFPlayer
- ```GPIO 6``` - LED output pin (make sure to use a 300 ohm resistor)
- ```GPIO 18``` - Side A detector pin (should short with 3v3 if the A side is inserted)
- ```GPIO 19``` - Side B detector pin (should short with 3v3 if the B side is inserted)

All button pins are set up for normally open buttons and should short with 3v3
- ```GPIO 11``` - Pause button
- ```GPIO 9``` - Next song button
- ```GPIO 7``` - Previous song button
- ```GPIO 14``` - Volume up button
- ```GPIO 15``` - Volume down button
- ```GPIO 17``` - On-Line/mode button

The input and output pins are interchangeable, but watch out for the UART and i2c wires, as only certain pins on the Pico can be used for these

### Firmware
Set up your Pico for Micropython using the [documentation]("www.micropython.org/download").         

### OLED
If you would like to use an OLED display just copy `main.py`, `settings.txt`, `ssd.py` and `dfdriver.py` over to your Pico, and change the relevant values, if you arent't using the same pins as I am.

### No OLED
If you are not using an OLED display, delete `main.py`, rename `mainnooled.py` to `main.py` and copy `main.py`, `settings.txt`, `ssd.py` and `dfdriver.py` over to your Pico, and change the relevant values, if you arent't using the same pins as I am.