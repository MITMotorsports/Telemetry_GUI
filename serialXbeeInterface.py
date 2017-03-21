import serial
import sys
import argparse
import random
import time

def syncXbee(xBeeSerial):
    notSync = True
    ack = 'b'
    while(notSync):
        if xBeeSerial.in_waiting > 0:
            val = xBeeSerial.read(1)
            print(val.decode())
            if val.decode() == 'a':
                print('wee')
                xBeeSerial.write(ack.encode('utf-8'))
                notSync = False

def mainLoop(xbeeData):
    loop = True
    num = 0
    while(loop):
        # try:
        #     inp = sys.stdin.readlines()
        #     print(inp)
        #     if inp == '-stop\n':
        #         loop = false
        #     else:
        #         xbee.write(inp)
        # except StopIteration:
        #     pass
        bat = random.randint(0, 100)
        t = random.randint(0, 100)
        b = random.randint(0, 100)
        batString = str(num) + '_1_' + str(bat) + '\n'
        tString = str(num) + '_4_' + str(t) + '\n'
        bString = str(num) + '_5_' + str(b) + '\n'
        xbee.write(batString.encode('utf-8'))
        xbee.write(tString.encode('utf-8'))
        xbee.write(bString.encode('utf-8'))
        print(batString)
        print(tString)
        print(bString)
        num = num + 1;
        time.sleep(.1)

        # tmp = []
        # if xbee.in_waiting > 0:
        #     tmp.append(xbee.read(1))
        #
        # if tmp == [b'\n']:
        #     print(xbeeData)
        #     xbeeData = ''
        # elif tmp != []:
        #     xbeeData += tmp[0].decode()

try:
    xbee = serial.Serial(port='/dev/cu.usbserial-DN01HQ13')
    xbee.isOpen()
    #syncXbee(xbee)
    xbeeData = ''
    mainLoop(xbeeData)
except KeyboardInterrupt:
    xbee.close()
    exit()
