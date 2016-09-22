#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from RPLCD_i2c import CharLCD
from RPLCD_i2c import Alignment, CursorMode, ShiftMode
from RPLCD_i2c import cursor, cleared

try:
    input = raw_input
except NameError:
    pass

try:
    unichr = unichr
except NameError:
    unichr = chr


lcd = CharLCD(address=0x3F, port=1, cols=16, rows=2, dotsize=8)

input('Display should be blank. ')

lcd.cursor_mode = CursorMode.blink
input('The cursor should now blink. ')

lcd.cursor_mode = CursorMode.line
input('The cursor should now be a line. ')

lcd.write_string('Hello world!')
input('"Hello world!" should be on the LCD. ')

assert lcd.cursor_pos == (0, 12), 'cursor_pos should now be (0, 12)'

lcd.cursor_pos = (1, 0)
lcd.write_string('2')
assert lcd.cursor_pos == (1, 1), 'cursor_pos should now be (2, 1)'
input('Lines 2, should now be labelled with the right number. ')

lcd.clear()
input('Display should now be clear, cursor should be at initial position. ')

lcd.cursor_pos = (0, 5)
lcd.write_string('12345')
input('The string should have a left offset of 5 characters. ')

lcd.write_shift_mode = ShiftMode.display
lcd.cursor_pos = (1, 5)
lcd.write_string('12345')
input('Both strings should now be at column 0. ')

lcd.write_shift_mode = ShiftMode.cursor
lcd.cursor_pos = (0, 5)
lcd.write_string(lcd.write_shift_mode.name)
input('The string "cursor" should now be on the first row, column 0. ')

lcd.home()
input('Cursor should now be at initial position. Everything should be shifted to the right by 5 characters. ')

with cursor(lcd, 1, 15):
    lcd.write_string('X')
input('The last character on the LCD should now be an "X"')

lcd.display_enabled = False
input('Display should now be blank. ')

with cleared(lcd):
    lcd.write_string('Eggs Ham Bacon\n\rand Spam')
lcd.display_enabled = True
input('Display should now show "Eggs Ham Bacon and Spam". ')

lcd.shift_display(4)
input('Text should now be shifted to the right by 4 characters. ')
lcd.shift_display(-4)
input('Shift should now be undone. ')

lcd.text_align_mode = Alignment.right
lcd.cursor_mode = CursorMode.hide
lcd.write_string(' Spam')
input('The word "Spam" should now be inverted. ')

lcd.text_align_mode = Alignment.left
lcd.cursor_mode = CursorMode.hide
lcd.write_string(' Wurscht')
input('The word "mapS" should now be replaced with "Wurscht". ')

lcd.clear()
lcd.write_string('1\n')
lcd.write_string('2')
input('The numbers 1-2 should now be displayed, each line shifted to the right by 1 char more than the previous. ')

lcd.clear()
lcd.write_string('This is a multiple line string!')
input('Text should nicely wrap around lines. ')

lcd.cursor_mode = CursorMode.hide

# Test custom chars
lcd.clear()
happy = (0b00000, 0b01010, 0b01010, 0b00000, 0b10001, 0b10001, 0b01110, 0b00000)
sad = (0b00000, 0b01010, 0b01010, 0b00000, 0b01110, 0b10001, 0b10001, 0b00000)
lcd.create_char(0, sad)
lcd.write_string(unichr(0))
lcd.create_char(1, happy)
lcd.write_string(unichr(1))
input('You should now see a sad and a happy face next to each other. ')
lcd.create_char(0, happy)
lcd.home()
lcd.write_string(unichr(0))
input('Now both faces should be happy. ')

lcd.clear()
lcd.set_backlight(False)
lcd.home()
lcd.write_string('No backlight')
input('Display backlight should be off (if wired). ')

lcd.clear()
lcd.set_backlight(True)
lcd.home()
lcd.write_string('Backlight')
input('Display backlight should be back on (if wired). ')

lcd.clear()
print('Test done.')
