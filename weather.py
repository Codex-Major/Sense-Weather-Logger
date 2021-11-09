import time
import sys
import json
from genericpath import exists
from datetime import datetime
from sense_hat import SenseHat
sense=SenseHat()
defaultFilePath="./weatherlog" # File extensions are added by the script
defaultFormat="text" # text | json | csv(WIP)
defaultIncrement=10  # Daily: 60*60*24 
helpTxt="""
--------------------------------------------------------------------------------------------
~PiSense-Weather-Logger~
Author: Codex-Major

Notes:
    You may change the defaultFilepath on line 8 to wherever you'd like your logfile to go.
    You may change the defaultFormat on line 9 to your desired default format.
    You may also change the defaultIncrement on line 10 to any number of seconds. 
    
Arguments:
    --help              Shows this message.
    --log               Prompts the user for an output file...
    --noconfirm         Skips the prompt and uses the default filepath / increment: {} / {}
    --format            Format of logfile. Supported: text | json ... Default: {}
        text -          Good for output to .log and .txt files...
        json -          JavaScript Object Notation file support...
        csv  -          Work In Progress...
    --increment         The time between checks/logs in seconds.... Default: {}

Usages:
    -No logging with default filepath and increment...
        sudo python3 weather.py
    
    -Logging prompt with default increment...
        sudo python3 weather.py --log --format
    
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
            if ("--noconfirm" in cmdargs[0:]):
                print("[!] Please use either --log or --noconfirm. Not both.")
            fp=input("[->] Filepath/name of log file without an extension. Default:{}>> ".format(defaultFilePath))
            if fp=="":
                fp=defaultFilePath
            logging=True
        if ("--noconfirm" in cmdargs[0:]):
            if ("--log" in cmdargs[0:]):
                print("[!] Please use either --log or --noconfirm. Not both.")
            fp=defaultFilePath
            logging=True
        if ("--format" in cmdargs[0:]):
            if not("--log" or "--noconfirm" in cmdargs[0:]):
                print("[!] You must be using --log or --noconfirm to use --format.")
                exit()
            frmtIndx=cmdargs.index("--format")
            frmt=cmdargs[frmtIndx+1]
            if (frmt=="text" or frmt=="json"):
                print("[*] Format {} selected.".format(frmt))
            else:
                if (frmt=="csv"):
                    print("[!] CSV format is a Work In Progress...use another for now..")
                    exit()
                print("[!] Please use a supported format: text | json | csv(WIP) ")
                exit()
        if ("--increment" in cmdargs[0:]):
            try:
                incIndx=cmdargs.index("--increment")
                inc=cmdargs[incIndx+1]
                inc=int(inc)
            except ValueError:
                print("[?] I think you used --increment with something other than an integer.")
                print("[?] If you tried an increment like...60*60*24...then change the defaultIncrement on line 10.")
                exit(0)
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
            if (x>=2):
                print("[*] It has been {} seconds since last log.\n".format(inc))
            dt_strd=str(dt_str)
            pressured=str(pressure)
            tempd=str(temp)
            htempd=str(htemp)
            ptempd=str(ptemp)
            if (frmt=="text"):
                if not(".txt" or ".log" in fp):
                    print("[!] Not a valid text file extension. Try .txt or .log ...")
                    exit()
                data=[
                    "Timestamp: "+dt_strd+"\n",
                    "Humidity: "+humidity+"\n",
                    "Pressure: "+pressured+" Millibar\n",
                    "Temp: "+tempd+" C\n",
                    "Temp(humidity): "+htempd+" C\n",
                    "Temp(pressure): "+ptempd+" C\n",
                    "--------------------------------------------\n"]
                with open(fp, 'a') as f:
                    
                    print("[*] Now Logging data. "+dt_strd+"\n***********************************************************")
                    f.writelines(data)
            if (frmt=="json"):
                if not(".json" in fp):
                    print("[!] Not a valid json file.")
                    exit()
                data={
                    "Timestamp":dt_strd,
                    "Humidity":humidity,
                    "Pressure":pressured,
                    "Temp":tempd,
                    "Temp(humidity)":htempd,
                    "Temp(pressure)":ptempd}
                if exists(fp):
                    print("[*] File {} exists.".format(fp))
                    with open(fp,'r') as f:
                        wdata=json.load(f)
                        weather=wdata['weather']
                        wdata['weather'].append(data)
                    #with open(fp,'w') as f:
                    #    json.dump(wdata,f,indent=4)
                else:
                    print("[!] File does not exist. Creating new file.")
                    wdata={}
                    wdata['weather']=[]
                    wdata['weather'].append(data)
                print("[*] Logging data in {}.".format(fp))
                with open(fp,'w') as f:
                    json.dump(wdata,f,indent=4)

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
