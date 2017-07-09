import time
import socket
from struct import unpack
from util import escalate_thread_exceptions

@escalate_thread_exceptions
def run_autodiscover_server(cfg):

    # Create UDP socket, bind to it
    socket_protocol = socket.IPPROTO_UDP
    adminsock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    adminsock.bind((cfg['autodiscover_ip'], cfg['autodiscover_port']))
    adminsock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    responsesocks = {}
    macs = {}
    for (i, iface) in enumerate(cfg['interfaces']):
        responsesock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        responsesock.bind((iface["ip"], cfg['autodiscover_port']))
        responsesocks[iface["ip"]] = responsesock
        macs[iface["ip"]] = iface["mac"]
        

    # Loop forever
    while True:
        raw_buffer = adminsock.recvfrom(64)[0]
        ip_raw_header = raw_buffer[0:20]        
        iph = unpack('!BBHHHBBH4s4s' , ip_raw_header)

        version_ihl = iph[0]
        ihl = version_ihl & 0xF
        iph_length = ihl * 4

        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);

        udp_raw_header = raw_buffer[iph_length:]
        udp_ports = unpack("!HH", udp_raw_header[0:4])
        s_port = udp_ports[0]
        d_port = udp_ports[1]     
        admindata = raw_buffer[iph_length+8:]
        

        # Debugging

        #if str(admindata).find("Link_Wi-Fi") != -1:
        #    print(', Source:'+ str(s_addr) + ', Destination:' + str(d_addr))
        #    print("Full UDP data: {}".format(admindata))
        #    print("port: {}".format(d_port))
        #    print("data: "+str(admindata)+ "print port: "+str(d_port))

        if admindata is not None and d_port == cfg['autodiscover_port'] and not (s_addr in responsesocks and s_port == cfg['autodiscover_port']):
            response_target_addr = (s_addr, s_port)
            response_data = bytes('+ok', "utf-8")                                           # Always answer with OK when nothing special is requested
            
            if d_addr == cfg['broadcast_ip']:                                               # On broadcast, send one response_data per virtual interface
                for iface in cfg['interfaces']:
                    if str(admindata).find("Link_Wi-Fi") != -1:                             # Specific case: If "Link_Wi-Fi" is requested
                        response = iface["ip"] + ',' + iface["mac"].replace(":", "").upper() + ','    
                        response_data = bytes(response, "utf-8")                            # return our IP/MAC
                    responsesocks[iface["ip"]].sendto(response_data, response_target_addr)
                    time.sleep(0.05)                                                        # Make a pause to improve reliability
            elif d_addr in responsesocks:
                if str(admindata).find("Link_Wi-Fi") != -1:                                 # Specific case: If "Link_Wi-Fi" is requested                                  
                    response = d_addr + ',' + macs[d_addr].replace(":", "").upper() + ','           # answer with requested interface
                    response_data = bytes(response, "utf-8")
                    
                responsesocks[d_addr].sendto(response_data, response_target_addr)           # else respond normally