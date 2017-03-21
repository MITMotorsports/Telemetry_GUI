import time

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

def parseMessage(message):
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
