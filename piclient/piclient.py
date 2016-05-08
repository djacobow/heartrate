#!/usr/bin/python3

from PyQt4 import QtGui
from PyQt4 import QtCore

import sys
import gui_form
import uuid
import time
import calendar
import copy
import serial_scan

wave_size = 128 
    
def getnow():
    return calendar.timegm(time.gmtime())

heart_state = {
    'wave' : {
        'size' : wave_size,
        'curr' : 0,
        'data' : [0] * wave_size,
        'stable_data' : [0] * wave_size,
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
        # print("instr " + instr)
        info_type = instr[0]
        number = int(instr[1:])
        if info_type == 'S':
            curr = heart_state['wave']['curr']
            heart_state['wave']['data'][curr] = number
            curr += 1
            if curr >= heart_state['wave']['size']:
                curr = 0
                heart_state['wave']['stable_data'] = copy.copy(heart_state['wave']['data'])
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


class MyApp(QtGui.QMainWindow,gui_form.Ui_MainWindow):
    def __init__(self, QApp, parent=None):
        super(MyApp, self).__init__(parent)
        self.setupUi(self)
        self.exitButton.clicked.connect(self.quit)
        self.startButton.clicked.connect(self.start_scan)
        sertimer = self.sertimer = QtCore.QTimer()
        sertimer.timeout.connect(self.scan_tick)
        sertimer.start(100)
        disptimer = self.disptimer = QtCore.QTimer()
        disptimer.timeout.connect(self.redisp)
        disptimer.start(2000)

        self.QApp = QApp
        self.ser_scanner = None
        self.nameLineEdit.insert(str(uuid.uuid4()))


    def quit(self):
        if self.ser_scanner is not None:
            del self.ser_scanner
        self.QApp.quit()
    def start_scan(self):
        if self.ser_scanner is not None:
            del self.ser_scanner
            self.ser_scanner = None
        self.ser_scanner = serial_scan.SerialScanner('/dev/ttyACM0')
    def scan_tick(self):
        if self.ser_scanner is not None:
            blobs = self.ser_scanner.scan()
            for blob in blobs:
                update(blob)
    def redisp(self):
        now = getnow()
        age = now - heart_state['bpm']['last']
        if age < 3:
            self.lcdNumber.show()
            self.lcdNumber.display(heart_state['bpm']['value'])
        else:
            self.lcdNumber.hide()
        self.draw_wave()

    def draw_wave(self):
        gv = self.graphicsView
        scene = QtGui.QGraphicsScene(gv)
        sc_height = 150 #scene.height()
        sc_width  = 720 #scene.width()
        dt_len = len(heart_state['wave']['data'])
        max_v = heart_state['wave']['stable_data'][0]
        min_v = heart_state['wave']['stable_data'][0]
        last_x_loc = -1
        last_y_loc = -1
        for idx in range(0, dt_len):
            val = heart_state['wave']['stable_data'][idx]
            if val > max_v:
                max_v = val
            if val < min_v:
                min_v = val

        print("max_v " + str(max_v) + " min_v " + str(min_v))
        print("sc_width " + str(sc_width) + " sc_height" + str(sc_height))
        if max_v != min_v:           
            for idx in range(0, dt_len):
                x_loc = 10 + int(float(sc_width) * float(idx) / float(dt_len))
                val = heart_state['wave']['stable_data'][idx]
                y_loc = 0 + int(float(sc_height) *
                             (float(val) - float(min_v)) /
                             (float(max_v) - float(min_v))
                            )
                if last_x_loc >= 0:
                    line = QtGui.QGraphicsLineItem(last_x_loc,last_y_loc,x_loc,y_loc)
                    # print("idx " + str(idx) + " xl " + str(x_loc) + " yl " + str(y_loc))
                    scene.addItem(line)
                last_x_loc = x_loc
                last_y_loc = y_loc
                    
        gv.setScene(scene)
        gv.show()




def main():
    app = QtGui.QApplication(sys.argv)
    form = MyApp(app)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()

