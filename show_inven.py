#!/usr/bin/env python3

import sys
import subprocess
import configparser
import os
import time

''' This program expects that RANCID is deployed and can login to devices using clogin
'''

def processing(str):

   time.sleep(1)
   if str == "-":
      return "\\"
   elif str == "\\":
      return "|"
   elif str == "|":
      return "/"
   elif str == "/":
      return "-"

str="-"
msg="Working on devices: "

config = configparser.ConfigParser()
config.readfp(open(r'configuration.txt'))
username = config.get('Authentication','username')
password = config.get('Authentication','password')

if len(sys.argv) == 1:
    print ("No filename given with list of devices!")
    sys.exit()

switchlist = []

with open(sys.argv[1],'r') as file:
    switchlist = [x.strip() for x in file.readlines()]

for switch in switchlist:
    str=processing(str)
    print(msg+str, end='\r')
    cmd = "clogin -c 'show inventory | begin Manufacturer' "+switch
    filename = switch+"-optic_inven.txt"
    fh = open(filename,"w")

    raw_inventory = ret=os.popen(cmd).read()
    result = raw_inventory.find('Manufacturer')

    fh.write(raw_inventory[result:])
    fh.close()

print ("\nFinished writing Inventory files in the local directory.\n")

