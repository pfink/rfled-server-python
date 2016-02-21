import socket
import serial
from util import escalate_thread_exceptions


@escalate_thread_exceptions
def run_milight_bridge(ip, ttl_port, cfg):
    # Create UDP socket, bind to it
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.bind((ip, cfg['led_port']))

    # Connect to serial
    ser = serial.Serial(ttl_port, cfg['ttl_speed'])

    while True:
        data, addr = sock.recvfrom(64) # buffer size is 64 bytes

        if data is not None:
            # print("led command: ", str(data)) # Debugging
            ser.write(data) # Write packet data out