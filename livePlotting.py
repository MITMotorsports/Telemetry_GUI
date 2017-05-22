import sys
import os
import serial
import threading
import random

from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QMainWindow,
    QAction, qApp, QMenuBar, QMessageBox, QFileDialog, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout, QTextEdit, QSizePolicy, QGridLayout)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import QCoreApplication, Qt, QTimer

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from xbeeParser import *
import CAN_SPEC

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass

class batteryGraph(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.barGraph = self.axes.bar(left=[0], height=[10])
        self.axes.set_ylim([0, 100])
        self.axes.get_xaxis().set_visible(False)
        self.axes.set_ylabel('SOC Percentage')
        self.axes.set_title('Battery SOC')

    def update_figure(self, soc):
        first = CAN_SPEC.Data_Pos_Dict['CURRENT_SENSOR_ENERGY']['PACK_ENERGY'][0]
        last = CAN_SPEC.Data_Pos_Dict['CURRENT_SENSOR_ENERGY']['PACK_ENERGY'][1]
        max_soc = 2**(last - first + 1) - 1
        soc = (soc/max_soc)*100
        if soc >= 20:
            c = 'y'
            if soc >= 50:
                c = 'g'
        else:
            c = 'r'
        self.barGraph[0].set_height(int(soc))
        self.barGraph[0].set_color(c)
        #self.axes.set_ylim([0, 100])
        #self.axes.get_xaxis().set_visible(False)
        self.draw()


class LineGraph(MyMplCanvas):
    def __init__(self, *args, data_color='g', data_name=THROTTLE,
                    data_title='Throttle', percentageY=1, unitsY='s', **kwargs):
        self.data_buffer = []
        self.time_buffer = []
        self.data_color = data_color
        self.buffer_length = 100
        self.data_name = data_name
        self.data_title = data_title
        self.percentageY = percentageY
        self.unitsY = unitsY
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.line = self.axes.plot(self.time_buffer, self.data_buffer)
        self.axes.lines[0].set_color(self.data_color)
        self.axes.set_xlabel('Time')
        self.axes.set_title(self.data_title)
        if self.percentageY:
            self.axes.set_ylim([0, 100])
            self.axes.set_ylabel(self.data_title + ' Percentage')
        else:
            self.axes.set_ylabel(self.data_title + ' ' + self.unitsY)

    def update_figure(self, timestamp, data):
        self.axes.lines.remove(self.axes.lines[0]);
        if(len(self.time_buffer) < self.buffer_length):
            # self.time_buffer.append(newData.get(TIME))
            # self.data_buffer.append(newData.get(self.data_name))
            self.time_buffer.append(timestamp)
            self.data_buffer.append(data)
        else:
            self.time_buffer.pop(0)
            self.data_buffer.pop(0)
            # self.time_buffer.append(newData.get(TIME))
            # self.data_buffer.append(newData.get(self.data_name))
            self.time_buffer.append(timestamp)
            self.data_buffer.append(data)

        self.line = self.axes.plot(self.time_buffer, self.data_buffer)
        self.axes.set_xlim([self.time_buffer[0], self.time_buffer[-1]])
        self.axes.lines[0].set_color(self.data_color)
        self.draw()

class BatteryTemps(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        positions = [(i,j) for i in range(20) for j in range(10)]

        for pos in positions:
            text = QLabel(str(pos[0] + pos[1]*10))
            self.grid.addWidget(text, *pos)

        self.gridCol = self.grid.columnCount()

    #accepts a dictionary {cellNum:temp}
    def update(temps):
        for cell in temps.keys():
            color = tempColor(temps[cell])
            oldData = self.grid.itemAtPosition(*indToPosition(cell)).widget()
            newString = str(cell) + ": " + str(temps[cell])
            oldData.setText(newString)
            oldData.setStyleSheet('color:red')

    #returns a color for the cell text based on the temperature
    def tempColor(temp):
        return 0

    #returns the grid position of a cell based on the index
    def indToPosition(ind):
        return (ind % self.gridCol, ind // self.gridCol)

class XbeeLiveData(QWidget):
    def __init__(self, serialPort):
        super().__init__()
        #Open the serial port to communicate with xbee
        self.serialPort = serialPort
        self.xbee = serial.Serial(port='/dev/'+serialPort, baudrate=XBEE_BAUD, timeout=3, parity=serial.PARITY_EVEN)
        self.xbee.isOpen()
        #syncXbee(self.xbee)
        #Initialize a thread to run the live data view in
        self.thread = threading.Thread(target=self.gatherData)
        self.continueThread = threading.Event()
        self.continueThread.set()

        #Data Display Initialization
        self.logOutput = QTextEdit(self)
        self.batBar = batteryGraph(self, width=5, height=4, dpi=100)
        self.throttleGraph = LineGraph(self, data_color='g', data_name=THROTTLE,
                                data_title='Throttle', percentageY=1)
        self.brakeGraph = LineGraph(self, data_color='r', data_name=BRAKE,
                                data_title='Brake', percentageY=1)
        self.cellTemps = BatteryTemps()

        #Run Initialization function
        self.initUI(serialPort)

    def initUI(self, xbeeList):
        h1 = QHBoxLayout()
        self.logOutput.setReadOnly(True)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        font = self.logOutput.font()
        font.setFamily("Courier")
        font.setPointSize(12)
        h1.addWidget(self.logOutput)
        h1.addWidget(self.batBar)

        h2 = QHBoxLayout()
        h2.addWidget(self.throttleGraph)
        h2.addWidget(self.brakeGraph)

        v1 = QVBoxLayout()
        v1.addLayout(h1)
        v1.addLayout(h2)

        v2 = QVBoxLayout()
        v2.addWidget(QLabel('Battery Cell Temperatures'), stretch = 1)
        v2.addWidget(self.cellTemps, stretch = 10)

        finalH = QHBoxLayout(self)
        finalH.addLayout(v1, stretch = 4)
        finalH.addLayout(v2, stretch = 1)

        self.thread.start()

        self.setGeometry(300, 300, 1500, 1000)
        self.setWindowTitle('Live Data From: ' + self.serialPort)

    def gatherData(self):
        xbeeData = ''
        while(self.continueThread.is_set()):
            tmp = []
            if self.xbee.in_waiting > 0:
                xbeeData, payload = read_packet(self.xbee)

                print('xbeeData {0}'.format(xbeeData))

                self.logOutput.moveCursor(QTextCursor.End)
                self.logOutput.insertPlainText(xbeeData+'\n')
                sb = self.logOutput.verticalScrollBar()
                sb.setValue(sb.maximum())
                timestamp, ID, MSG = parseMessage(xbeeData, payload)
                print('Timestamp: {0}'.format(timestamp))
                print('ID Name: {0}'.format(ID))
                print('MSG DATA: {0}'.format(MSG))

                if ID != None:
                    self.updateVisuals(timestamp, ID, MSG)


    def updateVisuals(self, timestamp, ID, MSG):
        if ID == 'CURRENT_SENSOR_ENERGY':
            self.batBar.update_figure(MSG['PACK_ENERGY'])
        if ID == 'FRONT_CAN_NODE_DRIVER_OUTPUT':
            torque = MSG['REQUESTED_TORQUE']
            first = CAN_SPEC.Data_Pos_Dict['FRONT_CAN_NODE_DRIVER_OUTPUT']['REQUESTED_TORQUE'][0]
            last = CAN_SPEC.Data_Pos_Dict['FRONT_CAN_NODE_DRIVER_OUTPUT']['REQUESTED_TORQUE'][1]
            max_torque = 2**(last - first + 1) - 1
            torque = (torque/max_torque)*100
            self.throttleGraph.update_figure(timestamp, torque)

            pressure = MSG['BRAKE_PRESSURE']
            first = CAN_SPEC.Data_Pos_Dict['FRONT_CAN_NODE_DRIVER_OUTPUT']['BRAKE_PRESSURE'][0]
            last = CAN_SPEC.Data_Pos_Dict['FRONT_CAN_NODE_DRIVER_OUTPUT']['BRAKE_PRESSURE'][1]
            max_pressure = 2**(last - first + 1) - 1
            pressure = (pressure/max_pressure)*100
            self.brakeGraph.update_figure(timestamp, MSG['BRAKE_PRESSURE'])

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "End Live Data Session?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.continueThread.clear()
            self.thread.join()
            self.xbee.close()
            event.accept()
        else:
            event.ignore()
