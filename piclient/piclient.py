#!/usr/bin/python3

import serial
import time
import calendar

import serial_scan

def getnow():
    return calendar.timegm(time.gmtime())

wave_size = 2048
    
heart_state = {
    'wave' : {
        'size' : wave_size,
        'curr' : 0,
        'data' : [0] * wave_size,
    },
    'bpm' : {
        'last' : 0,
        'value': 0,
    },
    'ibi' : {
        'last' : 0,
        'value': 0,
    },
}

def update(inbytes):
    instr = inbytes.decode('ascii')
    if len(instr) > 1:
        info_type = instr[0]
        number = int(instr[1:])
        if info_type == 'S':
            curr = heart_state['wave']['curr']
            heart_state['wave']['data'][curr] = number
            curr += 1
            if curr >= heart_state['wave']['size']:
                curr = 0
            heart_state['wave']['curr'] = curr
        elif info_type == 'B':
            heart_state['bpm'] = {
                'last': getnow(),
                'value': number,
            }
        elif info_type == 'Q':
            heart_state['ibi'] = {
                'last': getnow(),
                'value': number,
            }

def main():
    scanner = serial_scan.SerialScanner('/dev/ttyACM0')
    ct = 0
    while ct < 10000:
        res = scanner.scan()
        if res is not None:
            update(res)
            print(res)
        ct += 1
    print(heart_state)

if __name__ == '__main__':
    main()

