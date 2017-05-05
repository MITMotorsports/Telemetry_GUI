import sys
import os
import serial
import threading

from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QMainWindow,
    QAction, qApp, QMenuBar, QMessageBox, QFileDialog, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout, QTextEdit, QProgressBar, QScrollArea)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import QCoreApplication, Qt, QTimer, QEvent

from livePlotting import XbeeLiveData
from csv_output import raw_to_csv

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Cmd+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        openFile = QAction(QIcon('icons/sd.png'), 'Open', self)
        openFile.setShortcut('Cmd+O')
        openFile.setStatusTip('Select an SD card')
        openFile.triggered.connect(self.show_file_dialog)

        downloadFile = QAction(QIcon('icons/download.png'), 'Download File', self)
        downloadFile.setShortcut('Cmd+D')
        downloadFile.setStatusTip('Download a logging file from the Black Box')
        downloadFile.triggered.connect(self.show_download_dialog) #make a function to show menu

        devices = os.listdir('/dev')
        xbeeList = []

        for i in devices:
            if 'cu.usbserial' in i:
                xbeeList.append(i)

        xbeeButtons = XbeeButtons(xbeeList, 'Select xbee for Live Data Streaming')

        QMainWindow.setCentralWidget(self, xbeeButtons)

        self.resize(500, 500)
        self.center()

        self.statusBar().showMessage('Select SD Card or Serial Stream')

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openFile)
        self.toolbar.addAction(downloadFile)

        menubar = QMenuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        self.setMenuBar(menubar)

        self.setWindowTitle('FSAE Telemetry')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_file_dialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open SD Card', '/Volumes')

        if fname[0]:
            self.sdData = SDData(fname)
            self.sdData.show()

    def show_download_dialog(self):
        self.sd_download = DownloadSDWindow()
        self.sd_download.show()

class XbeeButtons(QWidget):
    def __init__(self, xbeeList, xbee_function):
        super().__init__()
        self.xbeeButtons = []
        self.xbee_function = xbee_function

        self.initUI(xbeeList)

    def initUI(self, xbeeList):
        vbox = QVBoxLayout()

        if len(xbeeList) != 0:
            vbox.addWidget(QLabel(self.xbee_function))
            for i in xbeeList:
                btn = QPushButton(i)
                btn.setObjectName(i)
                btn.setStatusTip('Open Serial Stream from ' + i)
                btn.clicked.connect(self.buttonClicked)
                vbox.addWidget(btn)
                self.xbeeButtons.append(btn)
        else:
            noDev = QLabel('No xbee devices detected')
            vbox.addWidget(noDev)

        vbox.addStretch(1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addStretch(1)
        self.setLayout(hbox)

    def buttonClicked(self):
        sender = self.sender()
        self.dataWindow = XbeeLiveData(sender.objectName())
        self.dataWindow.show()

class XbeeButtonsDownload(XbeeButtons):
    def buttonClicked(self):
        sender = self.sender()
        self.parentWidget().connect_to_car(sender.objectName())

class SDData(QWidget):
    def __init__(self, file_name):
        super().__init__()
        self.file_name = file_name[0]
        self.f = open(self.file_name, 'rb')
        self.initUI()

    def initUI(self):
        textOut = QTextEdit(self)
        textOut.setReadOnly(True)
        textOut.setLineWrapMode(QTextEdit.NoWrap)
        font = textOut.font()
        font.setFamily("Courier")
        font.setPointSize(12)

        folder_loc = raw_to_csv(self.f)

        textOut.setText("SD File Parsed, Data in: {0}".format(folder_loc))

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('SD Data From: ' + self.file_name)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "End SD Data Session?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.f.close()
            event.accept()
        else:
            event.ignore()

class DownloadSDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Download SD data')

        self.v1 = QVBoxLayout(self)

        devices = os.listdir('/dev')
        xbeeList = []

        for i in devices:
            if 'cu.usbserial' in i:
                xbeeList.append(i)

        xbeeButtons = XbeeButtonsDownload(xbeeList, "Select XBee Receiver")

        self.v1.addWidget(xbeeButtons)

    def connect_to_car(self, serialPort):
        #Open the serial port to communicate with xbee
        self.serialPort = serialPort
        self.xbee = serial.Serial(port='/dev/'+serialPort, baudrate=115200, timeout=3)
        self.xbee.isOpen()
        children = self.children()
        for i in children:
            if type(i) == XbeeButtonsDownload:
                i.setParent(None)
        file_list = self.list_files()

    def list_files(self):
        self.xbee.write('ls\n'.encode('utf-8'))
        scan = True
        xbeeData = ''
        self.scroll = QScrollArea()
        widg = QWidget()
        but_box = QVBoxLayout()
        widg.setLayout(but_box)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widg)
        while scan:
            tmp = []
            if self.xbee.in_waiting > 0:
                val = self.xbee.read(1)
                tmp.append(val)

            if tmp == [b'\n']:
                if xbeeData == 'end':
                    break
                btn = QPushButton(xbeeData)
                btn.setObjectName(xbeeData)
                btn.setStatusTip('Download Data from ' + xbeeData)
                btn.clicked.connect(self.download_file)
                but_box.addWidget(btn)
                xbeeData = ''
            elif tmp != []:
                xbeeData += val.decode()

            self.v1.addWidget(self.scroll)
        return 0

    def download_file(self):
        #Get file name from button name
        sender = self.sender()
        file_name = sender.objectName()

        #Tell black box to dump the file data over serial
        self.xbee.write('open\n'.encode('utf-8'))
        self.xbee.write(file_name.encode('utf-8'))
        self.xbee.write('\n'.encode('utf-8'))
        file_name = file_name[0:-1]
        print(file_name)

        #recieve data until black box sends "end\n" and print to file
        out_file = open('../data/'+file_name, 'wb')
        scan = True
        xbeeData = ''
        new_line_found = 0
        while scan:
            # tmp = []
            if self.xbee.in_waiting > 0:
                val = self.xbee.read(1)
                # tmp.append(val)

                if val == b'\n':
                    if 'end' in xbeeData:
                        out_file.close()
                        scan = False
                        break
                    else:
                        print(xbeeData)
                        out_file.write(xbeeData+'\n');
                        xbeeData = ''
                else:
                    xbeeData += val.decode()



    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "End SD Data Session?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        try:
            self.xbee.close()
        except AttributeError:
            pass

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/logo.png'))
    win = MainWindow()

    sys.exit(app.exec_())
