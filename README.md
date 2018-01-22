# Network Scritps to communicate with Aruista and HPE Switches

# There are few files in this directory

1. show_ver.py 
   
Description: Collects active firmware, next boot firmware, serial number etc.

Syntax: python3 show_ver.py arista.db



2. show_inven.py
  
Description: This script provides transceiver inventory for a switch. It reads file with list of switches,
             uses RANCID clogin to login to the switch and collect the output

Syntax: show_inven.py arista.db

3. push_multidevices.py

Description: Sends block of commands to devices

Syntax: python3 push_multidevices.py <cmd.list> <devices.db>


4. configuration.txt

This is a common file for all the scripts:

[Authentication]
username=admin
password=admin_password

[EAPI]
username=user2
password=user2_password




