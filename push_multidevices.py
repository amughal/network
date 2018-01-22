#!/usr/bin/env python3

import paramiko
from datetime import datetime
import time
import sys
import configparser

def connect(router):

    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    try:
        remote_conn_pre.connect(router, username=username, password=password, look_for_keys=False, allow_agent=False)
    except:
        print("Cannot connect to host:",router)
        exit()
    remote_conn = remote_conn_pre.invoke_shell()
    print ("\nSSH session established to:",router)

    # Return connection object 
    return remote_conn

if __name__ == '__main__':

    #start_time = datetime.time()
    if str(sys.argv) == 0:
        print ("Usage: ",sys.argv[0]," <routers.db> <commands.list>")
        exit

    config = configparser.ConfigParser()
    try:
        config.readfp(open(r'configuration.txt'))
        username = config.get('Authentication', 'username')
        password = config.get('Authentication', 'password')
    except FileNotFoundError:
        print ("Error reading configuration.txt")
        exit() 

    paramiko.util.log_to_file('demo.log')

    routers = sys.argv[1]
    commands = sys.argv[2]

    with open(routers) as fp1:
        start_time = datetime.now()
        for dev in fp1:
            dev = dev.strip()
            remote_conn = connect(dev)
            time.sleep (2)
            remote_conn.send("\r\n")
            time.sleep (1)
            print ('Issuing commands ', end='')

            with open(commands) as fp2:
                for cmd in fp2:
                    #remote_conn.send("terminal length 0\n")
                    #print (cmd)
                    remote_conn.send(cmd)
                    time.sleep(1)
                    #print ( str(remote_conn.recv(80000)).strip()+"\r" )
                    print('.', end='', flush=True)

            print("Done.")
            remote_conn.close()

    end_time = datetime.now()
    time_taken = end_time - start_time
    print ("\nTotal processing time ",time_taken)

