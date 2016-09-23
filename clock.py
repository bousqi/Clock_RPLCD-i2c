#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys
import bme280

from RPLCD_i2c import CharLCD
from RPLCD_i2c import Alignment, CursorMode, ShiftMode
from RPLCD_i2c import cursor, cleared
from time import strftime, sleep
from datetime import datetime

# build big digits
def disp_number(lcd_char, position):

    if lcd_char=="0" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(4))
        lcd.write_string(unichr(0))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(7))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))

    elif lcd_char=="1" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(0))
        lcd.write_string(unichr(5))
        lcd.write_string(unichr(254))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(1))
		
    elif lcd_char=="2" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(1))

    elif lcd_char=="3" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(0))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))

    elif lcd_char=="4" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(255))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(6))
		
    elif lcd_char=="5" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(2))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))
		
    elif lcd_char=="6" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(4))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(2))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(7))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))
		
    elif lcd_char=="7" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(0))
        lcd.write_string(unichr(0))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(6))
		
    elif lcd_char=="8" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(4))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(7))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))
		
    elif lcd_char=="9" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(2))
        lcd.write_string(unichr(5))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(1))
        lcd.write_string(unichr(6))
     
    elif lcd_char=="C" :
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(255))
        lcd.write_string(unichr(2))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
    
    else:
        lcd.cursor_pos = (0, position)
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
        lcd.cursor_pos = (1, position)
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
        lcd.write_string(unichr(254))
    
    return lcd_char;
    
# scroll effect
def shift(direction): 
    if direction=="left" :
        for x in range(0, 16):
            lcd.shift_display(-1)
            sleep(0.05)
    else :
        for x in range(0, 16):
            lcd.shift_display(1)
            sleep(0.05)

def read_temp():
    temperature,pressure,humidity = bme280.readBME280All()
    return temperature
                
def clock_dots():
    # display two dots
    lcd.cursor_pos = (0, 8)
    lcd.write_string(unichr(3))
    lcd.cursor_pos = (1, 8)
    lcd.write_string(unichr(3))
    sleep(0.5)
    
    # remove the two dots
    lcd.cursor_pos = (0, 8)
    lcd.write_string(unichr(254))
    lcd.cursor_pos = (1, 8)
    lcd.write_string(unichr(254))
    sleep(0.5)

def clock_date(digits, month, day_name):
    # previous text leaving to left
    shift("left")
    # preparing date buffer
    tens_day = disp_number(digits[4], 0)
    day = disp_number(digits[5], 4)
    lcd.cursor_pos = (0, 8)
    lcd.write_string('        ')
    lcd.cursor_pos = (1, 8)
    lcd.write_string('        ')
    lcd.cursor_pos = (0, 8)
    lcd.write_string(month[:8])
    lcd.cursor_pos = (1, 8)
    lcd.write_string(day_name[:8])
    # date entering from left
    shift("right")
    sleep(2)


def clock_temp():
    # previous text leaving to left
    shift("left")
    # preparing temp buffer
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Temp:           ')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('                ')

    temp_digits = str(read_temp());
    disp_number(temp_digits[0], 6)
    disp_number(temp_digits[1], 10)
    disp_number("C", 14)
    lcd.cursor_pos = (0, 13)
    lcd.write_string(unichr(223))
    # date entering from left
    shift("right")
    sleep(5)

def clock_hour(digits):
    # date leaving to left
    shift("left")
    # preparing hour buffer
    lcd.cursor_pos = (0, 0)
    lcd.write_string('                ')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('                ')
    disp_number(digits[0], 0)
    disp_number(digits[1], 4)
    disp_number(digits[2], 9)
    disp_number(digits[3], 13)
    # hour entering from left
    shift("right")


def main():

    try:
        input = raw_input
    except NameError:
        pass

    try:
        unichr = unichr
    except NameError:
        unichr = chr

    old_time = 0
    counter = 0

    # custom symbols
    lcd.clear()
    top_line = (0b11111, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000)
    bottom_line = (0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111)
    both_lines = (0b11111, 0b11111, 0b00000, 0b00000, 0b00000, 0b00000, 0b11111, 0b11111)
    dot = (0b00000, 0b00000, 0b00000, 0b11000, 0b11000, 0b00000, 0b00000, 0b00000)
    up_left = (0b00111, 0b01111, 0b01111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111)
    up_right = (0b11100, 0b11110, 0b11110, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111)
    bot_right = (0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11110, 0b11110, 0b11100)
    bot_left = (0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b01111, 0b01111, 0b00111)

    lcd.create_char(0, top_line)
    lcd.create_char(1, bottom_line)
    lcd.create_char(2, both_lines)
    lcd.create_char(3, dot)
    lcd.create_char(4, up_left)
    lcd.create_char(5, up_right)
    lcd.create_char(6, bot_right)
    lcd.create_char(7, bot_left)

    #main loop
    while True:
        counter += 1
        new_time = datetime.now().strftime('%H%M%d')
        month = datetime.now().strftime('%B')
        day_name = datetime.now().strftime('%A')

        # time changed, update LCD buffer
        if new_time!=old_time :
            digits = str(new_time)
            tens_hour = disp_number(digits[0], 0)
            hour = disp_number(digits[1], 4)
            tens_minutes = disp_number(digits[2], 9)
            minutes = disp_number(digits[3], 13)
            old_time = new_time

            cur_hour = int(tens_hour)*10 + int(hour)
            # enable backlight by night
            lcd.set_backlight(cur_hour>=19 or cur_hour<9)

        # dots blink
        clock_dots()
        
        if counter==15 :
            counter=0
            # date display
            clock_date(digits, month, day_name)
            # temperature display
            clock_temp()
            # temperature display
            clock_hour(digits)


if __name__ == '__main__':

  lcd = CharLCD(address=0x3F, port=1, cols=16, rows=2, dotsize=8)

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd.clear()
    lcd.set_backlight(False)
    lcd.home()
