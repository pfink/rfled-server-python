#!/usr/bin/env python3

from concurrent import futures
import socket
import serial

# Set LED Control server settings
LED_PORT = 8899
TTL_SPEED = 9600
INT_IFACES = [
                {"ip": '192.168.0.13', "ttl": '/dev/ttyAMA0'},
                {"ip": '192.168.0.52', "ttl": '/dev/ttyUSB0'}
             ]

def run_led_server():
    executor = futures.ThreadPoolExecutor(max_workers=len(INT_IFACES))

    for iface in INT_IFACES:
        executor.submit(run_milight_bridge, iface["ip"], iface["ttl"])


def run_milight_bridge(ip, ttl_port):
    # Create UDP socket, bind to it
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip, LED_PORT))

    # Connect to serial
    ser = serial.Serial(ttl_port, TTL_SPEED)

    while True:
        data, addr = sock.recvfrom(64) # buffer size is 64 bytes

        if data is not None:
            # print("led command: ", str(data)) # Debugging
            ser.write(data) # Write packet data out

run_led_server()