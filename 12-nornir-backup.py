#!/usr/bin/env python
import os
from nornir import InitNornir
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result

BACKUP_DIR = "backup/"

# Initiate nornir inventory
nr = InitNornir(
    config_file="config.yml", dry_run=True
)

# Function to Create backup folder
def create_backups_dir():
    if not os.path.exists(BACKUP_DIR):
        os.mkdir(BACKUP_DIR)

# Function to save the device configs to file
def save_config_to_file(hostname, config):
    filename =  f"{hostname}_nornir.txt"
    with open(os.path.join(BACKUP_DIR, filename), "w") as f:
        f.write(config)

# Function to collect the show run from devices
def get_netmiko_backups():
    backup_results = nr.run(
        task=netmiko_send_command, 
        command_string="show run"
        )

    for hostname in backup_results:
        save_config_to_file(
            hostname=hostname,
            config=backup_results[hostname][0].result,
        )

# Main function to invoke other functions
def main():
    create_backups_dir()
    get_netmiko_backups()


if __name__ == "__main__":
    main()
