from shutil import ExecError
import time
import sys
import json
from datetime import datetime
from sense_hat import SenseHat
sense=SenseHat()
defaultFilePath="./weather.log" # The script will add .txt, .json or .csv accordingly resulting in ./weather.log.txt
defaultFormat="text" # Formats: text | json(WIP) | csv(WIP)
defaultIncrement=60  # Daily: 60*60*24 
helpTxt="""
--------------------------------------------------------------------------------------------
~PiSense-Weather-Logger~
Author: Codex-Major

Notes:
    You may change the defaultFilepath on line 6 to wherever you'd like your logfile to go.
    You may also change the defaultIncrement on line 7 to any number of seconds. 
    
Arguments:
    --help              Shows this message.
    --log               Prompts the user for an output file.
    --noconfirm         Skips the prompt and uses the default filepath / increment: {} / {}
    --log-format        Format of logfile. Supported: text ... Default: {}
    --increment         The time between checks/logs in seconds.... Default: {}

Work In Progress:
    --log-format - Currently the only supported format is text (outputs raw text to .log file)
                    Adding json format..

Usages:
    -No logging with default filepath and increment.
        sudo python3 weather.py
    
    -Logging prompt with default increment.
        sudo python3 weather.py --log
    
    -Logging enabled with default filepath and custom increment.
        sudo python3 weather.py --noconfirm --increment 60
--------------------------------------------------------------------------------------------
""".format(defaultFilePath,defaultIncrement,defaultFormat,defaultIncrement)
try:
    fp=defaultFilePath
    inc=int(defaultIncrement)
    frmt=defaultFormat
    running=True
    logging=False
    if(len(sys.argv)) >= 1:
        cmdargs=sys.argv[1:]
        if ("--log" in cmdargs[0:]):
            fp=input("[->] Filepath/name of log file. Default:{}>> ".format(defaultFilePath))
            if fp=="":
                fp=defaultFilePath
            logging=True
        if ("--noconfirm" in cmdargs[0:]):
            fp=defaultFilePath
            logging=True
        if ("--log-format" in cmdargs[0:]):
            frmtIndx=cmdargs.index("--log-format")
            frmt=cmdargs[frmtIndx+1]
            if (frmt=="text" or frmt=="json"):
                print("[*] Format {} selected.".format(frmt))
            else:    
                print("[!] Please use a supported format. text || json ")
                exit()
        if ("--increment" in cmdargs[0:]):
            incIndx=cmdargs.index("--increment")
            inc=cmdargs[incIndx+1]
            inc=int(inc)
        if ("--help" in cmdargs[0:]):
            print(helpTxt)
            exit(0)
    x=0
    humidity=sense.get_humidity()
    pressure=sense.get_pressure()
    temp=sense.get_temperature()
    htemp=sense.get_temperature_from_humidity()
    ptemp=sense.get_temperature_from_pressure()
    while(running==True):
        x+=1
        now=datetime.now()
        dt_str=now.strftime("%d/%m/%Y %H:%M:%S")
        humidity=str(sense.get_humidity())
        pressure=str(sense.get_pressure())
        temp=str(sense.get_temperature())
        htemp=str(sense.get_temperature_from_humidity())
        ptemp=str(sense.get_temperature_from_pressure())
        print("-----------------------------------------------------------")
        print("Timestamp: %s " % dt_str)
        print("Humidity: "+humidity)
        print("Pressure: "+pressure)
        print("Temp: "+temp)
        print("Temp(humidity): "+htemp)
        print("Temp(pressure): "+ptemp)
        print("--------------------------------------------------------------")
        if(logging==True):
            #if (x>=2):
                #print("\n[*] It has been {} seconds since last log.\n".format(defaultIncrement))
            dt_strd=str(dt_str)
            pressured=str(pressure)
            tempd=str(temp)
            htempd=str(htemp)
            ptempd=str(ptemp)
            if (frmt=="text"):
                data=["Timestamp: "+dt_strd+"\n","Humidity: "+humidity+"\n","Pressure: "+pressured+" Millibar\n","Temp: "+tempd+" C\n","Temp(humidity): "+htempd+" C\n","Temp(pressure): "+ptempd+" C\n","--------------------------------------------\n"]
                with open(fp, 'a') as f:
                    print("[*] Now Logging data. "+dt_strd+"\n***********************************************************\n")
                    f.writelines(data)

        time.sleep(inc)    
except KeyboardInterrupt:
    print("[!] Ctrl+C Interrupt!")
    print("[*] Cleaning up and Exiting!")
    sense.clear()
    if (logging==True):
        f.close()
    if(NameError):
        running=False
        exit(0)
    running=False
    exit(0)
except ValueError:
    print("[?] I think you used --increment with something other than an integer.")
    exit(0)
