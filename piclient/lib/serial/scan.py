#!/usr/bin/python3

import serial

class SerialScanner(object):
    def __init__(self,port,speed=115200):
        self.line = b''
        ser = serial.Serial(
            port = port,
            baudrate = speed,
            parity = serial.PARITY_NONE,
            stopbits = serial.STOPBITS_ONE,
            bytesize = serial.EIGHTBITS,
        )
        if ser.isOpen():
            print("Serial is open.");
        self.ser = ser

    def __exit__(self):
        self.ser.close()

    def bytes2data(self, inbytes):
        instr = inbytes.decode('ascii')
        rv = None
        if len(instr) > 1:
            info_type = instr[0]
            info_num = -1;
            try:
              info_num = int(instr[1:])
            except:
              print('decode err:' + instr)

            rv = { 
                'type': info_type,
                'value': info_num,
            }
        return rv

    def scan(self):
        lines = []
        while self.ser.inWaiting():
            b = self.ser.read(1)
            if b == b'\r':
                pass
            elif b == b'\n':
                out = self.line
                self.line = b''
                lines.append(out)
            else:
                self.line += b

        return_list = []

        for line in lines:
            decoded = self.bytes2data(line)
            if decoded is not None:
                return_list.append(decoded)

        return return_list 
 
    
