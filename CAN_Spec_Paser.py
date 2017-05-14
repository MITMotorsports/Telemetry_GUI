from collections import OrderedDict

if __name__ == '__main__':
    with open('../MY17_Can_Library/can_validator/fsae_can_spec.txt', 'r') as in_file:
        with open('CAN_SPEC.py', 'w') as out_file:
            out_file.write('from collections import OrderedDict\n\n')

            #parse for CAN IDs and data
            ID_Dict = {}
            Data_Pos_Dict = {}
            cur_msg_name = ''
            is_little_endian = {}

            current_endian = 0
            for line in in_file:
                if 'MESSAGE_NAME' in line:
                    tmp = line.split(' ')
                    cur_msg_name = tmp[0][13:]
                    print(cur_msg_name)
                    ID = int(tmp[1][3:], 16)
                    print(tmp[1][3:])
                    ID_Dict[ID] = cur_msg_name
                    is_little_endian[cur_msg_name] = current_endian

                if 'ENDIAN=' in line:
                    tmp = line.split('=')
                    tmp_endian = tmp[-1][:-1]
                    print(tmp_endian)
                    if tmp_endian == 'BIG':
                        current_endian = 0
                    else:
                        current_endian = 1

                if 'DATA_NAME' in line:
                    tmp = line.split(' ')
                    print(tmp)
                    data_name = tmp[-2][10:]
                    print(data_name)
                    data_pos = tmp[-1][9:]
                    print(data_pos)
                    data_pos = data_pos.split(':')
                    print(data_pos[0])
                    print(data_pos[1])
                    data_pos = (int(data_pos[0]),int(data_pos[1]))
                    if cur_msg_name in Data_Pos_Dict.keys():
                        Data_Pos_Dict[cur_msg_name][data_name] = data_pos
                    else:
                        Data_Pos_Dict[cur_msg_name] = OrderedDict({data_name:data_pos})

            #Write ID Dictionary in file
            # print(Data_Pos_Dict)
            out_file.write('ID_Dict = {')
            first = 1
            for k,v in ID_Dict.items():
                if first:
                    first = 0
                else:
                    out_file.write(',\n')
                out_file.write(str(k)+':')
                out_file.write('\'' + v + '\'')

            out_file.write('}\n\n')

            #Write data position Dictionary in file
            out_file.write('Data_Pos_Dict = {')
            first = 1
            for k,v in Data_Pos_Dict.items():
                if first:
                    first = 0
                else:
                    out_file.write(',\n')
                out_file.write('\'' + k + '\': ')
                out_file.write('OrderedDict([')
                first_v = 1
                for k_v, v_v in v.items():
                    if first_v:
                        first_v = 0
                    else:
                        out_file.write(', ')
                    out_file.write('(\'' + k_v + '\',(' + str(v_v[0]) + ',' + str(v_v[1]) + '))')
                out_file.write('])')

            out_file.write('}\n\n')

            #Write Endianess Dictionary in file
            out_file.write('is_little_endian = {')
            first = 1
            for k,v in is_little_endian.items():
                if first:
                    first = 0
                else:
                    out_file.write(',\n')
                out_file.write('\'' + k + '\': ')
                out_file.write(str(v))

            out_file.write('}\n\n')

            out_file.close()
        in_file.close()
