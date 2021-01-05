from time import sleep
from PyQt5 import QtWidgets
import serial
import sys
import json
from csv import writer
import serial.tools.list_ports
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QComboBox, QDateTimeEdit,QSlider,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel,QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QMainWindow, QFontComboBox,QMessageBox)
from PyQt5.QtGui import QFont,QPixmap

global settings
with open ('settings.json') as _file:
    settings = json.loads(_file.read())

class Screen(QWidget):
    def __init__(self , onConnect, get_value_on, get_value_off, parent = None):
        super(Screen, self).__init__(parent)
        self.onConnect = onConnect
        self.get_value_on = get_value_on
        self.get_value_off = get_value_off
        self.port_selec=''
        self.baud_selec='115200'
        self.choices=[]
        self.y_max = 100
        self.y_min = 0
        self.value_on=0
        self.value_off=100
        grid = QGridLayout()
        self.setLayout(grid)

        title = QLabel("               Brightness Controller                ")
        title.setFont(QFont("Times",23,weight=QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        grid.addWidget(title,0,0)
        grid.addWidget(self.serial_settings(), 1, 0)
        grid.addWidget(self.slider_bar(), 2,0)
        grid.addWidget(self.values_box(),3,0,2,1)
        self.setWindowTitle('Brightness Controller')
        self.show()

############ SERIAL SETTINGS
    def serial_settings(self):
        global settings
        self.box_serial = QGroupBox("Serial Settings")
        text_port = QLabel("Port")        
        self.port = QComboBox()
        if(settings['port'] == ""):
            self.port_selec =""
            self.port.addItem("Choose a Port")
        else:
            self.port_selec = settings['port']
        self.ports = list(serial.tools.list_ports.comports())
        for i in self.ports:
            self.port.addItem(i.device)
        self.port.setCurrentText(settings['port'])
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

        self.icon_serial = QLabel(self)
        image = QPixmap('image/disconect-icon.png')
        self.icon_serial.setPixmap(image)

        b1 = QHBoxLayout()
        b1.addStretch(1)
        b1.addWidget(text_port)
        b1.addWidget(self.port)
        b1.addStretch(1)
        b1.addWidget(text_baud)
        b1.addWidget(self.baud)
        b1.addStretch(2)
        b1.addWidget(self.connect_button) 
        b1.addWidget(self.icon_serial)
        
        # self.box_serial.setStyleSheet("background-color: #F1F7EE")
        self.box_serial.setLayout(b1)
        self.box_serial.setStyleSheet("background-color: #E1EFF6")
        self.box_serial.setFont(QFont("Segoe UI",12))
        return self.box_serial
    
############ SLIDER BAR ON
    def slider_bar(self):
        self.box_slider = QGroupBox("Time ON")
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)        
        self.slider.valueChanged.connect(self.get_value_on)

        self.icon = QLabel(self)
        image = QPixmap('image/full.png')
        self.icon.setPixmap(image.scaled(30,30))

        self.value_data = QLabel(str(self.value_on))
        self.value_data.setStyleSheet("background-color:#F1F7EE")
        self.value_data.setAlignment(Qt.AlignCenter)
        self.value_data.setFont(QFont("Segoe UI",16))

        title2 = QLabel("Time in ms")
        title2.setFont(QFont("Segoe UI",12, weight= QFont.Bold))
        title2.setAlignment(Qt.AlignCenter)
        self.value_data_s = QLabel("0.0")
        self.value_data_s.setStyleSheet("background-color:#F1F7EE")
        self.value_data_s.setAlignment(Qt.AlignCenter)
        self.value_data_s.setFont(QFont("Segoe UI",16))


        b1 = QHBoxLayout()
        b1.addWidget(self.icon)
        b1.addSpacing(20)
        b1.addWidget(self.slider)
        b1.addSpacing(50)
        b1.addWidget(self.value_data)

        b2 = QVBoxLayout()
        b2.addWidget(title2)
        b2.addWidget(self.value_data_s)

        b3 = QHBoxLayout()
        b3.addLayout(b1)
        b3.addSpacing(20)
        b3.addLayout(b2)
        self.box_slider.setLayout(b3)
        self.box_slider.setFont(QFont("Segoe UI",12))
        return self.box_slider


        # List COM availables 

############ SLIDER BAR OFF
    def values_box(self):
        self.box_slider_off = QGroupBox("Time OFF")
        self.slider_off = QSlider(Qt.Horizontal, self)
        self.slider_off.setGeometry(50,50,320,200)
        self.slider_off.setMinimum(0)
        self.slider_off.setMaximum(100)
        self.slider_off.setValue(100)
        self.slider_off.setTickPosition(QSlider.TicksBelow)
        self.slider_off.setTickInterval(10)        
        self.slider_off.valueChanged.connect(self.get_value_off)

        self.icon = QLabel(self)
        image = QPixmap('image/empty.png')
        self.icon.setPixmap(image.scaled(30,30))
        # self.icon.setSize(20  0,200)

        self.value_data_1 = QLabel(str(self.value_off))
        self.value_data_1.setStyleSheet("background-color:#F1F7EE")
        self.value_data_1.setAlignment(Qt.AlignCenter)
        self.value_data_1.setFont(QFont("Segoe UI",16))
        # self.value_data.setFont(QFont("Times",23,weight=QFont.Bold))

        title2 = QLabel("Time in ms")
        title2.setFont(QFont("Segoe UI",12, weight= QFont.Bold))
        title2.setAlignment(Qt.AlignCenter)
        self.value_data_off_s = QLabel("00")
        self.value_data_off_s.setStyleSheet("background-color:#F1F7EE")
        self.value_data_off_s.setAlignment(Qt.AlignCenter)
        self.value_data_off_s.setFont(QFont("Segoe UI",16))


        b1 = QHBoxLayout()
        b1.addWidget(self.icon)
        b1.addSpacing(20)
        b1.addWidget(self.slider_off)
        b1.addSpacing(50)
        b1.addWidget(self.value_data_1)

        b2 = QVBoxLayout()
        b2.addWidget(title2)
        b2.addWidget(self.value_data_off_s)

        b3 = QHBoxLayout()
        b3.addLayout(b1)
        b3.addSpacing(20)
        b3.addLayout(b2)
        self.box_slider_off.setLayout(b3)
        self.box_slider_off.setFont(QFont("Segoe UI",12))
        return self.box_slider_off

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


    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Alert")
        msgBox.setText("Choose a valid port")
        msgBox.setStandardButtons(QMessageBox.Ok )

        returnValue = msgBox.exec()
    









