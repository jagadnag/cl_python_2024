#!/usr/bin/env python
import os
from getpass import getpass
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException

# Check environment variable for login credentials, if that fails, use getpass().
username = os.getenv("NETMIKO_USERNAME") if os.getenv("NETMIKO_USERNAME") else input('Enter username: ')
password = os.getenv("NETMIKO_PASSWORD") if os.getenv("NETMIKO_PASSWORD") else getpass()

# Sending device ip's stored in a file
with open('device_list') as f:
    device_list = f.read().splitlines()

# Sending list of show commands stored in a file 
with open('show_command') as f:
    show_commands = f.readlines()

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
    # Error handling parameters
    try:
        net_connect = ConnectHandler(**ios_device)
    except (NetmikoAuthenticationException):
        print ('Authentication failure: ' + ip_address_of_device)
        continue
    except (NetmikoTimeoutException):
        print ('Timeout to device: ' + ip_address_of_device)
        continue
    except (EOFError):
        print ("End of file while attempting device " + ip_address_of_device)
        continue
    except (SSHException):
        print ('SSH Issue. Are you sure SSH is enabled? ' + ip_address_of_device)
        continue
    except Exception as unknown_error:
        print ('Some other error: ' + str(unknown_error))
        continue

    # Iterate through command list and print the output
    net_connect = ConnectHandler(**ios_device)
    for command in show_commands:
        output = net_connect.send_command(command)
        print (command + output + '\n')
    net_connect.disconnect()    