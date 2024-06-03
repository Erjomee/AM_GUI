import random
import socket
import struct
import threading
import time
import zlib

SERVER_IP = "localhost"
SERVER_PORT = 1818

# Function to send data to the dashboard
def send_data(ip, port, data):


    # Make a connection with ther server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print("Connected to the server.")

    data_bytes = bytearray(256)
    data_bytes[2:6] = struct.pack('<i', data["Battery"])  #0

    data_bytes[6:10] = struct.pack('<f', data["Temp1"])  #1
    data_bytes[10:14] = struct.pack('<f', data["Temp2"])  #2
    data_bytes[14:18] = struct.pack('<f', data["Temp3"])  #3

    data_bytes[18:22] = struct.pack('<f', data["LFoot_x"])  #4
    data_bytes[22:26] = struct.pack('<f', data["LFoot_y"])  #5
    data_bytes[26:30] = struct.pack('<f', data["LFoot_z"])  #6
    data_bytes[30:34] = struct.pack('<f', data["RFoot_x"])  #7
    data_bytes[34:38] = struct.pack('<f', data["RFoot_y"])  #8
    data_bytes[38:42] = struct.pack('<f', data["RFoot_z"])  #9

    data_bytes[42:46] = struct.pack('<f', data["LFootCOP_x"])  #10
    data_bytes[46:50] = struct.pack('<f', data["LFootCOP_y"])  #11
    data_bytes[50:54] = struct.pack('<f', data["RFootCOP_x"])  #12
    data_bytes[54:58] = struct.pack('<f', data["RFootCOP_y"])  #13

    data_bytes[58:62] = struct.pack('<f', data["LFootCOP_value"])  #14
    data_bytes[62:66] = struct.pack('<f', data["LFootCOP_vector_x"])  #15
    data_bytes[66:70] = struct.pack('<f', data["LFootCOP_vector_y"])  #16
    data_bytes[70:74] = struct.pack('<f', data["RFootCOP_value"])  #17
    data_bytes[74:78] = struct.pack('<f', data["RFootCOP_vector_x"])  #18
    data_bytes[78:82] = struct.pack('<f', data["RFootCOP_vector_y"])  #19

    data_bytes[82:86] = struct.pack('<f', data["LFoot_time_travel"])  #20
    data_bytes[86:90] = struct.pack('<f', data["RFoot_time_travel"])  #21

    # TEMPERATURE
    data_bytes[90:94] = struct.pack('<f', data["LH_Abd_Temp"])  #22
    data_bytes[94:98] = struct.pack('<f', data["LH_Rot_Temp"])  #23
    data_bytes[98:102] = struct.pack('<f', data["LH_Flex_Temp"])  #24
    data_bytes[102:106] = struct.pack('<f', data["LK_Temp"])  #25
    data_bytes[106:110] = struct.pack('<f', data["LA_Lat_Temp"])  #26
    data_bytes[110:114] = struct.pack('<f', data["LA_Med_Temp"])  #27

    data_bytes[114:118] = struct.pack('<f', data["RH_Abd_Temp"])  #28
    data_bytes[118:122] = struct.pack('<f', data["RH_Rot_Temp"])  #29
    data_bytes[122:126] = struct.pack('<f', data["RH_Flex_Temp"])  #30
    data_bytes[126:130] = struct.pack('<f', data["RK_Temp"])  #31
    data_bytes[130:134] = struct.pack('<f', data["RA_Lat_Temp"])  #32
    data_bytes[134:138] = struct.pack('<f', data["RA_Med_Temp"])  #33

    # AMPERAGE
    data_bytes[138:142] = struct.pack('<f', data["LH_Abd_Amp"])  #34
    data_bytes[142:146] = struct.pack('<f', data["LH_Rot_Amp"])  #35
    data_bytes[146:150] = struct.pack('<f', data["LH_Flex_Amp"])  #36
    data_bytes[150:154] = struct.pack('<f', data["LK_Amp"])  #37
    data_bytes[154:158] = struct.pack('<f', data["LA_Lat_Amp"])  #38
    data_bytes[158:162] = struct.pack('<f', data["LA_Med_Amp"])  #39

    data_bytes[162:166] = struct.pack('<f', data["RH_Abd_Amp"])  #40
    data_bytes[166:170] = struct.pack('<f', data["RH_Rot_Amp"])  #41
    data_bytes[170:174] = struct.pack('<f', data["RH_Flex_Amp"])  #42
    data_bytes[174:178] = struct.pack('<f', data["RK_Amp"])  #43
    data_bytes[178:182] = struct.pack('<f', data["RA_Lat_Amp"])  #44
    data_bytes[182:186] = struct.pack('<f', data["RA_Med_Amp"])  #45

    # Compress the data
    # compressed_data = zlib.compress(data_bytes)

    # Send data to the server
    client_socket.sendall(data_bytes)
    print("Data sent to the server.")

    client_socket.close()


# # # # # # # # # # # Data Sending Simulation # # # # # # # # # # # # # # #
info_dict = {
    # Battery Info
    "Battery": 100,
    # Temperature
    "Temp1": 0.0,
    "Temp2": 0.0,
    "Temp3": 0.0,
    # Destination coordinates
    "LFoot_time_travel": 3,
    "LFoot_x": 0.0,
    "LFoot_y": 0.0,
    "LFoot_z": 0.0,
    "RFoot_x": 0.0,
    "RFoot_y": 0.0,
    "RFoot_z": 0.0,
    # COP coordinates
    "RFoot_time_travel": 3,
    "LFootCOP_x": 0.0,
    "LFootCOP_y": 0.0,
    "RFootCOP_x": 0.0,
    "RFootCOP_y": 0.0,
    # COP Info
    "LFootCOP_value": 30.0,
    "LFootCOP_vector_x": 30.0,
    "LFootCOP_vector_y": 30.0,
    "RFootCOP_value": 30.0,
    "RFootCOP_vector_x": 30.0,
    "RFootCOP_vector_y": -30.0,

    # Temperature
    "LH_Abd_Temp": 0.0,
    "LH_Rot_Temp": 0.0,
    "LH_Flex_Temp": 0.0,
    "LK_Temp": 0.0,
    "LA_Lat_Temp": 0.0,
    "LA_Med_Temp": 0.0,
    
    "RH_Abd_Temp": 0.0,
    "RH_Rot_Temp": 0.0,
    "RH_Flex_Temp": 0.0,
    "RK_Temp": 0.0,
    "RA_Lat_Temp": 0.0,
    "RA_Med_Temp": 0.0,

    # Amperage
    "LH_Abd_Amp": 0.0,
    "LH_Rot_Amp": 0.0,
    "LH_Flex_Amp": 0.0,
    "LK_Amp": 0.0,
    "LA_Lat_Amp": 0.0,
    "LA_Med_Amp": 0.0,

    "RH_Abd_Amp": 0.0,
    "RH_Rot_Amp": 0.0,
    "RH_Flex_Amp": 0.0,
    "RK_Amp": 0.0,
    "RA_Lat_Amp": 0.0,
    "RA_Med_Amp": 0.0,
}


def batteryUpdate():
    global info_dict
    for i in range(100):
        # test_data = [battery, w, c , x,y,pressure,x2,y2,pressure2]
        info_dict["Battery"] -= 1
        temp = info_dict["Battery"]

        info_dict["LH_Abd_Amp"] = temp
        info_dict["LH_Rot_Amp"] = temp
        info_dict["LH_Flex_Amp"] = temp
        info_dict["LK_Amp"] = temp
        info_dict["LA_Lat_Amp"] = temp
        info_dict["LA_Med_Amp"] = temp

        info_dict["RH_Abd_Amp"] = temp
        info_dict["RH_Rot_Amp"] = temp
        info_dict["RH_Flex_Amp"] = temp
        info_dict["RK_Amp"] = temp
        info_dict["RA_Lat_Amp"] = temp
        info_dict["RA_Med_Amp"] = temp
        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(2)



def temperatureUpdate():
    global info_dict
    for i in range(10000):
        # test_data = [battery, w, c, x,y,pressure,x2,y2,pressure2]
        info_dict["Temp1"] = float(random.randint(0, 200))
        info_dict["Temp2"] = float(random.randint(0, 200))
        info_dict["Temp3"] = float(random.randint(0, 200))

        info_dict["LH_Abd_Temp"] = float(random.randint(0, 200))
        info_dict["LH_Rot_Temp"] = float(random.randint(0, 200))
        info_dict["LH_Flex_Temp"] = float(random.randint(0, 200))
        info_dict["LK_Temp"] = float(random.randint(0, 200))
        info_dict["LA_Lat_Temp"] = float(random.randint(0, 200))
        info_dict["LA_Med_Temp"] = float(random.randint(0, 200))

        info_dict["RH_Abd_Temp"] = float(random.randint(0, 200))
        info_dict["RH_Rot_Temp"] = float(random.randint(0, 200))
        info_dict["RH_Flex_Temp"] = float(random.randint(0, 200))
        info_dict["RK_Temp"] = float(random.randint(0, 200))
        info_dict["RA_Lat_Temp"] = float(random.randint(0, 200))
        info_dict["RA_Med_Temp"] = float(random.randint(0, 200))
        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(0.5)



def feetsPositionUpdate():
    global info_dict
    i = 2

    for i in range(100000):
        if i % 2 == 0:
            # Foot in the air
            if i == 0:
                info_dict["LFoot_x"] += 100
                # info_dict["LFoot_y"] += 350
            else:
                info_dict["LFoot_x"] += 200
                # info_dict["LFoot_y"] += 150
            info_dict["LFootCOP_value"] = 0
            # Foot in the ground
            info_dict["RFootCOP_x"] = random.randint(-85, 235)
            info_dict["RFootCOP_y"] = random.randint(-80, 80)
            info_dict["RFootCOP_value"] = random.randint(10, 30)
        else:
            # Foot in the air
            info_dict["RFoot_x"] += 200
            # info_dict["RFoot_y"] += 150
            info_dict["RFootCOP_value"] = 0
            # Foot in the ground
            info_dict["LFootCOP_x"] = random.randint(-85, 235)
            info_dict["LFootCOP_y"] = random.randint(-80, 80)
            info_dict["LFootCOP_value"] = random.randint(10, 30)

        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(0.05) #max frequencies
        # time.sleep(1)



time.sleep(2)

# Create threads
t1 = threading.Thread(target=batteryUpdate)
t2 = threading.Thread(target=temperatureUpdate)
t3 = threading.Thread(target=feetsPositionUpdate)

# # Start threads
t1.start()
t2.start()
t3.start()

# Wait for both threads to finish
t1.join()
t2.join()
t3.join()