import sys
import os
import serial
import threading

from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QWidget, QMainWindow,
    QAction, qApp, QMenuBar, QMessageBox, QFileDialog, QPushButton, QLabel,
    QHBoxLayout, QVBoxLayout, QTextEdit)
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import QCoreApplication, Qt, QTimer

from livePlotting import XbeeLiveData

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
        openFile.triggered.connect(self.showFileDialog)

        devices = os.listdir('/dev')
        xbeeList = []

        for i in devices:
            if 'cu.usbserial' in i:
                xbeeList.append(i)

        xbeeButtons = XbeeButtons(xbeeList)

        QMainWindow.setCentralWidget(self, xbeeButtons)

        self.resize(500, 500)
        self.center()

        self.statusBar().showMessage('Select SD Card or Serial Stream')

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.toolbar.addAction(openFile)

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

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open SD Card', '/Volumes')

        if fname[0]:
            self.sdData = SDData(fname)
            self.sdData.show()



class XbeeButtons(QWidget):
    def __init__(self, xbeeList):
        super().__init__()
        self.xbeeButtons = []
        self.initUI(xbeeList)

    def initUI(self, xbeeList):
        vbox = QVBoxLayout()

        if len(xbeeList) != 0:
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

class SDData(QWidget):
    def __init__(self, fname):
        super().__init__()
        self.fname = fname[0]
        self.f = open(self.fname, 'r')
        self.initUI()

    def initUI(self):
        textOut = QTextEdit(self)
        textOut.setReadOnly(True)
        textOut.setLineWrapMode(QTextEdit.NoWrap)
        font = textOut.font()
        font.setFamily("Courier")
        font.setPointSize(12)

        with self.f:
            data = self.f.read()
            textOut.setText(data)

        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('SD Data From: ' + self.fname)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "End SD Data Session?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.f.close()
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('icons/logo.png'))
    win = MainWindow()

    sys.exit(app.exec_())
