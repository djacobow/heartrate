#!/usr/bin/python3

import sys
import datetime

from lib.serial import scan
from lib.server import push

config = {
    'serial': {
        'port': '/dev/ttyACM0',
        'speed': 115200,
    },
    'server': {
        'name': '52.34.85.6',
        'port': 8000,
        'username': 'bob',
    },
    'logfilename': 'heartrate.log',
    'todo': {
        'show_raw_decoded': False,
        'show_heartrate': True,
        'log_heartrate': False,
        'send_heartrate': False,
    }
}


def main():
    scanner = scan.SerialScanner(config['serial']['port'],
                                 config['serial']['speed'])

    logfile = None
    if config['todo']['log_heartrate']:
        try:
            logfile = open(config['logfilename'],'a')
            logfile.write('time,heartrate\n')
        except:
            print('Could not open logfile.')
            return

    sender = None
    if config['todo']['send_heartrate']:
        sender = push.ServerPusher(config['server']['name'],
                                     config['server']['port'],
                                     config['server']['username'])
    while True:
        data = scanner.scan()

        for datum in data:
            if config['todo']['show_raw_decoded']:
                print('datum received:')
                print(datum)

            if config['todo']['show_heartrate']:
                if datum['type'] == 'B':
                    print('Heartrate is: ' + str(datum['value']) +
                            ' BPM')

            if logfile is not None:
                if datum['type'] == 'B':
                    time = datetime.datetime.now().isoformat()
                    bpm = datum['value']
                    logfile.write('{},{}\n'.format(time,bpm))

            if sender is not None:
                if datum['type'] == 'B':
                    push_res = sender.push({ 'bpm': datum['value'] })
                    if push_res != 'ok':
                        print(push_res)
                    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

