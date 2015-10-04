RPLCD-i2c
#####

A Python 2/3 Raspberry Pi Character LCD library for the Hitachi HD44780
controller, I²C only version.
May work on other embedded boards with I²C bus.

Based on RPLCD library https://github.com/dbrgn/RPLCD

Tested with the 20x4 LCD MT-20S4A, Raspberry Pi model B and PCF8574AN
I²C port expander.

Original GPIO based library tested with:
- 20x4 LCD that is sold for example by adafruit.com or mikroshop.ch
- 16x2 LCD from mikroshop.ch

Depends on `python-smbus` library.
For getting smbus support in Python 3.x use instructions provided here:

http://procrastinative.ninja/2014/07/21/smbus-for-python34-on-raspberry/

http://jtecheng.com/?p=959

Wiring
========

For setting up I²C bus on Raspberry Pi see pinout here:

http://elinux.org/RPi_Low-level_peripherals

For enabling I²C bus on Device Tree enabled kernel
see instructions here:

https://github.com/raspberrypi/firmware/blob/master/boot/overlays/README

Connecting PCF8574A (DIP16 package) to Raspberry Pi B Rev. 2
-----------

with address bits A0, A1, A2 set to 0

========== ================= ============== ===============
RPi signal RPi B rev2 pin #  PCF8574 signal PCF8574 pin #
+3.3v      1, 17             VCC            16       
GND        6, 9, 14, 20, 25  GND            1, 2, 3, 8   
SCL        5                 SCL            14       
SDA        3                 SDA            15       
========== ================= ============== ===============

Connecting LCD display to PCF8574A and Raspberry Pi
-----------

with contrast set to maximum (U0 connected to GND)

============== ============== ============ ===========
PCF8574 signal PCF8574 pin #  LCD signal   LCD Pin #     
GND            8              GND, U0      1, 3          
P0             4              RS (A0)      4             
P1             5              R/W          5             
P2             6              E            6             
P4             9              DB4          11            
P5             10             DB5          12            
P6             11             DB6          13            
P7             12             DB7          14            
============== ============== ============ ===========

Connect display pin 2 (VCC) to Raspberry Pi pin 2 (5v) 
OR to Raspberry Pi pin 1 (3.3v)
depending on your display required supply voltage.

To activate display backlight connect LCD pin 15 (+LED) to 5 or 3.3v,
connect LCD pin 16 (-LED) to GND directly or through a MOSFET (see schemacic below).

It is recommended to connect 0.1 uF ceramic bypass capacitor
between VCC (16) and GND (8) pins of port expander.

Connection schematics
========

Without backlight control
-----------

.. image:: https://cdn.rawgit.com/zador-blood-stained/RPLCD-i2c/master/RPLCD-i2c.sch.svg
	:alt: Schematic w/o backlight control

With backlight control
-----------

.. image:: https://cdn.rawgit.com/zador-blood-stained/RPLCD-i2c/master/RPLCD-i2c-backlight.sch.svg
	:alt: Schematic with backlight control

Backlight control requires N-channel MOSFET 
with certain characteristics, i.e. BS170, 2N7000, 2N7002.

Installation
========

.. code::

     git clone https://github.com/zador-blood-stained/RPLCD-i2c.git
     cd RPLCD-i2c
     sudo python3 setup.py install
     # and/or
     sudo python setup.py install


I²C bus number
-----------

For Rasbberry Pi Model A, B Rev 2, B+ and Raspberry Pi 2 use bus number 1
For Raspberry Pi Model B Rev 1 use bus number 0

I²C device address
-----------

To check your port expander address use ``gpio i2cd`` command
(alternatively ``sudo i2cdetect -y 0``
or ``sudo i2cdetect -y 1`` depending on bus number)
Example output with one PCF8574A connected at address 0x38:

.. code::

     % sudo i2cdetect -y 1
          0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
     00:          -- -- -- -- -- -- -- -- -- -- -- -- --
     10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     30: -- -- -- -- -- -- -- -- 38 -- -- -- -- -- -- --
     40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     70: -- -- -- -- -- -- -- --
     %

or refer to datasheet for your port expander.

Features, Code examples & Usage
========

See original library documentation here: https://github.com/dbrgn/RPLCD


Testing
=======

To test your 20x4 display, please run the ``test_20x4.py`` script and
confirm/verify each step with the enter key. Make sure to set your bus 
number and address to the ``CharLCD`` constructor in ``test_20x4.py``.

License
=======

This code is licensed under the MIT license, see the `LICENSE file
<https://github.com/zador-blood-stained/RPLCD-i2c/blob/master/LICENSE>`_ or `tldrlegal
<http://www.tldrlegal.com/license/mit-license>`_ for more information. 

The module ``RPLCD/enum.py`` is (c) 2004-2013 by Barry Warsaw. It was
distributed as part of the ``flufl.enum`` package under the LGPL License version
3 or later.
