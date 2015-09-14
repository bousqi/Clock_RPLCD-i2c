# -*- coding: utf-8 -*-
"""
Copyright (C) 2013-2015 Danilo Bargen

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from __future__ import print_function, division, absolute_import, unicode_literals

import time
from collections import namedtuple

from smbus import SMBus

from . import enum

### PYTHON 3 COMPAT ###

try:
    range = xrange
except NameError:
    pass


### BIT PATTERNS ###

# Commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# Flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# Flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00

# Flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00

# Flags for function set
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00

# Flags for RS pin modes
RS_INSTRUCTION = 0x00
RS_DATA = 0x01

PIN_E = 0x4
PIN_RW = 0x2
PIN_RS = 0x1

### NAMEDTUPLES ###

LCDConfig = namedtuple('LCDConfig', 'rows cols dotsize')

### ENUMS ###

class Alignment(enum.Enum):
    left = LCD_ENTRYLEFT
    right = LCD_ENTRYRIGHT


class ShiftMode(enum.Enum):
    cursor = LCD_ENTRYSHIFTDECREMENT
    display = LCD_ENTRYSHIFTINCREMENT


class CursorMode(enum.Enum):
    hide = LCD_CURSOROFF | LCD_BLINKOFF
    line = LCD_CURSORON | LCD_BLINKOFF
    blink = LCD_CURSOROFF | LCD_BLINKON


### HELPER FUNCTIONS ###

def msleep(milliseconds):
    """Sleep the specified amount of milliseconds."""
    time.sleep(milliseconds / 1000.0)


def usleep(microseconds):
    """Sleep the specified amount of microseconds."""
    time.sleep(microseconds / 1000000.0)


### MAIN ###

class CharLCD(object):

    # Init, setup, teardown
    #TODO: Change signature
    def __init__(self, address, port = 1, cols=20, rows=4, dotsize=8, auto_linebreaks=True):
        """
        Character LCD controller.

        Args:
            address:
                Address on i2c bus
            port:
                i2c port
            rows:
                Number of display rows (usually 1, 2 or 4). Default: 4.
            cols:
                Number of columns per row (usually 16 or 20). Default 20.
            dotsize:
                Some 1 line displays allow a font height of 10px.
                Allowed: 8 or 10. Default: 8.
            auto_linebreaks:
                Whether or not to automatically insert line breaks.
                Default: True.

        Returns:
            A :class:`CharLCD` instance.

        """
        assert dotsize in [8, 10], 'The ``dotsize`` argument should be either 8 or 10.'

        self.lcd = LCDConfig(rows=rows, cols=cols, dotsize=dotsize)

        # Setup GPIO
        self.address = address
        self.port = port

        self.bus = SMBus(self.port)
        msleep(50)

        # Setup initial display configuration
        displayfunction = LCD_4BITMODE | LCD_5x8DOTS
        if rows == 1:
            displayfunction |= LCD_1LINE
        elif rows in [2, 4]:
            # LCD only uses two lines on 4 row displays
            displayfunction |= LCD_2LINE
        if dotsize == 10:
            # For some 1 line displays you can select a 10px font.
            displayfunction |= LCD_5x10DOTS

        # Create content cache
        self._content = [[0x20] * cols for _ in range(rows)]

        # Set up auto linebreaks
        self.auto_linebreaks = auto_linebreaks
        self.recent_auto_linebreak = False

        # Initialization
        msleep(50)

        # Hitachi manual page 46
        # 4 bit mode
        self._write4bits(0x03)
        msleep(4.5)
        self._write4bits(0x03)
        msleep(4.5)
        self._write4bits(0x03)
        usleep(100)
        self._write4bits(0x02)

        # Write configuration to display
        self.command(LCD_FUNCTIONSET | displayfunction)
        usleep(50)

        # Configure display mode
        self._display_mode = LCD_DISPLAYON
        self._cursor_mode = int(CursorMode.hide)
        self.command(LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        usleep(50)

        # Clear display
        self.clear()

        # Configure entry mode
        self._text_align_mode = int(Alignment.left)
        self._display_shift_mode = int(ShiftMode.cursor)
        self._cursor_pos = (0, 0)
        self.command(LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        usleep(50)

    def close(self, clear=False):
        if clear:
            self.clear()


    # Properties

    def _get_cursor_pos(self):
        return self._cursor_pos

    def _set_cursor_pos(self, value):
        if not hasattr(value, '__getitem__') or len(value) != 2:
            raise ValueError('Cursor position should be determined by a 2-tuple.')
        if value[0] not in range(self.lcd.rows) or value[1] not in range(self.lcd.cols):
            msg = 'Cursor position {pos!r} invalid on a {lcd.rows}x{lcd.cols} LCD.'
            raise ValueError(msg.format(pos=value, lcd=self.lcd))
        row_offsets = [0x00, 0x40, self.lcd.cols, 0x40 + self.lcd.cols]
        self._cursor_pos = value
        self.command(LCD_SETDDRAMADDR | row_offsets[value[0]] + value[1])
        usleep(50)

    cursor_pos = property(_get_cursor_pos, _set_cursor_pos,
            doc='The cursor position as a 2-tuple (row, col).')

    def _get_text_align_mode(self):
        try:
            return Alignment[self._text_align_mode]
        except ValueError:
            raise ValueError('Internal _text_align_mode has invalid value.')

    def _set_text_align_mode(self, value):
        if value not in Alignment:
            raise ValueError('Cursor move mode must be of ``Alignment`` type.')
        self._text_align_mode = int(value)
        self.command(LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        usleep(50)

    text_align_mode = property(_get_text_align_mode, _set_text_align_mode,
            doc='The text alignment (``Alignment.left`` or ``Alignment.right``).')

    def _get_write_shift_mode(self):
        try:
            return ShiftMode[self._display_shift_mode]
        except ValueError:
            raise ValueError('Internal _display_shift_mode has invalid value.')

    def _set_write_shift_mode(self, value):
        if value not in ShiftMode:
            raise ValueError('Write shift mode must be of ``ShiftMode`` type.')
        self._display_shift_mode = int(value)
        self.command(LCD_ENTRYMODESET | self._text_align_mode | self._display_shift_mode)
        usleep(50)

    write_shift_mode = property(_get_write_shift_mode, _set_write_shift_mode,
            doc='The shift mode when writing (``ShiftMode.cursor`` or ``ShiftMode.display``).')

    def _get_display_enabled(self):
        return self._display_mode == LCD_DISPLAYON

    def _set_display_enabled(self, value):
        self._display_mode = LCD_DISPLAYON if value else LCD_DISPLAYOFF
        self.command(LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        usleep(50)

    display_enabled = property(_get_display_enabled, _set_display_enabled,
            doc='Whether or not to display any characters.')

    def _get_cursor_mode(self):
        try:
            return CursorMode[self._cursor_mode]
        except ValueError:
            raise ValueError('Internal _cursor_mode has invalid value.')

    def _set_cursor_mode(self, value):
        if value not in CursorMode:
            raise ValueError('Cursor mode must be of ``CursorMode`` type.')
        self._cursor_mode = int(value)
        self.command(LCD_DISPLAYCONTROL | self._display_mode | self._cursor_mode)
        usleep(50)

    cursor_mode = property(_get_cursor_mode, _set_cursor_mode,
            doc='How the cursor should behave (``CursorMode.hide``, ' +
                                   '``CursorMode.line`` or ``CursorMode.blink``).')

    # High level commands

    def write_string(self, value):
        """Write the specified unicode string to the display.

        To control multiline behavior, use newline (\n) and carriage return
        (\r) characters.

        Lines that are too long automatically continue on next line, as long as
        ``auto_linebreaks`` has not been disabled.

        Make sure that you're only passing unicode objects to this function. If
        you're dealing with bytestrings (the default string type in Python 2),
        convert it to a unicode object using the ``.decode(encoding)`` method
        and the appropriate encoding. Example for UTF-8 encoded strings:

        .. code::

            >>> bstring = 'Temperature: 30°C'
            >>> bstring
            'Temperature: 30\xc2\xb0C'
            >>> bstring.decode('utf-8')
            u'Temperature: 30\xb0C'

        Only characters with an ``ord()`` value between 0 and 255 are currently
        supported.

        """
        ignored = None  # Used for ignoring manual linebreaks after auto linebreaks
        for char in value:
            # Write regular chars
            if char not in '\n\r':
                self.write(ord(char))
                ignored = None
                continue
            # If an auto linebreak happened recently, ignore this write.
            if self.recent_auto_linebreak is True:
                # No newline chars have been ignored yet. Do it this time.
                if ignored is None:
                    ignored = char
                    continue
                # A newline character has been ignored recently. If the current
                # character is different, ignore it again. Otherwise, reset the
                # ignored character tracking.
                if ignored != char:  # A carriage return and a newline
                    ignored = None  # Reset ignore list
                    continue
            # Handle newlines and carriage returns
            row, col = self.cursor_pos
            if char == '\n':
                if row < self.lcd.rows - 1:
                    self.cursor_pos = (row + 1, col)
                else:
                    self.cursor_pos = (0, col)
            elif char == '\r':
                if self.text_align_mode is Alignment.left:
                    self.cursor_pos = (row, 0)
                else:
                    self.cursor_pos = (row, self.lcd.cols - 1)

    def clear(self):
        """Overwrite display with blank characters and reset cursor position."""
        self.command(LCD_CLEARDISPLAY)
        self._cursor_pos = (0, 0)
        self._content = [[0x20] * self.lcd.cols for _ in range(self.lcd.rows)]
        msleep(2)

    def home(self):
        """Set cursor to initial position and reset any shifting."""
        self.command(LCD_RETURNHOME)
        self._cursor_pos = (0, 0)
        msleep(2)

    def shift_display(self, amount):
        """Shift the display. Use negative amounts to shift left and positive
        amounts to shift right."""
        if amount == 0:
            return
        direction = LCD_MOVERIGHT if amount > 0 else LCD_MOVELEFT
        for i in range(abs(amount)):
            self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | direction)
            usleep(50)

    def create_char(self, location, bitmap):
        """Create a new character.

        The HD44780 supports up to 8 custom characters (location 0-7).

        Args:
            location:
                The place in memory where the character is stored. Values need
                to be integers between 0 and 7.
            bitmap:
                The bitmap containing the character. This should be a tuple of
                8 numbers, each representing a 5 pixel row.

        Raises:
            AssertionError:
                Raised when an invalid location is passed in or when bitmap
                has an incorrect size.

        Example::

            >>> smiley = (
            ...     0b00000,
            ...     0b01010,
            ...     0b01010,
            ...     0b00000,
            ...     0b10001,
            ...     0b10001,
            ...     0b01110,
            ...     0b00000,
            ... )
            >>> lcd.create_char(0, smiley)

        """
        assert 0 <= location <= 7, 'Only locations 0-7 are valid.'
        assert len(bitmap) == 8, 'Bitmap should have exactly 8 rows.'

        # Store previous position
        pos = self.cursor_pos

        # Write character to CGRAM
        self.command(LCD_SETCGRAMADDR | location << 3)
        for row in bitmap:
            self._send(row, RS_DATA)

        # Restore cursor pos
        self.cursor_pos = pos

    # Mid level commands

    def command(self, value):
        """Send a raw command to the LCD."""
        self._send(value, RS_INSTRUCTION)

    def write(self, value):
        """Write a raw byte to the LCD."""

        # Get current position
        row, col = self._cursor_pos

        # Write byte if changed
        if self._content[row][col] != value:
            self._send(value, RS_DATA)
            self._content[row][col] = value  # Update content cache
            unchanged = False
        else:
            unchanged = True

        # Update cursor position.
        if self.text_align_mode is Alignment.left:
            if self.auto_linebreaks is False or col < self.lcd.cols - 1:
                # No newline, update internal pointer
                newpos = (row, col + 1)
                if unchanged:
                    self.cursor_pos = newpos
                else:
                    self._cursor_pos = newpos
                self.recent_auto_linebreak = False
            else:
                # Newline, reset pointer
                if row < self.lcd.rows - 1:
                    self.cursor_pos = (row + 1, 0)
                else:
                    self.cursor_pos = (0, 0)
                self.recent_auto_linebreak = True
        else:
            if self.auto_linebreaks is False or col > 0:
                # No newline, update internal pointer
                newpos = (row, col - 1)
                if unchanged:
                    self.cursor_pos = newpos
                else:
                    self._cursor_pos = newpos
                self.recent_auto_linebreak = False
            else:
                # Newline, reset pointer
                if row < self.lcd.rows - 1:
                    self.cursor_pos = (row + 1, self.lcd.cols - 1)
                else:
                    self.cursor_pos = (0, self.lcd.cols - 1)
                self.recent_auto_linebreak = True


    # Low level commands

    def _send(self, value, mode):
        """Send the specified value to the display with automatic 4bit / 8bit
        selection. The rs_mode is either ``RS_DATA`` or ``RS_INSTRUCTION``."""
        self._write4bits(mode | (value & 0xF0))
        self._write4bits(mode | ((value << 4) & 0xF0))


    def _write4bits(self, value):
        """Write 4 bits of data into the data bus."""
        self.bus.write_byte(self.address, value & ~PIN_RW)
        self._pulse_enable(value)

    def _pulse_enable(self, value):
        """Pulse the `enable` flag to process data."""
        self.bus.write_byte(self.address, value & ~PIN_E)
        usleep(1)
        self.bus.write_byte(self.address, value | PIN_E)
        usleep(1)
        self.bus.write_byte(self.address, value & ~PIN_E)
        usleep(100)  # commands need > 37us to settle
