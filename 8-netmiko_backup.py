#!/usr/bin/env python
import os, time
from datetime import datetime
from getpass import getpass
from netmiko import ConnectHandler


print(datetime.now())
# Check for environment variable, if that fails, use getpass().
password = os.getenv("NETMIKO_PASSWORD") if os.getenv("NETMIKO_PASSWORD") else getpass()
username = os.getenv("NETMIKO_USERNAME") if os.getenv("NETMIKO_USERNAME") else input('Enter username: ')

# Collect login credentials
#username = input('Enter your SSH username: ')
#password = getpass('Enter your password: ')

# Create backup folder
if not os.path.exists('backup/'):
    os.mkdir('backup')
    
# Sending device ip's stored in a file
with open('device_list') as f:
    device_list = f.read().splitlines()

# Iterate through device list and configure the devices
for devices in device_list:
    print ('Connecting to device ' + devices)
    ip_address_of_device = devices
    ios_device = {
        'device_type': 'cisco_ios',
        'ip': ip_address_of_device,
        'username': username,
        'password': password
    }

    # Connect to device and collect running config
    net_connect = ConnectHandler(**ios_device)
    
    # Getting hostname and storing it as filename variable
    hostname = net_connect.find_prompt()[:-1]

    # Collecting running config output
    print (f'Initiating config backup on {hostname}..')
    output = net_connect.send_command("show run")
    #print(output)

    # Saving running config to file
    with open(f'backup/{hostname}.cfg', 'w') as file:
        file.write(output)

    print ('Finished config backup \n')
    net_connect.disconnect()
    time.sleep(3)

print(datetime.now())
