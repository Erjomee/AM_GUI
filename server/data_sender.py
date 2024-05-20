import random
import socket
import struct
import threading
import time

SERVER_IP = "localhost"
SERVER_PORT = 1818

def send_data(ip, port, data):

    # Make a connection with ther server 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    print("Connected to the server.")

    data_bytes = bytearray(128)
    data_bytes[2:6] = struct.pack('<i', data[0])
    data_bytes[6:10] = struct.pack('<f', data[1])
    data_bytes[10:14] = struct.pack('<f', data[2])

    starting_point_index = 14
    for i in range(3,9):
        data_bytes[starting_point_index:starting_point_index+4] = struct.pack('<i', data[i])
        starting_point_index +=4

    # for point in range(6):
    #     data_bytes[starting_point_index:starting_point_index+4] = struct.pack('<i', random.randint(-85, 235))
    #     starting_point_index += 4


    # Send data to the server
    client_socket.sendall(data_bytes)
    print("Data sent to the server.")

    client_socket.close()


# Test data to send
battery = 100
w = 0.0
c = 0.0

x = random.randint(-85, 235)
y = random.randint(-80, 80)
pressure = 10

x2 = random.randint(-85, 235)
y2 = random.randint(-80, 80)
pressure2 = 10



def batteryUpdate():
    global battery
    for i in range(100):
        test_data = [battery, w, c , x,y,pressure,x2,y2,pressure2]
        send_data(SERVER_IP, SERVER_PORT, test_data)
        time.sleep(2)
        battery -= 1

def temperature():
    global w, c , x,y,pressure,x2,y2,pressure2
    for i in range(10000):
        test_data = [battery, w, c, x,y,pressure,x2,y2,pressure2]
        send_data(SERVER_IP, SERVER_PORT, test_data)
        time.sleep(0.03)
        w = float(random.randint(0, i))
        c = float(random.randint(0, i))
        x = random.randint(-85, 235)
        y = random.randint(-80, 80)
        pressure = 10

        x2 = random.randint(-85, 235)
        y2 = random.randint(-80, 80)
        pressure2 = 10


time.sleep(2)

# Create threads
t1 = threading.Thread(target=batteryUpdate)
t2 = threading.Thread(target=temperature)

# Start threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()