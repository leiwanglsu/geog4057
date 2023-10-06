import os
def readSingleECM(filename,new_pos_dict):
    raw_file = open(filename)

    pos_dict = {}
    GPS_disc = {}
    ysi_dict = {}
    ECM_dict = {}
    while True:
        nstr = raw_file.readline()
        if len(nstr) == 0:
            break
        else:
            strs = nstr.split()
            if(strs[0]=="POS"):
                device_tag = int(strs[1])
                time_tag = float(strs[2])
                pos_dict[time_tag] = [float(strs[3]),float(strs[4])]
            if(strs[0]=="ECM"):
                device_tag = int(strs[1])
                time_tag = float(strs[2])
                number_data = int(strs[3])
                data = [0 for _ in range(number_data)]
                for i in range(number_data):
                    data[i]=float(strs[i + 4])
                ECM_dict[time_tag] = data
    for ecm in ECM_dict.items():
        search_key = ecm[0]
        print(search_key)
        key = min(pos_dict.keys(), key = lambda key: abs(key-search_key))
        new_pos_dict[key] = [search_key,pos_dict[key],ecm[1]]
    return new_pos_dict
def readECM(pathname):
    pos_dict = {}
    for filename in os.listdir(pathname):
        f = os.path.join(pathname, filename)
        file_extension = os.path.splitext(f)[1]
        if(file_extension == ".RAW"):
            pos_dict = readSingleECM(f,pos_dict)
    return pos_dict