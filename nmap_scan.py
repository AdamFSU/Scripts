#!/usr/local/bin/python3

# python module imports
import os
import shutil
import nmap
import smtplib
from email.message import EmailMessage
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
nm.scan(hosts='192.168.1.69/24', arguments='-n -sn')
# Retrieve results for all hosts found
nm.all_hosts()
# For every host result, write their mac address and ip to the $mac_list file
for host in nm.all_hosts():
    # If 'mac' expression is found in results write results to file
    if 'mac' in nm[host]['addresses']:
        f.write(str(nm[host]['addresses']) + "\n")
    # If 'mac' expression isn't found in results print warning
    else:
        print("MAC address not found in results, make sure you run this script as root!")

# Close file for editing
f.close()
# Open file for reading
f = open(mac_list, "r")
# Read each line of file and store it in a list
mac_addresses = f.read().splitlines()
# Close file for reading
f.close()
# Open masterfile for reading
f2 = open(masterfile, "r")
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
f3 = open(scanlog, 'a')
# If the new_devices list is empty
if len(new_devices) == 0:
    # Write in scanlog file: All is well on: [date]
    f3.write("\n- - - - All is well on: " + datetime.now().strftime("%Y_%m_%H:%M") + " - - - -\n")
else:
    # Write in scanlog file: New Devices on the LAN: {LIST OF DEVICES}
    f3.write("\nWARNING!! NEW DEVICE(S) ON THE LAN!! - UNKNOWN MAC ADDRESS(ES): " + str(new_devices) + "\n")
    # Create an email message object
    msg = EmailMessage()
    # Email description
    msg.set_content("WARNING!! NEW DEVICE(S) ON THE LAN!!\n\nUNKNOWN MAC ADRESS(ES): " + str(new_devices))
    # Email subject
    msg['Subject'] = "NEW DEVICE(S) ON THE LAN!"
    # From email
    msg['From'] = "email@adress.com"
    # To email
    msg['To'] = "email@adress.com"
    # Create SMTP server call which will send the email
    s = smtplib.SMTP('localhost')
    # send email
    s.send_message(msg)
    # Quit SMTP server call
    s.quit()

# Close the scanlog file
f3.close()
