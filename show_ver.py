#!/usr/bin/env python

from jsonrpclib import Server
import ssl
import sys
import re
import ConfigParser

''' Specific to Arista Switches using EAPI REST calls
'''

config = ConfigParser.ConfigParser()
config.readfp(open(r'configuration.txt'))
username = config.get('EAPI','username')
password = config.get('EAPI','password')

if len(sys.argv) == 1:
   print ("No filename given with list of EOS devices!")
   sys.exit()

ssl._create_default_https_context = ssl._create_unverified_context

dev_list=sys.argv[1]

print ("Device\t\t Model\t\t\tCurrent Fw\tBootConfig\t\t\tSerialNumber")

with open(dev_list) as fp:
   for dev in fp:
      dev=dev.strip()
      try:
          conn_str = username + ":" + password + "@" + dev + "/command-api"
          switch = Server( "https://" + conn_str )
      except:
          print ('TCP connect error to',dev)
          continue
      
      try:
          response_ver = switch.runCmds( 1, [ "show version" ] )
      except:
          print ('Unable to issue commands to', dev)
          continue


      try:
          response_config = switch.runCmds( 1, [ "show boot-config" ] )
      except:
          print ('Unable to issue commands to', dev)
          continue

      model_name = response_ver[0]["modelName"] + "\t" 

      print ("%s\t %s \t%s \t%s \t\t%s" % \
            (dev, \
            model_name.expandtabs(16) if len(response_ver[0]["modelName"]) < 10 else response_ver[0]["modelName"], \
            response_ver[0]["version"], \
            response_config[0]["softwareImage"], \
            response_ver[0]['serialNumber']) \
            )

