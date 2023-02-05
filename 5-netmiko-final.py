
#!/usr/bin/env python
from getpass import getpass
from netmiko import ConnectHandler
from netmiko import NetmikoAuthenticationException
from netmiko import NetmikoTimeoutException
from paramiko.ssh_exception import SSHException

# Collect login credentials
username = input('Enter your SSH username: ')
password = getpass('Enter your password: ')

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

    # Configure the device and save config
    output = net_connect.send_config_from_file('config_commands')
    output += net_connect.save_config()
    net_connect.disconnect()
    print (output)