import sys
import os
import collections, itertools
import csv

import CAN_SPEC
from xbeeParser import parseMessage

#converts a whole file of raw CAN messages into a bunch of CSVs
def raw_to_csv(file_obj):
    file_obj.seek(0)
    #Extract the name of the data file
    file_path = file_obj.name.split('/')

    #Use the data file name to make a folder to put the CSV data
    csv_name = file_path[-1][:-4]
    csv_output_folder = '../data/'+csv_name+'_csv_data'
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
    exit = False
    while not exit:
        # timestamp_ID_MSGLEN_MSG_LineCount
        # ASCCI_ ASCII_ASCII_ BYTES_ASCII
        data_line = ''

        under_count = 0
        while under_count < 3:
            val = file_obj.read(1).decode()
            print(val)
            if val == '':
                exit = True
                break
            if val == '_':
                under_count = under_count + 1
            data_line += val

        if exit:
            break

        split_data = data_line.split('_')
        payload_len = int(split_data[2])
        payload = file_obj.read(payload_len)

        newline = 0
        while not newline:
            val = file_obj.read(1).decode()
            print(val)
            if val == '':
                break
            if val == '\n':
                newline = 1
                break
            data_line += val

        timestamp, ID, MSG_data  = parseMessage(data_line, payload)
        out = [timestamp]
        for k in output_csv_dict_col_map[ID]:
            out.append(MSG_data[k])
        output_csv_dict[ID].writerow(out)

    #CLOSE ALL THE FILES
    for k,v in output_file_dict.items():
        v.close()

    return csv_output_folder

#converts a downloaded file of raw CAN messages into a bunch of CSVs
#parses output until the xbee sends 'end\n'
def xbee_to_csv(xbee, filename):
    #read the data coming from the xbee into a giant buffer before parsing it
    xbee_buffer = collections.deque()
    while xbee.in_waiting > 0:
        val = xbee.read(1)
        if val == b'\n':
            xbee_buffer.append(val)

    #Use the data file name to make a folder to put the CSV data
    csv_name = filename[:-4]
    csv_output_folder = '../data/'+csv_name+'_csv_data'
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
    exit = False
    i = 0
    while not exit:
        # timestamp_ID_MSGLEN_MSG_LineCount
        # ASCCI_ ASCII_ASCII_ BYTES_ASCII
        print('Reading new line...')
        data_line = ''

        under_count = 0
        while under_count < 3:
            val = xbee_buffer[i]
            i = i + 1
            print(val)
            val = val.decode()
            if val == '_':
                under_count = under_count + 1
            data_line += val
            if data_line == 'end':
                print('End of file reached')
                exit = True
                break

        if exit:
            break

        split_data = data_line.split('_')
        print('split_data: {0}'.format(split_data))
        payload_len = int(split_data[2])
        payload = list(itertools.islice(xbee_buffer, i, i+payload_len))
        i = i + payload_len
        payload = xbee.read(payload_len)

        newline = 0
        while not newline:
            val = xbee_buffer[i]
            i = i + 1
            print(val)
            val = val.decode()
            if val == '\n':
                newline = 1
                break
            data_line += val

        print('raw_data: {0}'.format(data_line))
        timestamp, ID, MSG_data  = parseMessage(data_line, payload)
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
