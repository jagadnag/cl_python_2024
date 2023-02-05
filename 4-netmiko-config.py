#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

# SSH username and password provided by user
username = input('Enter your SSH username: ')
password = getpass('Enter your password: ')

# Sending device ip's stored in a file 
with open('device_list') as f:
    device_list = f.read().splitlines()

# Iterate through device list and configure the devices 
for device in device_list:
    print ('Connecting to device ' + device)
    ip_address_of_device = device
    
    # SSH Connection details
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device, 
        'username': username,
        'password': password
    }
 
    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_config_from_file('config_commands')
    net_connect.disconnect()
    print (output)
