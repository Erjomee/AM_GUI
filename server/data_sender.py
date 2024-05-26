import random
import socket
import struct
import threading
import time

SERVER_IP = "localhost"
SERVER_PORT = 1818

# Function to send data to the dashboard
def send_data(ip, port, data):

    # Make a connection with ther server 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print("Connected to the server.")

    data_bytes = bytearray(128)
    data_bytes[2:6] = struct.pack('<i', data["Battery"])

    data_bytes[6:10] = struct.pack('<f', data["Temp1"])
    data_bytes[10:14] = struct.pack('<f', data["Temp2"])
    data_bytes[14:18] = struct.pack('<f', data["Temp3"])

    data_bytes[18:22] = struct.pack('<f', data["LFoot_x"])
    data_bytes[22:26] = struct.pack('<f', data["LFoot_y"])
    data_bytes[26:30] = struct.pack('<f', data["RFoot_x"])
    data_bytes[30:34] = struct.pack('<f', data["RFoot_y"])

    data_bytes[34:38] = struct.pack('<f', data["LFootCOP_x"])
    data_bytes[38:42] = struct.pack('<f', data["LFootCOP_y"])
    data_bytes[42:46] = struct.pack('<f', data["RFootCOP_x"])
    data_bytes[46:50] = struct.pack('<f', data["RFootCOP_y"])

    data_bytes[50:54] = struct.pack('<f', data["LFootCOP_value"])
    data_bytes[54:58] = struct.pack('<f', data["LFootCOP_vector_x"])
    data_bytes[58:62] = struct.pack('<f', data["LFootCOP_vector_y"])
    data_bytes[62:66] = struct.pack('<f', data["RFootCOP_value"])
    data_bytes[66:70] = struct.pack('<f', data["RFootCOP_vector_x"])
    data_bytes[70:74] = struct.pack('<f', data["RFootCOP_vector_y"])

    data_bytes[74:78] = struct.pack('<f', data["LFoot_time_travel"])
    data_bytes[78:82] = struct.pack('<f', data["RFoot_time_travel"])

    # starting_point_index = 14
    # for i in range(3,9):
    #     data_bytes[starting_point_index:starting_point_index+4] = struct.pack('<i', data[i])
    #     starting_point_index +=4

    # for point in range(6):
    #     data_bytes[starting_point_index:starting_point_index+4] = struct.pack('<i', random.randint(-85, 235))
    #     starting_point_index += 4

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
    "RFoot_x": 0.0,
    "RFoot_y": 0.0,
    # COP coordinates
    "RFoot_time_travel": 3,
    "LFootCOP_x": 0.0,
    "LFootCOP_y": 0.0,
    "RFootCOP_x": 0.0,
    "RFootCOP_y": 0.0,
    # COP Info
    "LFootCOP_value": 0,
    "LFootCOP_vector_x": 0.0,
    "LFootCOP_vector_y": 0.0,
    "RFootCOP_value": 0,
    "RFootCOP_vector_x": 0.0,
    "RFootCOP_vector_y": 0.0,
}


x = random.randint(-85, 235)
y = random.randint(-80, 80)
pressure = 10

x2 = random.randint(-85, 235)
y2 = random.randint(-80, 80)
pressure2 = 10

def batteryUpdate():
    global info_dict
    for i in range(100):
        # test_data = [battery, w, c , x,y,pressure,x2,y2,pressure2]
        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(2)
        info_dict["Battery"] -= 1
        print(info_dict)


def temperatureUpdate():
    global info_dict

    for i in range(10000):
        # test_data = [battery, w, c, x,y,pressure,x2,y2,pressure2]
        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(0.5)
        info_dict["Temp1"] = float(random.randint(0, i))
        info_dict["Temp2"] = float(random.randint(0, i))
        info_dict["Temp3"] = float(random.randint(0, i))
        print(info_dict)

def feetsPositionUpdate():
    global info_dict

    for i in range(100):
        # test_data = [battery, w, c, x,y,pressure,x2,y2,pressure2]
        send_data(SERVER_IP, SERVER_PORT, info_dict)
        time.sleep(5)
        if i%2 == 0:
            # Foot in the air
            info_dict["LFoot_x"] += 100
            info_dict["LFoot_y"] += 10
            info_dict["LFootCOP_value"] = 0
            # Foot in the ground
            info_dict["RFootCOP_x"] = random.randint(-85, 235)
            info_dict["RFootCOP_y"] = random.randint(-80, 80)
            info_dict["RFootCOP_value"] = 5
        else:
            # Foot in the air
            info_dict["RFoot_x"] += 100
            info_dict["RFoot_y"] += 10
            info_dict["RFootCOP_value"] = 0
            # Foot in the ground
            info_dict["LFootCOP_x"] = random.randint(-85, 235)
            info_dict["LFootCOP_y"] = random.randint(-80, 80)
            info_dict["LFootCOP_value"] = 5

        print(info_dict)

time.sleep(2)

# Create threads
t1 = threading.Thread(target=batteryUpdate)
t2 = threading.Thread(target=temperatureUpdate)
t3 = threading.Thread(target=feetsPositionUpdate)

# Start threads
t1.start()
t2.start()
t3.start()

# Wait for both threads to finish
t1.join()
t2.join()
t3.join()