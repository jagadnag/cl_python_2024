#!/usr/bin/env python
from netmiko import ConnectHandler
from pprint import pprint

# SSH Connection Details
ios1 = {
    'device_type': 'cisco_ios',
    'ip': '198.18.1.11',
    'username': 'cisco',
    'password': 'cisco',
}

# Establish SSH to device and use genie to parse command output
net_connect = ConnectHandler(**ios1)
output = net_connect.send_command('show version', use_genie=True)
net_connect.disconnect()
print(output)

# Pretty print output to readable format 
print()
pprint(output)
print()