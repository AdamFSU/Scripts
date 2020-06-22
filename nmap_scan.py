#!/usr/local/bin/python3

# *** NOTE: THIS SCRIPT MUST BE RUN AS ROOT ***

# python module imports
import os
import shutil
import nmap
import sys
import socket
import subprocess
from datetime import datetime

# variable containing the filepath of the nmap scan results file
mac_list = os.environ['HOME'] + "/maclist.log"

# variable containing the filepath of the approved mac addresses on the LAN file
masterfile = os.environ['HOME'] + "/master_mac"

# variable containing the filepath of the log file which documents every scan result
scanlog = os.environ['HOME'] + "/macscan.log"

# If a file from previous nmap scans exists, create a backup of the file
if os.path.exists(mac_list):
    shutil.copyfile(mac_list, os.environ['HOME'] + '/maclist_' + datetime.now().strftime("%Y_%m_%H:%M") + '.log.bk')

# Open a new file for the new nmap scan results
f = open(mac_list, "w+")

# Print to console this warning
print("Don't forget to update your network in the nmap scan of this script")

# This block of code will scan the network and extract the IP and MAC address
# Create port scanner object, nm
nm = nmap.PortScanner()
# Perform: nmap -oX - -n -sn 192.168.1.69/24
# *** NOTE: -sP has changed to -sn for newer versions of nmap! ***
nm.scan(hosts='192.168.1.69/24', arguments='-n -sn')
# Retrieve results for all hosts found
nm.all_hosts()
# For every host result, write their mac address and ip to the $mac_list file
for host in nm.all_hosts():
    # If 'mac' expression is found in results write results to file
    if 'mac' in nm[host]['addresses']:
        f.write(str(nm[host]['addresses']) + "\n")
    # If 'mac' expression isn't found in results print warning
    elif nm[host]['status']['reason'] != "localhost-response":
        print("MAC addresses not found in results, make sure you run this script as root!")

# Close file for editing
f.close()
# Open file for reading
f = open(mac_list, "r")
# Read each line of file and store it in a list
mac_addresses = f.read().splitlines()
# Close file for reading
f.close()
# Open masterfile for reading
if os.path.isfile(masterfile):
    f2 = open(masterfile, "r")
else:
    print("Could not find master_mac file! Verify file path is correct!")
    sys.exit()

# Read each line of file and store it in a list
master_mac_addresses = f2.read().splitlines()
# Close file for reading
f2.close()

# Create empty list of new devices found on network
new_devices = []

# For every list entry in the mac_addresses list
for i in mac_addresses:
    # Convert the list index from a string to a dictionary so we can parse out mac address for comparison
    dic = eval(i)
    # Compare mac address portion of dictionary to mac addresses in the master_mac_addresses file
    # If the scanned mac address is not in the master_mac_addresses file
    if dic['mac'] not in master_mac_addresses:
        # Add scanned mac address to new devices list
        new_devices.append(dic)

# Open scanlog file for appending
if os.path.isfile(scanlog):
    f3 = open(scanlog, 'a')
else:
    print("Could not find macscan.log file! Verify file path is correct!")
    sys.exit()

# If the new_devices list is empty
if len(new_devices) == 0:
    # Write in scanlog file: All is well on: [date]
    f3.write("\n- - - - All is well on: " + datetime.now().strftime("%Y_%m_%H:%M") + " - - - -\n")
else:
    warning = "\nWARNING!! NEW DEVICE(S) ON THE LAN!! - UNKNOWN MAC ADDRESS(ES): " + str(new_devices) + "\n"
    print(warning)
    # Write in scanlog file: New Devices on the LAN: {LIST OF DEVICES}
    f3.write(warning)

    try:
        # First command which gets PIPEd to second command
        p1 = subprocess.Popen(['echo', '-e', '\nWARNING!!'], stderr=subprocess.PIPE, universal_newlines=True,
                              stdout=subprocess.PIPE)
        # Second command which takes input from first command
        p2 = subprocess.Popen(['mutt', '-e', 'my_hdr From:user@email.com', '-s', 'WARNING!! NEW DEVICE ON THE '
                                                                                       'LAN',
                               '-i', 'maclist.log', 'user@email.com'], stdin=p1.stdout, stdout=subprocess.PIPE)
        output = p2.communicate()
        # Print output of running command
        print(output)
    except OSError as e:
        print("Error sending email: {0}".format(e))
    except subprocess.SubprocessError as se:
        print("Error sending email: {0}".format(se))

# Close the scanlog file
f3.close()

