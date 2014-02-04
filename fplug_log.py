#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
F-Plug Logger

Copyright (C) 2014 SUNAGA Takahiro

This software is released under the MIT License.
http://opensource.org/licenses/mit-license.php
"""

import pyfplug
import sys
import threading
import time


duration = 2.0

fdev = pyfplug.FPlugDevice('/dev/rfcomm0')

fdev.led_on()
time.sleep(0.5)
fdev.led_off()

    
def print_now_data():
    print "{time},{temperature},{humidity},{illuminance},{power}".format(time = time.time(), **fdev.get_data_dict())
    sys.stdout.flush()


def main():
    assert duration >= 1.0
    next_time = time.time()
    while True:
        try:
            print_now_data()
        except UnknownState:
            time.sleep(duration)
            fdev.clear()
            next_time = next_time + duration
        next_time = next_time + duration
        if next_time - time.time() < 0:
            print >>sys.stderr,  "Error: Too short duration"
            continue
        time.sleep(next_time - time.time())

if __name__ == '__main__':
    main()
