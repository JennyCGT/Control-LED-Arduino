from threading import Thread, Lock, Event
import time
import serial
import sys
import glob
import os
import struct   
import json
from collections import deque
import serial.tools.list_ports
from datetime import datetime, timedelta
import signal
from GUI import *
from PyQt5.QtGui import QFont,QPixmap
look= Lock()

# Global Parametes
start_serial = False
stop_threads = False
stop_threads_1 = False
flag_data=False
flag_save= False
line =1
event = Event()
global serial_p
class Serial_com:
    def __init__(self, port, baud):
        self.ser= serial.Serial(port,baud,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=(0.5))
        self.SOH = b'SOH'
        self.STX = b'STX'
        self.ETX = b'ETX'
        self.data = b'0'
        # Thread for writting serial Port
        self.t1 = Thread(target = self.loop)
        self.t1.start()

    def loop (self):
        while True:
            global stop_threads, frame, event
            if stop_threads: 
                self.ser.close()
                break 
            # Transform the value of brightness to byte
            self.data = frame.value_on.to_bytes(1,'big')
            # Send trama to arduino
            self.ser.write(self.SOH)
            self.ser.write(b'A')
            self.ser.write(self.STX)
            self.ser.write(self.data)
            self.ser.write(self.ETX)
            # Period of transmition
            time.sleep(5)
            self.data = frame.value_off.to_bytes(1,'big')
            self.ser.write(self.SOH)
            self.ser.write(b'B')
            self.ser.write(self.STX)
            self.ser.write(self.data)
            self.ser.write(self.ETX)
            time.sleep(5)

        self.ser.close()

def onConnect(event):
    global stop_threads, serial_p
    # Detect if the port was selected
    if frame.connect_button.text()=='Connect':
        if(frame.port_selec == '' or frame.port_selec == 'Choose a port'):
            frame.showDialog()
        else:
            # Start Serial protocol
            image = QPixmap('image/green-icon.png')
            frame.icon_serial.setPixmap(image)
            stop_threads = False
            frame.connect_button.setText('Disconnect')
            serial_p = Serial_com(frame.port_selec, frame.baud_selec)
            # Disable the options for port and baudrate
            frame.port.setDisabled(True)
            frame.baud.setDisabled(True)
            
    else:
        image = QPixmap('image/disconect-icon.png')
        frame.icon_serial.setPixmap(image)
        stop_threads = True
        frame.connect_button.setText('Connect')
        frame.port.setDisabled(False)
        frame.baud.setDisabled(False)


   # Get slider value ON
def get_value_on(event):
    frame.value_on = frame.slider.value()
    frame.value_data.setText(str(frame.value_on))
    frame.value_data_s.setText(str(frame.value_on/10)+" ms")
    data = frame.value_on.to_bytes(1,'big')
    # Send trama to arduino
    serial_p.ser.write(b'SOH')
    serial_p.ser.write(b'A')
    serial_p.ser.write(b'STX')
    serial_p.ser.write(data)
    serial_p.ser.write(b'ETX')

# Get slider value OFF
def get_value_off(event):
    frame.value_off = frame.slider_off.value()
    frame.value_data_1.setText(str(frame.value_off))
    frame.value_data_off_s.setText(str(frame.value_off/10)+" ms")
    data = frame.value_off.to_bytes(1,'big')
    # Send trama to arduino
    serial_p.ser.write(b'SOH')
    serial_p.ser.write(b'B')
    serial_p.ser.write(b'STX')
    serial_p.ser.write(data)
    serial_p.ser.write(b'ETX')

if __name__ == "__main__":
    global frame
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    frame = Screen(onConnect=onConnect, get_value_on= get_value_on, get_value_off= get_value_off)
    app.exec_()
    stop_threads = True 

