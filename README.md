RFLED-Server
============

Python Scripts to run UDP servers to emulate a LimitlessLED WiFi Bridge 4.0 unit.

This fork aims to provide functionality for multiple milight bridges on a single device such as the Raspberry Pi.

Install
=======

 * Change the variables in both scripts to meet your needs
 * Start the scripts and they will start the UDP listeners

Startup Script
==============

 * Place script into /etc/init.d/
 * a) Ensure scripts are in /usr/local/bin/ or
 * b) Adjust path in rfled-server script to path of the scripts
 * Run update-rc.d rfled-server defaults to set up
 
Running
=======

 * Run "/etc/init.d/rfled-server start" to start scripts without a restart


Support for multiple milight bridges
==============

 * Make sure the hardware device has multiple UART interfaces and connect the milight bridges to them (I tested it with CP2104 USB-to-Serial Adapter Carrier on the Raspberry Pi 2 -> https://www.pololu.com/product/1308)
 * For each additional milight bridge, add a virtual interface with it's own IP and MAC address. Please consider that DHCP probably won't work with these virtual interfaces, so you have to assign static IPs to them. On Linux/Rasbian, you can create virtual interfaces by adding the following lines to /etc/network/interfaces:
```
auto vlan.milight1
iface vlan.milight1 inet static
   address 192.168.0.52
   netmask 255.255.255.0
   gateway 192.168.0.1
   pre-up ip link add link eth0 vlan.milight1 address 00:11:22:33:44:55 type macvlan mode bridge
   post-down ip link delete dev vlan.milight1
```
 * Reboot the device
 * Adjust the variables within the scripts according to your own configuration