#!/usr/bin/python3

import sys
import datetime
import math
import yaml

from lib.serial import scan
from lib.server import push

config = None 

with open('config.json','r') as cfile:
    try:
        config = yaml.load(cfile)
    except yaml.YAMLError as exc:
        print(exc)

print(config)


if len(sys.argv) > 1:
    config['shared']['serial']['port'] = sys.argv[1]

def main():
    scanner = scan.SerialScanner(config['shared']['serial']['port'],
                                 config['shared']['serial']['speed'])

    logfile = None
    if config['piclient_simple']['todo']['log_heartrate']:
        try:
            logfile = open(config['piclient_simple']['logfilename'],'a')
            logfile.write('time,heartrate\n')
        except:
            print('Could not open logfile.')
            return

    sender = None
    if config['piclient_simple']['todo']['send_heartrate']:
        sender = push.ServerPusher(config['shared']['server']['name'],
                                     config['shared']['server']['port'],
                                     config['shared']['server']['username'])
    while True:
        data = scanner.scan()

        for datum in data:
            if config['piclient_simple']['todo']['show_raw_decoded']:
                print('datum received:')
                print(datum)

            if config['piclient_simple']['todo']['show_heartrate']:
                if datum['type'] == 'B':
                    print('Heartrate is: ' + str(datum['value']) +
                            ' BPM')

            if config['piclient_simple']['todo']['show_better_heartrate']:
                if datum['type'] == 'Q':
                    ibi = datum['value']
                    hr = math.floor((600000.0 / float(ibi)) + 0.5) / 10.0;
                    print('IBI-based Heartrate is: ' + str(hr))
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

