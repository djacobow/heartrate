#!/usr/bin/python3

import serial

class SerialScanner(object):
    def __init__(self,port,speed=115200):
        self.line = b''
        self.out = b''
        ser = serial.Serial(
            port = port,
            baudrate = speed,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
        )
        self.ser = ser

    def __exit__(self):
        self.ser.close()

    def scan(self):
        if self.ser.inWaiting():
            b = self.ser.read(1)
            if b == b'\r':
                pass
            elif b == b'\n':
                self.out = self.line
                self.line = b''
                return self.out
            else:
                self.line += b
        return None
    
