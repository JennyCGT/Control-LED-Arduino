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
look= Lock()

# Global Parametes
start_serial = False
stop_threads = False
stop_threads_1 = False
flag_data=False
flag_save= False
line =1
event = Event()
global frame

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
        # Thread for reading serial Port
        self.t1 = Thread(target = self.loop)
        self.t1.start()

    def loop (self):
        while True:
            global stop_threads, frame, event
            if stop_threads: 
                break      
            self.data = bytes(frame.value_led)
            self.ser.write(self.STX)
            self.ser.write(self.data)
            self.ser.write(self.ETX)
        self.ser.close()    
    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication([])
    frame = Screen()
    app.exec_()
    stop_threads = True 

