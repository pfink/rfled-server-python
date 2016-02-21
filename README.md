RFLED-Server
============

Python Scripts to run UDP servers to emulate a LimitlessLED WiFi Bridge 4.0 unit.

This fork aims to provide functionality for multiple milight bridges on a single device such as the Raspberry Pi.

Install
=======

 1. Install `python3` and `python3-yaml` on your machine. On new linux distributions, `python3-serial` is also needed.
 2. Take the config.example.yaml and configure it according to your needs. Rename it to config.yml.
 3. Put config.yaml to the source folder or elsewhere (in case of the latter, set the environment variable RFLED_CONFIG_PATH to the path of config.yaml)

Running
=======

Start main.py, e.g. with `python3 main.py`.


Support for multiple milight bridges
==============

 1. Make sure the hardware device has multiple UART interfaces and connect the milight bridges to them (I tested it with CP2104 USB-to-Serial Adapter Carrier on the Raspberry Pi 2 -> https://www.pololu.com/product/1308)
 2. For each additional milight bridge, add a virtual interface with it's own IP and MAC address. Please consider that DHCP probably won't work with these virtual interfaces, so you have to assign static IPs to them. Make sure that `iproute2` is installed.
   
  Method 1: You can create virtual interfaces by adding the following lines to /etc/network/interfaces:
  ```
  auto vlan.milight1
  iface vlan.milight1 inet static
     address 192.168.0.52
     netmask 255.255.255.0
     gateway 192.168.0.1
     pre-up ip link add link eth0 vlan.milight1 address 00:11:22:33:44:55 type macvlan mode bridge
     post-down ip link delete dev vlan.milight1
  ```
  Method 2: On newer operating systems (like Debian Jessie) you could also use systemd-networkd to configure your VLAN. Do it like that:
  
   * Create /etc/systemd/network/eth0.milight1.netdev
   ```
   [NetDev]
   Name=eth0.milight1
   Kind=macvlan
   MACAddress=00:11:22:33:44:55

   [MACVLAN]
   Mode=bridge
   ```
   * Create /etc/systemd/network/eth0.milight1.network
   ```
   [Match]
   Name=eth0.milight1
 
   [Network]
   IPForward=yes
   Address=192.168.0.52
   Gateway=192.168.0.1
   ```
   * Create /etc/systemd/network/eth0.network
   ```
   [Match]
   Name=eth0

   [Network]
   MACVLAN=eth0.milight1
   ```
 3. Reboot the device
 4. Adjust the variables within the scripts according to your own configuration
