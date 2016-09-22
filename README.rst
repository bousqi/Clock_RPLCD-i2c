Custom Clock for LCD 16x02 (based on RPLCD-i2c)
#####

Thanks to XXXX for the RPLCD-i2c driver.
https://github.com/zador-blood-stained/RPLCD-i2c

A Python 2/3 Raspberry Pi Custom Clock for the Hitachi HD44780 LCD

Tested with the 16x2 LCD MT-20S4A??, Raspberry Pi3 and PCF8574AT
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

Refer to original github repo for more details
https://github.com/zador-blood-stained/RPLCD-i2c

Installation
========

.. code::

     git clone https://github.com/bousqi/Clock_RPLCD-i2c.git
     cd Clock_RPLCD-i2c
     sudo python3 setup.py install
     # and/or
     sudo python setup.py install


I²C bus number
-----------

For Rasbberry Pi Model A, B Rev 2, B+, Raspberry Pi 2 and Raspberry Pi 3 use bus number 1
For Raspberry Pi Model B Rev 1 use bus number 0

I²C device address
-----------

To check your port expander address use ``gpio i2cd`` command
(alternatively ``sudo i2cdetect -y 0``
or ``sudo i2cdetect -y 1`` depending on bus number)
Example output with one PCF8574AT connected at address 0x3F:

.. code::

     % sudo i2cdetect -y 1
          0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
     00:          -- -- -- -- -- -- -- -- -- -- -- -- --
     10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 3F
     40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     70: -- -- -- -- -- -- -- --
     %

or refer to datasheet for your port expander.

Features, Code examples & Usage
========

blabla

Testing
=======

To test your 20x4 display, please run the ``test_20x4.py`` script and
confirm/verify each step with the enter key. Make sure to set your bus 
number and address to the ``CharLCD`` constructor in ``test_20x4.py``.

To test your 16x2 display, please run the ``test_16x2.py`` script and
confirm/verify each step with the enter key. Make sure to set your bus 
number and address to the ``CharLCD`` constructor in ``test_16x2.py``.

You can check the charmap on your display with ``show_charmap.py 2 16``
on a 16x2 display.

License
=======

This code is licensed under the MIT license, see the `LICENSE file
<https://github.com/zador-blood-stained/RPLCD-i2c/blob/master/LICENSE>`_ or `tldrlegal
<http://www.tldrlegal.com/license/mit-license>`_ for more information. 

The module ``RPLCD/enum.py`` is (c) 2004-2013 by Barry Warsaw. It was
distributed as part of the ``flufl.enum`` package under the LGPL License version
3 or later.
