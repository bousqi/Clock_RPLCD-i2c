#!/usr/bin/env python
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

import sys

from RPLCD_i2c import CharLCD


try:
    range = xrange
except NameError:  # Python 3
    pass

try:
    safe_input = raw_input
except NameError:  # Python 3
    safe_input = input

try:
    unichr = unichr
except NameError:  # Python 3
    unichr = chr


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: %s <rows> <cols>' % sys.argv[0])
        sys.exit(1)

    rows, cols = int(sys.argv[1]), int(sys.argv[2])
    lcd = CharLCD(address=0x3F, port=1, cols=cols, rows=rows, dotsize=8, ignore_special=True)

    print('This tool shows the character map of your LCD on the display.')
    print('Press ctrl+c at any time to abort.\n')

    page = 0
    chars_per_page = rows * cols

    try:
        while True:
            page_start = page * chars_per_page
            page_end = page_start + chars_per_page
            if page_end > 256:
                page_end = 256
            lcd.clear()
            print('Displaying page %d (characters %d-%d).' %
                       (page, page_start, page_end - 1))
            for i in range(page_start, page_end):
                if i < 255:
                    lcd.write_string(unichr(i))
                else:
                    lcd.write_string(unichr(i))
                    safe_input('Press <ENTER> to exit.')
                    lcd.clear()
                    sys.exit(0)
            page += 1
            safe_input('Press <ENTER> to continue.')
    except KeyboardInterrupt:
        print('Aborting.')

    lcd.clear()
