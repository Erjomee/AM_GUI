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

    data_bytes = bytearray(64)
    data_bytes[2:6] = struct.pack('<i', data[0])
    data_bytes[6:10] = struct.pack('<f', data[1])
    data_bytes[10:14] = struct.pack('<f', data[2])
    data_bytes[14:18] = struct.pack('<f', data[3])
    data_bytes[18:22] = struct.pack('<f', data[4])
    data_bytes[22:26] = struct.pack('<f ', data[5])
    data_bytes[26:30] = struct.pack('<i', 6)

    # Send data to the server
    client_socket.sendall(data_bytes)
    print("Data sent to the server.")

    client_socket.close()


# Test data to send
battery = 100
w = 0.0
c = 0.0
x1 = 10.0
y1 = 20.0
p1 = 3.0


def batteryUpdate():
    global battery
    for i in range(100):
        test_data = [battery, w, c, x1, y1, p1]
        send_data(SERVER_IP, SERVER_PORT, test_data)
        time.sleep(2)
        battery -= 1


def temperature():
    global w, c
    for i in range(1000):
        test_data = [battery, w, c, x1, y1, p1]
        send_data(SERVER_IP, SERVER_PORT, test_data)
        time.sleep(0.5)
        w = float(random.randint(0, i))
        c = float(random.randint(0, i))


# Create threads
t1 = threading.Thread(target=batteryUpdate)
t2 = threading.Thread(target=temperature)

# Start threads
t1.start()
t2.start()

# Wait for both threads to finish
t1.join()
t2.join()