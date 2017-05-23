from collections import OrderedDict

ID_Dict = {352:'BMS_CELL_TEMPS',
835:'ACCELEROMETER_HORIZONTAL',
836:'ACCELEROMETER_VERTICAL',
49:'REAR_CAN_NODE_HEARTBEAT',
353:'BMS_PACK_STATUS',
80:'VCU_BMS_HEARTBEAT',
81:'VCU_DASH_HEARTBEAT',
82:'VCU_MC_MESSAGE',
851:'GYRO_HORIZONTAL',
852:'GYRO_VERTICAL',
561:'FRONT_CAN_NODE_WHEEL_SPEED',
608:'BMS_ERRORS',
96:'BMS_HEARTBEAT',
1313:'CURRENT_SENSOR_CURRENT',
1314:'CURRENT_SENSOR_VOLTAGE',
867:'MAGNETOMETER_HORIZONTAL',
868:'MAGNETOMETER_VERTICAL',
1318:'CURRENT_SENSOR_POWER',
48:'FRONT_CAN_NODE_DRIVER_OUTPUT',
1320:'CURRENT_SENSOR_ENERGY',
112:'DASH_HEARTBEAT',
560:'FRONT_CAN_NODE_RAW_VALUES',
113:'DASH_REQUEST',
50:'REAR_CAN_NODE_WHEEL_SPEED',
819:'LV_BATTERY_VOLTAGE',
784:'MC_RESPONSE'}

Data_Pos_Dict = {'BMS_PACK_STATUS': OrderedDict([('PACK_VOLTAGE',(0,8)), ('PACK_CURRENT',(9,19)), ('AVE_CELL_VOLTAGE',(20,29)), ('MIN_CELL_VOLTAGE',(30,39)), ('MIN_CELL_VOLTAGE_ID',(40,46)), ('MAX_CELL_VOLTAGE',(47,56)), ('MAX_CELL_VOLTAGE_ID',(57,63))]),
'GYRO_VERTICAL': OrderedDict([('Z_AXIS',(0,31))]),
'MAGNETOMETER_HORIZONTAL': OrderedDict([('X_AXIS',(0,31)), ('Y_AXIS',(32,63))]),
'VCU_BMS_HEARTBEAT': OrderedDict([('STATE',(0,0))]),
'VCU_MC_MESSAGE': OrderedDict([('REG_ID',(0,7)), ('DATA_1',(8,15)), ('DATA_2',(16,23))]),
'CURRENT_SENSOR_ENERGY': OrderedDict([('PACK_ENERGY',(16,47))]),
'ACCELEROMETER_HORIZONTAL': OrderedDict([('X_AXIS',(0,31)), ('Y_AXIS',(32,63))]),
'MC_RESPONSE': OrderedDict([('REG_ID',(0,7)), ('DATA',(8,23))]),
'CURRENT_SENSOR_POWER': OrderedDict([('PACK_POWER',(16,47))]),
'REAR_CAN_NODE_WHEEL_SPEED': OrderedDict([('REAR_RIGHT_WHEEL_SPEED',(0,31)), ('REAR_LEFT_WHEEL_SPEED',(32,63))]),
'VCU_DASH_HEARTBEAT': OrderedDict([('RTD_LIGHT',(0,0)), ('AMS_LIGHT',(1,1)), ('IMD_LIGHT',(2,2)), ('HV_LIGHT',(3,3)), ('TRACTION_CONTROL',(4,4)), ('LIMP_MODE',(5,5)), ('LV_WARNING',(6,6)), ('ACTIVE_AERO',(7,7)), ('REGEN',(8,8)), ('SHUTDOWN_ESD_DRAIN',(9,9)), ('SHUTDOWN_BMS',(10,10)), ('SHUTDOWN_IMD',(11,11)), ('SHUTDOWN_BSPD',(12,12)), ('SHUTDOWN_VCU',(13,13)), ('SHUTDOWN_PRECHARGE',(14,14)), ('SHUTDOWN_MASTER_RESET',(15,15)), ('SHUTDOWN_DRIVER_RESET',(16,16)), ('LV_BATTERY_VOLTAGE_TENTH_VOLT',(17,24)), ('HEARTBEAT_FRONT_CAN_NODE_DEAD',(25,25)), ('HEARTBEAT_REAR_CAN_NODE_DEAD',(26,26)), ('HEARTBEAT_BMS_DEAD',(27,27)), ('HEARTBEAT_DASH_DEAD',(28,28)), ('HEARTBEAT_MC_DEAD',(29,29)), ('HEARTBEAT_CURRENT_SENSOR_DEAD',(30,30)), ('TSMS_OFF',(31,31)), ('RESET_LATCH_OPEN',(32,32)), ('PRECHARGE_RUNNING',(33,33)), ('MASTER_RESET_NOT_INITIALIZED',(34,34)), ('ET_NOT_INITIALIZED',(35,35))]),
'DASH_HEARTBEAT': OrderedDict([('HEARTBEAT_ON',(0,0))]),
'FRONT_CAN_NODE_DRIVER_OUTPUT': OrderedDict([('REQUESTED_TORQUE',(0,15)), ('BRAKE_PRESSURE',(16,23)), ('STEERING_POSITION',(24,31)), ('THROTTLE_IMPLAUSIBLE',(32,32)), ('BRAKE_THROTTLE_CONFLICT',(33,33)), ('BRAKE_ENGAGED',(34,34))]),
'DASH_REQUEST': OrderedDict([('REQUEST_TYPE',(0,2))]),
'BMS_CELL_TEMPS': OrderedDict([('AVE_CELL_TEMP',(0,14)), ('MIN_CELL_TEMP',(15,29)), ('MIN_CELL_TEMP_ID',(30,38)), ('MAX_CELL_TEMP',(39,53)), ('MAX_CELL_TEMP_ID',(54,62))]),
'CURRENT_SENSOR_VOLTAGE': OrderedDict([('PACK_VOLTAGE',(16,47))]),
'LV_BATTERY_VOLTAGE': OrderedDict([('BATTERY_VOLTAGE',(0,15))]),
'REAR_CAN_NODE_HEARTBEAT': OrderedDict([('IS_OK',(0,0))]),
'ACCELEROMETER_VERTICAL': OrderedDict([('Z_AXIS',(0,31))]),
'BMS_HEARTBEAT': OrderedDict([('STATE',(0,2)), ('SOC_PERCENTAGE',(3,12))]),
'CURRENT_SENSOR_CURRENT': OrderedDict([('PACK_CURRENT',(16,47))]),
'MAGNETOMETER_VERTICAL': OrderedDict([('Z_AXIS',(0,31))]),
'FRONT_CAN_NODE_RAW_VALUES': OrderedDict([('RIGHT_THROTTLE_POT',(0,9)), ('LEFT_THROTTLE_POT',(10,19)), ('FRONT_BRAKE_PRESSURE',(20,29)), ('REAR_BRAKE_PRESSURE',(30,39)), ('STEERING_POT',(40,49))]),
'GYRO_HORIZONTAL': OrderedDict([('X_AXIS',(0,31)), ('Y_AXIS',(32,63))]),
'BMS_ERRORS': OrderedDict([('ERROR_TYPE',(0,3))]),
'FRONT_CAN_NODE_WHEEL_SPEED': OrderedDict([('FRONT_RIGHT_WHEEL_SPEED',(0,31)), ('FRONT_LEFT_WHEEL_SPEED',(32,63))])}

is_little_endian = {'BMS_PACK_STATUS': 0,
'GYRO_VERTICAL': 0,
'MAGNETOMETER_HORIZONTAL': 0,
'VCU_BMS_HEARTBEAT': 0,
'VCU_MC_MESSAGE': 1,
'CURRENT_SENSOR_ENERGY': 0,
'ACCELEROMETER_HORIZONTAL': 0,
'MC_RESPONSE': 1,
'CURRENT_SENSOR_POWER': 0,
'REAR_CAN_NODE_WHEEL_SPEED': 0,
'VCU_DASH_HEARTBEAT': 0,
'DASH_HEARTBEAT': 0,
'FRONT_CAN_NODE_DRIVER_OUTPUT': 0,
'DASH_REQUEST': 0,
'BMS_CELL_TEMPS': 0,
'CURRENT_SENSOR_VOLTAGE': 0,
'LV_BATTERY_VOLTAGE': 0,
'REAR_CAN_NODE_HEARTBEAT': 0,
'ACCELEROMETER_VERTICAL': 0,
'BMS_HEARTBEAT': 0,
'CURRENT_SENSOR_CURRENT': 0,
'MAGNETOMETER_VERTICAL': 0,
'FRONT_CAN_NODE_RAW_VALUES': 0,
'GYRO_HORIZONTAL': 0,
'BMS_ERRORS': 0,
'FRONT_CAN_NODE_WHEEL_SPEED': 0}

