#!/usr/bin/env python
import os
import csv
from getpass import getpass
from netmiko import ConnectHandler
from pprint import pprint
from tabulate import tabulate

# Check for environment variable, if that fails, use getpass().
password = os.getenv("NETMIKO_PASSWORD") if os.getenv("NETMIKO_PASSWORD") else getpass()
username = os.getenv("NETMIKO_USERNAME") if os.getenv("NETMIKO_USERNAME") else input('Enter username: ')


# Creating a list for storing inventory data
inventory = []
title = ["Hostname", "Chassis", "Serial No", "os", "version"]
inventory.append(title)

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

    # Connect to device and collect date
    net_connect = ConnectHandler(**ios_device)
    output = net_connect.send_command('show version', use_genie=True)
    net_connect.disconnect()

    # Extracting output fields that are parsed by genie
    hostname = output["version"]["hostname"]
    chassis = output["version"]["chassis"]
    serial = output["version"]["chassis_sn"]
    os = output["version"]["os"]
    version = output["version"]["version"]

    # Adding stored values to inventory list
    device_details = [hostname, chassis, serial, os, version]
    inventory.append(device_details)


# Printing the inventory list to table
print(tabulate(inventory, headers="firstrow", tablefmt="grid"))

# Store the inventory data to files
with open("inventory.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(inventory)
