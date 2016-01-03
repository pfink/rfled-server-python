#!/usr/bin/env python

import time
import socket, sys
import logging
import logging.handlers
from struct import *

# logging

syslog = logging.getLogger('MyLogger')
syslog.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

syslog.addHandler(handler)

try:
    # Set admin server settings
    UDP_IP = '' # Leave empty for Broadcast support
    BROADCAST_IP = '192.168.0.255'
    ADMIN_PORT = 48899

    INT_IFACES = [  
                    {"ip": '192.168.0.13', "mac": 'b827eb515d78'},
                    {"ip": '192.168.0.52', "mac": '001122334455'}
                 ]               

    # Create UDP socket, bind to it
    socket_protocol = socket.IPPROTO_UDP
    adminsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    adminsock.bind((UDP_IP, ADMIN_PORT))
    adminsock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    responsesocks = {}
    for (i, iface) in enumerate(INT_IFACES):
        responsesock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        responsesock.bind((iface["ip"], ADMIN_PORT))
        responsesocks[iface["ip"]] = responsesock

    syslog.info("rfled-server admin.py started")

    # Loop forever
    while True:
        raw_buffer = adminsock.recvfrom(64)[0]
        ip_header = raw_buffer[0:20]        
        iph = unpack('!BBHHHBBH4s4s' , ip_header)

        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        admindata = raw_buffer[21:]

        # Debug
        # print(', Source:'+ str(s_addr) + ', Destination:' + str(d_addr))
        # print(admindata)

        if admindata is not None:
            response_target_addr = (s_addr, ADMIN_PORT)         
            response_data = bytes('+ok', "utf-8") # On all common requests, send OK
            
            if d_addr == BROADCAST_IP:                                                      # On broadcast, send one response_data per virtual interface
                for iface in INT_IFACES:                    
                    if str(admindata).find("Link_Wi-Fi") != -1:                             # Specific case: If "Link_Wi-Fi" is requested
                        response = iface["ip"] + ',' + iface["mac"] + ',' 
                        response_data = bytes(response, "utf-8")                            # return our IP/MAC instead of OK.

                    responsesocks[iface["ip"]].sendto(response_data, response_target_addr)
                    time.sleep(0.05)                                                        # Make a pause to improve reliability
            elif d_addr in responsesocks:                                                   # On direct request
                responsesocks[d_addr].sendto(response_data, response_target_addr)           # send OK with requested interface
        else:
            break
except:
    syslog.critical("rfled-server admin.py:" + str(sys.exc_info()[1]))
    raise