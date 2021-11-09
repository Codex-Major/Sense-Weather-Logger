import time
import sys
import json
from genericpath import exists
from datetime import datetime
from sense_hat import SenseHat
sense=SenseHat()
defaultFilePath="./weatherlog" # File extensions are added by the script
defaultFormat="text" # text | json | log | csv
defaultIncrement=10  # Daily: 60*60*24 | Hourly: 60*60 | Every 15min: 60*15
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
    --format            Format of logfile. Supported: text | json | log | csv... Default: {}
        text -          Good for output to .txt logfiles...
        json -          JavaScript Object Notation file support for .json logfiles...
        csv  -          Work In Progress...
        log  -          Work In Progress...
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
    dofl=False
    if(len(sys.argv)) >= 1:
        cmdargs=sys.argv[1:]
        if ("--log" in cmdargs[0:]):
            if ("--noconfirm" in cmdargs[0:]):
                sys.stderr.write("[!] Please use either --log or --noconfirm. Not both.\n")
            fp=input("[->] Filepath/name of log file without an extension. Default:{}>> ".format(defaultFilePath))
            if fp=="":
                fp=defaultFilePath
            logging=True
        if ("--noconfirm" in cmdargs[0:]):
            if ("--log" in cmdargs[0:]):
                sys.stderr.write("[!] Please use either --log or --noconfirm. Not both.\n")
            fp=defaultFilePath
            logging=True
        if ("--format" in cmdargs[0:]):
            if not("--log" or "--noconfirm" in cmdargs[0:]):
                sys.stderr.write("[!] You must be using --log or --noconfirm to use --format.\n")
                exit()
            frmtIndx=cmdargs.index("--format")
            frmt=cmdargs[frmtIndx+1]
            if (frmt=="text" or frmt=="json" or frmt=="log" or frmt=="csv"):
                sys.stdout.write('[*] Format "{}" selected.\n'.format(frmt))
            else:
                sys.stderr.write("[!] Please use a supported format: text | json | log | csv \n")
                exit()
        if ("--increment" in cmdargs[0:]):
            try:
                incIndx=cmdargs.index("--increment")
                inc=cmdargs[incIndx+1]
                inc=int(inc)
            except ValueError:
                sys.stderr.write("[!] I think you used --increment with something other than an integer.\n")
                sys.stdout.write("[?] If you tried an increment like...60*60*24...then change the defaultIncrement on line 10.\n")
                exit(0)
            incIndx=cmdargs.index("--increment")
            inc=cmdargs[incIndx+1]
            inc=int(inc)
        if ("--help" in cmdargs[0:]):
            sys.stderr.write(helpTxt)
            exit(0)
    x=0
    tt=0
    humidity=sense.get_humidity()
    pressure=sense.get_pressure()
    temp=sense.get_temperature()
    htemp=sense.get_temperature_from_humidity()
    ptemp=sense.get_temperature_from_pressure()
    while(running==True):
        x+=1
        tt=tt+inc
        now=datetime.now()
        dt_str=now.strftime("%d/%m/%Y %H:%M:%S")
        humidity=str(sense.get_humidity())
        pressure=str(sense.get_pressure())
        temp=str(sense.get_temperature())
        htemp=str(sense.get_temperature_from_humidity())
        ptemp=str(sense.get_temperature_from_pressure())
        sys.stdout.write("-----------------------------------------------------------\n")
        sys.stdout.write("Timestamp: %s " % dt_str+"\n")
        sys.stdout.write("Humidity: "+humidity+"\n")
        sys.stdout.write("Pressure: "+pressure+"\n")
        sys.stdout.write("Temp: "+temp+"\n")
        sys.stdout.write("Temp(humidity): "+htemp+"\n")
        sys.stdout.write("Temp(pressure): "+ptemp+"\n")
        sys.stdout.write("-----------------------------------------------------------\n")
        if(logging==True):
            if (x>=2):
                sys.stdout.write("[*] It has been {} seconds since start.\n".format(tt))
            dt_strd=str(dt_str)
            pressured=str(pressure)
            tempd=str(temp)
            htempd=str(htemp)
            ptempd=str(ptemp)
            if (frmt=="text" or frmt==".txt"):
                if not(".txt" in fp):
                    sys.stderr.write("[!] Not a supported text file extension. Try .txt ...\n")
                    exit(0)
                data=[
                    "Timestamp: "+dt_strd+"\n",
                    "Humidity: "+humidity+"\n",
                    "Pressure: "+pressured+" Millibar\n",
                    "Temp: "+tempd+" C\n",
                    "Temp(humidity): "+htempd+" C\n",
                    "Temp(pressure): "+ptempd+" C\n",
                    "--------------------------------------------\n"]
                with open(fp, 'a') as f:
                    sys.stdout.write("[*] Now Logging data in {}...\n".format(fp))
                    f.writelines(data)
            if (frmt=="json" or frmt==".json"):
                if not(".json" in fp):
                    sys.stderr.write("[!] Not a valid json file extension.\n")
                    exit(0)
                data={
                    "Timestamp":dt_strd,
                    "Humidity":humidity,
                    "Pressure":pressured,
                    "Temp":tempd,
                    "Temp(humidity)":htempd,
                    "Temp(pressure)":ptempd}
                if exists(fp):
                    sys.stdout.write("[*] File {} exists.\n".format(fp))
                    with open(fp,'r') as f:
                        wdata=json.load(f)
                        weather=wdata['weather']
                        wdata['weather'].append(data)
                else:
                    sys.stderr.write("[!] File does not exist. Creating new file.\n")
                    wdata={}
                    wdata['weather']=[]
                    wdata['weather'].append(data)
                sys.stdout.write("[*] Logging data in {}...\n".format(fp))
                with open(fp,'w') as f:
                    json.dump(wdata,f,indent=4)
            if (frmt=="log" or frmt==".log"):
                if not(".log" in fp):
                    sys.stderr.write("[!] Not a valid .log file...\n")
                    exit(0)
                data = str("date:"+dt_strd+" hum:"+humidity+" press:"+pressured+" temp:"+tempd+" htmp:"+htempd+" ptmp:"+ptempd+"\n")
                sys.stdout.write("[*] Logging data in {}...\n".format(fp))
                with open(fp,'a') as f:
                    f.writelines(data)
            if (frmt=="csv" or frmt==".csv"):
                if exists(fp):
                    sys.stdout.write("[!] .csv file exists, assuming it already has a header.")
                    dofl=False
                else:
                    dofl=True
                    fl=str('"Date/Time","Humidity","Pressure","Temp","TempFromHumidity","TempFromPressure"\n')
                if not(".csv" in fp):
                    sys.stderr.write("[!] Not a valid .csv file...\n")
                    exit(0)
                data = str('"'+dt_strd+'","'+humidity+'","'+pressured+'","'+tempd+'","'+htempd+'","'+ptempd+'"\n')
                sys.stdout.write("[*] Logging data in {}...\n".format(fp))
                with open(fp,'a') as f:
                    if dofl==True:
                        f.writelines(fl)
                    else:
                        f.writelines(data)
        time.sleep(inc)    
except KeyboardInterrupt:
    sys.stderr.write("[!] Ctrl+C Interrupt!\n")
    sys.stdout.write("[*] Cleaning up and Exiting!\n")
    sense.clear()
    if (logging==True):
        f.close()
    if(NameError):
        running=False
        exit(0)
    running=False
    exit(0)
