#!/usr/bin/env python

import serial
import time
import datetime
from struct import *

def hexdump(s):
    print hexdump_str(s)

def hexdump_str(s):
    result = []
    for ch in s:
        b = unpack('B', ch)[0]
        result.append('{0:0>2X}'.format(b))
    return ' '.join(result)

class UnknownState(Exception):
    pass

class FPlugDevice:
    
    def __init__(self, port, timeout = 10):
        self.port = port
        self.sfile = serial.Serial(self.port, 9600, timeout = timeout)
        self.tid = 100
        self.debug = True
        self.sfile.sendBreak(1.0)


    def read(self, nmax, nthru = 0):
        if nthru:
            thrustr = self.sfile.read(nthru)
            if self.debug:
                print "READ thru:", hexdump_str(thrustr)
            if len(thrustr) < nthru:
                return None
        rstr = self.sfile.read(nmax)
        if self.debug:
            print "READ:", hexdump_str(rstr)
        return rstr

    def read_byte(self, nthru = 0):
        ch = self.read(1, nthru)
        if ch:
            return unpack('B', ch)[0]
        else:
            return None
            
    def read_format(self, fmt, nthru = 0):
        sz = calcsize(fmt)
        read_data = self.read(sz, nthru = nthru)
        if len(read_data) < sz:
            return None
        return unpack(fmt, read_data)

    def send_command(self, fmt, **params):
        self.tid += 1
        byte_template = fmt.split(' ')
        fmt = ""
        data = []
        for elem in byte_template:
            if ':' in elem:
                varname, fmtchar = elem.split(':')
                fmt += fmtchar
                data.append(params[varname])
            elif len(elem) == 2:
                fmt += 'B'
                data.append(int(elem, 16))
            elif len(elem) == 4:
                fmt += 'H'
                data.append(int(elem, 16))
            else:
                raise Exception('Unknown format')
        print "packing:", (fmt, data)
        self.sfile.write(pack(fmt, *data))

    def plug_init(self):
        now = datetime.datetime.now()
        self.send_command(
            "10 81 tid:H 0E F0 00 00 22 00 61 02 97 02 hour:B minute:B 98 04 year:H month:B day:B",
            tid = self.tid,
            hour = now.hour,
            minute = now.minute,
            year = now.year,
            month = now.month,
            day = now.day
        )
        esv = self.read_byte(nthru = 10)
        if esv == 0x71:
            self.read(5)
            return True
        elif esv == 0x51:
            self.read(11)
            return False
        else:
            raise UnknownState("ESV={0}".format(esv))
        
    def get_acc_watt(self):
        now = datetime.datetime.now()
        self.send_command(
            "10 82 tid:H 11 hour:B minute:B year:H month:B day:B",
            tid = self.tid,
            hour = now.hour,
            minute = now.minute,
            year = now.year,
            month = now.month,
            day = now.day
        )
        is_fail = self.read_byte(nthru = 5)
        result = []
        for i in range(24):
            p, err = self.read_format('HB')
            if err:
                result.append(None)
            else:
                result.append(p)
        if is_fail:
            return None
        return result
        
    def get_temp(self):
        self.send_command("10 81 tid:H 0E F0 00 00 11 00 62 01 E0 00", tid =  0)
        esv = self.read_byte(10)
        if esv == 0x72:
            _opc, _epc1, _pdc1, value = self.read_format('BBBH')
            return value
        elif esv == 0x52:
            self.read(3)
            return None
        else:
            raise UnknownState("ESV = {0}".format(esv))
        
    
    def dump_all(self):
        while True:
            wlen = self.sfile.inWaiting()
            if wlen == 0:
                time.sleep(1)
                continue
            
            hexdump(self.sfile.read(wlen))
    
    def set_led(self, state = 0):
        self.send_command('05 state:B', state = state)
        _rk, result = self.read_format('BB')
        return result

    def led_on(self):
        self.set_led(1)

    def led_off(self):
        self.set_led(0)


    def set_datetime(self, dt = None):
        if not dt:
            dt = datetime.datetime.now()
        self.send_command(
            "07 hour:B minute:B year:H month:B day:B",
            hour = dt.hour,
            minute = dt.minute,
            year = dt.year,
            month = dt.month,
            day = dt.day - 5
        )
        is_fail = self.read_byte(nthru = 1)
        if is_fail == 0:
            return True
        elif is_fail == 1:
            return False
        else:
            raise UnknownState()
        

dev = FPlugDevice('/dev/rfcomm0')
print "on:", dev.led_on()
time.sleep(1)
print "off:", dev.led_off()
time.sleep(1)
print "TEMP:", dev.get_temp()
time.sleep(1)
print "result:", dev.set_datetime()
time.sleep(1)
print "init:", dev.plug_init()
time.sleep(1)
print "ACC:", dev.get_acc_watt()



