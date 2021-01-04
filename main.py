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

class Serial_com:
    def __init__(self, port, baud):
        self.ser= serial.Serial(port,baud,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
        timeout=(0.5))
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
            self.data = frame.value_led.to_bytes(1,'big')
            # Send trama to arduino
            self.ser.write(self.STX)
            self.ser.write(self.data)
            self.ser.write(self.ETX)
            # Period of transmition
            time.sleep(0.1)
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


if __name__ == "__main__":
    global frame
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    frame = Screen(onConnect=onConnect)
    app.exec_()
    stop_threads = True 

