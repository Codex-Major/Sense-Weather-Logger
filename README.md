# PiSense-Weather-Logger
```
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
        csv  -          Comma Separated Values for veiwing .csv with MS:Excel.
        log  -          Simple .log file format.
    --increment         The time between checks/logs in seconds.... Default: {}
Usages:
    -No logging with default filepath and increment...
        sudo python3 weather.py
    
    -Logging prompt with default increment...
        sudo python3 weather.py --log --format
    
    -Logging enabled with default filepath and custom increment.
        sudo python3 weather.py --noconfirm --increment 60
```
