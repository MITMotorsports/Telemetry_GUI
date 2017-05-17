import time
import CAN_SPEC

TIME = 0
BATTERY_SOC = 1
BATTERY_TEMP = 2
BATTERY_VOLTAGE = 3
THROTTLE = 4
BRAKE = 5
SPEED = 6


TIME_POS = 0
DATA_TYPE_POS = 1
DATA_POS = 2

def read_packet(xbee_stream):
    #timestamp_ID_MSGLEN_MSG_LineCount
    xbeeData = ''
    val = xbee_stream.read(1)
    print(val)
    try:
        xbeeData += val.decode()
    except UnicodeDecodeError:
        print('out of sync')
        return None

    under_count = 0
    while under_count < 3:
        if xbee_stream.in_waiting > 0:
            val = xbee_stream.read(1).decode()
            if val == '_':
                under_count = under_count + 1
            xbeeData += val

    split_data = xbeeData.split('_')
    payload_len = int(split_data[2])
    payload = xbee_stream.read(payload_len)

    newline = 0
    while not newline:
        if xbee_stream.in_waiting > 0:
            val = xbee_stream.read(1)
            val = val.decode()
            if val == '\n':
                newline = 1
                break
            xbeeData += val

    return xbeeData, payload

def parseMessage(message, payload):
    #timestamp_ID_MSGLEN_MSG_LineCount
    # print('Parsing message...')
    spiltMessage = message.split('_')
    timestamp = int(spiltMessage[0])
    # print('Timestamp: {0}'.format(timestamp))
    ID = int(spiltMessage[1])
    ID = CAN_SPEC.ID_Dict.get(ID)
    if ID == None:
        return None, None, None
    # print('ID Name: {0}'.format(ID))
    data_dict = CAN_SPEC.Data_Pos_Dict[ID]
    MSG_data = {}

    #Endianess is BULLSHIT
    if CAN_SPEC.is_little_endian[ID]:
        payload = bytearray(payload)
        payload.reverse()
        print("PAYLOAD LITTLE: {0}".format(payload))
        print("BYTE 0: {0}".format(payload[0]))
        MSG = int.from_bytes(payload, byteorder='little')
        print("MSG LITTLE: {0}".format(MSG))
        for k, v in data_dict.items():
            mask = 0
            for i in range(v[0], v[1]+1):
                mask = mask + (1<<i)
            MSG_data[k] = (MSG & mask)>>v[0];
    else:
        payload = bytearray(payload)
        payload.reverse()
        for i in range(0,len(payload)):
            print(bin(payload[i]))
        print("PAYLOAD BIG: {0}".format(payload))
        print("BYTE 0: {0}".format(payload[0]))
        MSG = int.from_bytes(payload, byteorder='big')
        print(bin(MSG))
        print("MSG BIG: {0}".format(MSG))
        for k, v in data_dict.items():
            mask = 0
            for i in range(v[0], v[1]+1):
                mask = mask + (1<<i)
            MSG_data[k] = (MSG & mask)>>v[0];
        # print("PAYLOAD BIG: {0}".format(payload))
        # for k, v in data_dict.items():
        #     mask = payload[(v[0]//8):((v[1]//8)+1)]
        #     MSG_data[k] = int.from_bytes(mask, byteorder='big')
        #     print("MSG BIG: {0}".format(MSG_data[k]))

    # print("--- Data Dictionary ---")
    # print(MSG_data)
    # print("--- Data Dictionary ---")

    return timestamp, ID, MSG_data


def parseMessage2(message):
    spiltMessage = message.split('_')

    try:
        time = int(spiltMessage[TIME_POS])
        dataType = int(spiltMessage[DATA_TYPE_POS])
        data = int(spiltMessage[DATA_POS])
    except ValueError as e:
        return None

    if dataType == BATTERY_SOC:
        return {BATTERY_SOC:data, TIME:time}
    elif dataType == BATTERY_TEMP:
        data = batteryTempParse(data)
        return {BATTERY_TEMP:data, TIME:time}
    elif dataType == BATTERY_VOLTAGE:
        return {BATTERY_VOLTAGE:data, TIME:time}
    elif dataType == THROTTLE:
        return {THROTTLE:data, TIME:time}
    elif dataType == BRAKE:
        return {BRAKE:data, TIME:time}
    elif dataType == SPEED:
        return {SPEED:data, TIME:time}
    else:
        return None

def syncXbee(xBeeSerial):
    notSync = True
    ack = 'a'
    print('sync')
    while(notSync):
        print('send ack' + ack)
        xBeeSerial.write(ack.encode('utf-8'))
        print('sleep')
        if xBeeSerial.in_waiting > 0:
            val = xBeeSerial.read(1)
            print(val.decode())
            if val.decode() == 'b':
                notSync = False

        time.sleep(.5)

def batteryTempParse(data):
    batteryData = data.split('-')
    outputDict = {}
    for i in splitMessage:
        cellData = batteryData.split('=')
        outputDict[cellData[0]] = cellData[1]/10

    return outputDict
