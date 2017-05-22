import sys
import os
import collections, itertools
import csv
import serial

import CAN_SPEC
from xbeeParser import parseMessage, XBEE_BAUD

#converts a whole file of raw CAN messages into a bunch of CSVs
def raw_to_csv(file_obj):
    file_obj.seek(0)
    #Extract the name of the data file
    file_path = file_obj.name.split('/')

    #Use the data file name to make a folder to put the CSV data
    csv_name = file_path[-1][:-4]
    csv_output_folder = '../data/'+csv_name+'_csv_data'
    if not os.path.isdir(csv_output_folder):
        os.mkdir(csv_output_folder)

    #create one csv file for every type of CAN messages
    #this makes handling the data easier because each data row will have the
    #same timestamp
    output_file_dict = {}
    output_csv_dict = {} #list of output file objects
    output_csv_dict_col_map = {} #list of names of data columns
    for k in CAN_SPEC.Data_Pos_Dict.keys():
        csv_file = open(csv_output_folder+'/'+csv_name+'_'+k+'.csv', 'w')
        output_file_dict[k] = csv_file
        output_csv_dict[k] = csv.writer(csv_file)
        col_keys = list(CAN_SPEC.Data_Pos_Dict[k].keys())
        output_csv_dict_col_map[k] = col_keys
        col_name_header = ['TIMESTAMP']
        col_name_header.extend(col_keys)
        output_csv_dict[k].writerow(col_name_header)

    #parse data file and put data into appropriate CSV files
    val = file_obj.read(4) #record the log start timestamp at head of file
    log_start = int.from_bytes(val, byteorder='little')
    print(log_start)

    #read until EOF is hit
    data_line = file_obj.read(13)
    print('FIRST READ RAW: {0}'.format(data_line))
    while data_line != b'':
        timestamp, ID, MSG_data  = parseMessage(data_line, log_start)
        out = [timestamp]
        for k in output_csv_dict_col_map[ID]:
            out.append(MSG_data[k])
        output_csv_dict[ID].writerow(out)

        data_line = file_obj.read(13)
        print('END OF LOOP READ RAW: {0}'.format(data_line))

    #CLOSE ALL THE FILES
    for k,v in output_file_dict.items():
        v.close()

    return csv_output_folder

#converts a downloaded file of raw CAN messages into a bunch of CSVs
#parses output until the xbee sends 'end\n'
def xbee_to_csv(xbee, filename, pbar):
    #read the data coming from the xbee into a giant buffer before parsing it
    xbee_buffer = collections.deque()

    val = xbee.read(4) #first four bytes are the file size in bytes
    file_size = int.from_bytes(val, byteorder='little')
    dl_time = (file_size/XBEE_BAUD)/60.0 #the estimated download time in minutes
    print('Estimated Download Time: {0} minutes'.format(dl_time))

    bytes_downloaded = 0;
    pbar.setValue((bytes_downloaded/file_size)*100)

    val = xbee.read(4) #second four bytes of the file are the log_start timestamp
    log_start = int.from_bytes(val, byteorder='little')
    print('log_start {0}'.format(log_start))
    bytes_downloaded = bytes_downloaded + 4

    #read 13 byte chunks until 13 bytes of 1's are seen, this is the EOF
    exit = False
    stop_code = b'\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff'
    while not exit:
        val = xbee.read(13)
        if val == b'' or val == stop_code:
            exit = True
            break
        xbee_buffer.append(val)
        bytes_downloaded = bytes_downloaded + 13
        pbar.setValue((bytes_downloaded/file_size)*100)

    #Use the data file name to make a folder to put the CSV data
    csv_name = filename[:-4]
    csv_output_folder = '../data/'+csv_name+'_csv_data'
    if not os.path.isdir(csv_output_folder):
        os.mkdir(csv_output_folder)

    #create one csv file for every type of CAN messages
    #this makes handling the data easier because each data row will have the
    #same timestamp
    output_file_dict = {}
    output_csv_dict = {} #list of output file objects
    output_csv_dict_col_map = {} #list of names of data columns
    for k in CAN_SPEC.Data_Pos_Dict.keys():
        csv_file = open(csv_output_folder+'/'+csv_name+'_'+k+'.csv', 'w')
        output_file_dict[k] = csv_file
        output_csv_dict[k] = csv.writer(csv_file)
        col_keys = list(CAN_SPEC.Data_Pos_Dict[k].keys())
        output_csv_dict_col_map[k] = col_keys
        col_name_header = ['TIMESTAMP']
        col_name_header.extend(col_keys)
        output_csv_dict[k].writerow(col_name_header)

    #parse data file buffer and put data into appropriate CSV files
    for i in xbee_buffer:
        data_line = i
        print('Raw Data: {0}'.format(data_line))

        timestamp, ID, MSG_data  = parseMessage(data_line, log_start)

        print('timestamp: {0}'.format(timestamp))
        print('ID: {0}'.format(ID))
        print('MSG_data: {0}\n'.format(MSG_data))

        out = [timestamp]
        for k in output_csv_dict_col_map[ID]:
            out.append(MSG_data[k])
        output_csv_dict[ID].writerow(out)

    #CLOSE ALL THE FILES
    for k,v in output_file_dict.items():
        v.close()

    print(csv_output_folder)
    return csv_output_folder
