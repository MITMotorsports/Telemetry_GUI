import serial
import sys
import argparse
import random as rd
import time
import CAN_SPEC

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

def mainLoop(xbee):
    loop = True
    num = 0
    line_count = 0
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
        tmp_choice = rd.choice(list(CAN_SPEC.ID_Dict.items()))
        ID = tmp_choice[0]
        print(tmp_choice)
        data_dict = CAN_SPEC.Data_Pos_Dict[tmp_choice[1]]
        # print(data_dict)
        data = 0
        data_count = 0
        for k, v in data_dict.items():
            for i in range(v[0], v[1]):
                # print(rd.randint(0,1)<<i%8)
                # data[i//8] = data[i//8] + rd.randint(0,1)<<i%8
                tmp = rd.randint(0,1)<<i
                data = data + tmp
                # print(data)

        # for i in range(len(data)):
        #     data[i] = bytes(data[i])
            # print(bytes(data[i]))
        payload_len = data.bit_length()//8 + 1
        MSG = data.to_bytes(payload_len, byteorder='little')
        # print('MSG')
        curr_time = int(time.time())
        # time_stamp = curr_time.to_bytes((curr_time.bit_length()//8 + 1), byteorder='little')
        time_stamp = str(curr_time).encode()
        # print("start")
        wrote = xbee.write(time_stamp)
        # print(wrote)
        wrote = xbee.write('_'.encode())
        # print(wrote)
        # wrote = xbee.write(ID.to_bytes((ID.bit_length()//8 + 1), byteorder='little'))
        wrote = xbee.write(str(ID).encode())
        # print(wrote)
        wrote = xbee.write('_'.encode())

        wrote = xbee.write(str(payload_len).encode())

        wrote = xbee.write('_'.encode())
        # print(wrote)
        wrote = xbee.write(MSG)
        # print(wrote)
        wrote = xbee.write('_'.encode())
        # print(wrote)
        wrote = xbee.write(str(line_count).encode())
        # print(wrote)
        wrote = xbee.write('\n'.encode())

        # print("Done")
        # print(line_count)
        # print("^lines^")

        time.sleep(.5)
        line_count = line_count + 1

        # tmp = []
        # if xbee.in_waiting > 0:
        #     tmp.append(xbee.read(1))
        #
        # if tmp == [b'\n']:
        #     print(xbeeData)
        #     xbeeData = ''
        # elif tmp != []:
        #     xbeeData += tmp[0].decode()

if __name__ == '__main__':
    try:
        # xbee = serial.Serial(port='/dev/cu.usbserial-DN01HQ13', baudrate=115200)
        xbee = serial.Serial(port='/dev/cu.usbserial-DN01EWWF', baudrate=115200)
        xbee.isOpen()
        #syncXbee(xbee)
        xbeeData = ''
        # wrote = xbee.write('hello\n'.encode())
        # print(wrote)
        mainLoop(xbee)
    except KeyboardInterrupt:
        xbee.close()
        exit()
