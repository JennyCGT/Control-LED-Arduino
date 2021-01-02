from PyQt5 import QtWidgets
import serial
import sys
import glob
import os
import struct   
import json
from csv import writer
import serial.tools.list_ports
from datetime import datetime, timedelta
from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,QSlider,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMainWindow, QFontComboBox,QMessageBox)
from PyQt5.QtGui import QFont,QPixmap
from PyQt5 import QtCore
from PyQt5.QtSerialPort import QSerialPortInfo
import signal
global settings
with open ('settings.json') as _file:
    settings = json.loads(_file.read())

class Screen(QWidget):
    def __init__(self, parent = None):
        super(Screen, self).__init__(parent)
        self.port_selec=''
        self.baud_selec='115200'
        self.choices=[]
        self.y_max = 100
        self.y_min = 0
        self.value_led=0
        grid = QGridLayout()
        self.setLayout(grid)

        title = QLabel("        Brightness Controller      ")
        title.setFont(QFont("Times",23,weight=QFont.Bold))

        grid.addWidget(title,0,0)
        grid.addWidget(self.serial_settings(), 1, 0)
        grid.addWidget(self.slider_bar(), 2,0)
        grid.addWidget(self.values_box(),3,0,2,1)
        # grid.setColumnStretch(0, 4)        
        # grid.setRowStretch(0, 3)
        self.setWindowTitle('Brightness Controller')
        self.show()

    ############ SERIAL SETTINGS
    def serial_settings(self):
        self.box_serial = QGroupBox("Serial Settings")
        text_port = QLabel("Port")        
        self.port = QComboBox()
        # self.port.addItem("Choose a Port")
        if(settings['port'] == ""):
            self.port_selec =""
            self.port.addItem("Choose a Port")
        else:
            self.port_selec = settings['port']
        self.ports = list(serial.tools.list_ports.comports())
        for i in self.ports:
            self.port.addItem(i.device)

        self.port.activated.connect(self.selec_port)
    
        text_baud = QLabel("Baudrate")
        self.baud = QComboBox()
        self.baud_array=['2400','4800','9600','19200','38400','57600','74880'
        ,'115200','230400', '460800']
        for i in self.baud_array:
            self.baud.addItem(i)
        self.baud.setCurrentIndex(7 )
        self.baud.activated.connect(self.selec_baud)
        
        self.connect_button = QPushButton('Connect')
        self.connect_button.clicked.connect(self.onConnect)

        b1 = QHBoxLayout()
        b1.addStretch(1)
        b1.addWidget(text_port)
        b1.addWidget(self.port)
        b1.addStretch(1)
        b1.addWidget(text_baud)
        b1.addWidget(self.baud)
        b1.addStretch(2)
        b1.addWidget(self.connect_button) 
        
        # self.box_serial.setStyleSheet("background-color: #F1F7EE")
        self.box_serial.setLayout(b1)
        return self.box_serial
    
    ############ SLIDER BAR
    def slider_bar(self):
        self.box_slider = QGroupBox("Slider Controller")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)        
        self.slider.valueChanged.connect(self.get_value)
        size = self.slider.size()
        print(size)

        self.icon = QLabel(self)
        image = QPixmap('image\empty.png')
        self.icon.setPixmap(image.scaled(30,30))
        # self.icon.setSize(20  0,200)

        self.value_data = QLabel(str(self.value_led))
        self.value_data.setStyleSheet("background-color:#F1F7EE")
        self.value_data.setAlignment(Qt.AlignCenter)
        self.value_data.setFont(QFont("Times",20))
        # self.value_data.setFont(QFont("Times",23,weight=QFont.Bold))

        b1 = QHBoxLayout()
        b1.addWidget(self.icon)
        b1.addSpacing(20)
        b1.addWidget(self.slider)
        b1.addSpacing(60)
        b1.addWidget(self.value_data)


        b3 = QVBoxLayout()
        b3.addLayout(b1)
        self.box_slider.setLayout(b3)
        return self.box_slider


        # List COM availables 

    ############ VALUES ON CHANGE
    def values_box(self):
        self.normal_value = QSpinBox()
        self.normal_value.setRange(0,100)
        self.normal_value.setSingleStep(10)
        self.normal_value.setAlignment(Qt.AlignHCenter)
        self.normal_value.setFont(QFont("Times",15))
        self.normal_value.valueChanged.connect(self.get_value_box)
        # self.normal_value.setFont(QFont("Times",15,weight=QFont.Bold))

        self.value_data_s = QLabel("00")
        self.value_data_s.setStyleSheet("background-color:#F1F7EE")
        self.value_data_s.setAlignment(Qt.AlignHCenter)
        self.value_data_s.setFont(QFont("Times",15))

        title = QLabel("Brightness value")
        title.setFont(QFont("Times",13, weight= QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        title2 = QLabel("Brightness value in sec")
        title2.setFont(QFont("Times",13, weight= QFont.Bold))
        title2.setAlignment(Qt.AlignHCenter)

        self.box_slider = QGroupBox("Value Controller")
        b1 = QHBoxLayout()
        b1.addWidget(self.normal_value)
        # b1.addStretch(1)
        b1.addWidget(self.value_data_s)

        b2 = QHBoxLayout()
        b2.addWidget(title)
        # b2.addStretch(1)
        b2.addWidget(title2)

        b3 = QVBoxLayout()
        b3.addLayout(b2)
        b3.addSpacing(10)
        b3.addLayout(b1)

        self.box_slider.setLayout(b3)
        return self.box_slider

    def List_port(self):
        self.port.clear()
        ports = list(serial.tools.list_ports.comports())
        lst = []
        for p in ports:
            self.port.addItem(p.device)

    # Get de Baudrate selected
    def selec_baud(self,text):
        self.baud_selec = self.baud.currentText() 
    
    # Get Port Selected 
    def selec_port(self,text):
        self.port_selec = self.port.itemText(text)
        settings['port']= self.port_selec
        with open ('settings.json','w') as _file:
            json.dump(settings,_file)

    # Start thread of Serial Communication
    def onConnect(self, event):
        # Detect if the port was selected
        if self.connect_button.text()=='Connect':
            if(self.port_selec == '' or self.port_selec == 'Choose a port'):
                self.showDialog()
            else:
                # Start Serial protocol
                self.connect_button.setText('Disconnect')
                # Disable the options for port and baudrate
                self.port.setDisabled(True)
                self.baud.setDisabled(True)
                flag_data = True
        else:
            self.connect_button.setText('Connect')
            stop_threads = True
            flag_data = False
            self.ser_msg.setText("Close")            
            self.port.setDisabled(False)
            self.baud.setDisabled(False)

    # Get slider number 
    def get_value(self, event):
        self.value_led = self.slider.value()
        self.value_data.setText(str(self.value_led))
        self.normal_value.setValue(self.value_led)
        self.value_data_s.setText(str(self.value_led/100)+" s")
        print(self.value_led)

    # Get box values
    def get_value_box(self, event):
        self.value_box = self.normal_value.value()
        self.slider.setValue(self.value_box)
        self.value_data_s.setText(str(self.value_box/100)+" s")


# if __name__ == "__main__":
#     signal.signal(signal.SIGINT, signal.SIG_DFL)
#     app = QApplication([])
#     frame = Screen()
#     app.exec_()

    








