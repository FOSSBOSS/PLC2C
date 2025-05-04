#!/usr/bin/env python3
import os
# ansi color codes failed me after building and EXE
from colorama import init, Fore, Style
init(autoreset=True)
import threading               # faclitate time simulation 
import serial.tools.list_ports # from pyserial pkg
#import shutil
import subprocess
import sys
import time
from time import sleep

# you need to put AO suite tools in your windows path for this program to work right
# This code assumes that this is true
'''
Compile exe:
pyinstaller --onefile  PLC_Brute.py

Why compile an open source project?
You populate your passwords list, and distribute the program.

Use of this project is at your own risk, educational purposes only.
Zero liability, 



############## CLI VERSION 0.00.1 ##############
0. Define functions
1. Print a basic useage guide
2. Comence password guessing.
  
'''
################# 0. Functions #######

# keep the output screen clear
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


# PLC Physical Connection status:
def detect_idec_plc():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Display all port info
        print(f"{port.device}: {port.description}")
        if "IDEC" in port.description.upper():
            print(f"{Fore.GREEN}Found IDEC PLC on {port.device}{Style.RESET_ALL}")
            return port.device
    print(f"{Fore.RED}No IDEC PLC found{Style.RESET_ALL}")
    return None

def wait_for_plc_connection():
    try:
        while True:
            a = detect_idec_plc()
            if a:
                print("PLC Connection verified.")
                return a
            else:
                print("Please connect the IDEC PLC. Retrying in 10 seconds... (Press Ctrl+C to cancel)")
                sleep(10)
    except KeyboardInterrupt:
        print("\nUser aborted the program.")
        exit(1)


#################### 1. Basic Useage Guide ###############################
def guide():
    print(f"{Fore.GREEN}#### Welcome to IDEC PLC BRUTE ####")
    print(f"This program uses a password dictionary to reset the password on an IDEC PLC {Fore.RED}")
    print(f"{Fore.GREEN}PLC_Brute requires Automation Organizer 4.8 or later")
    print(f"\nWhy use this program?\n")
    print(f"1. Forgotten Passwords")
    print(f"2. Blank a PLC")
    print(f"3. Secure Disposal")
    print(f"\nThis code if successful WILL blank your PLC")
    print(f"The result of which is no more password")
    print(f"\nIf you need the code on you PLC {Fore.RED}DO NOT USE this PROGRAM\n")
    print(f"Application run time is N passwords * 60 seconds")
    print(f"Populate your dictionary wisely.")
    print(f"This program requires an IDEC PLC connected via USB to run") 
    #print(f"") 
    #print(f"") 
   
    input(f"\nPress {Fore.GREEN}ENTER{Style.RESET_ALL} to continue \nor {Fore.RED}CTRL+C{Style.RESET_ALL} to exit: ")
guide()
cls()

   
################ 6. Verify Hardware & Conectivity  #########################
print(f"{Fore.GREEN}Verifying Hardware Connectivity:{Style.RESET_ALL}")
wait_for_plc_connection()

'''
# on IDEC systems Passwords are Alpha numeric, and case senitive, 
# this means there is 62^8th possiblities, and each pass takes about 
60 seconds to run. Choose your password list wisely. Lest ye wittness 
the heat death of the universe before completion. or maybe its 90s, ...
'''
passwords = [
""  # sometimes you get lucky
"password",
"userpass",
"DRYW00D1",
"HardPass",
]

# 6000 years of waiting, might look better with a per step percent
def show_progress(estimated_duration, process_done_flag):
    start = time.time()
    max_percent = 95
    while not process_done_flag["done"]:
        elapsed = time.time() - start
        percent = int((elapsed / estimated_duration) * max_percent)
        percent = min(percent, max_percent)
        print(f"\rProgress: {percent}% completed", end='', flush=True)
        time.sleep(1)
 
def PLC_NULL():
    for index, pwd in enumerate(passwords):
        if index > 10:
            cls()
        command = [
            "DataFileManager.exe", "\\PLC", "-S", "\\download",
            "-C", ".\\null.zld", "USB", f"pass-{pwd}"
        ]
        print(f"Trying password: {pwd}")
        estimated_duration = 90  # seconds per try 
        process_done_flag = {"done": False}
        progress_thread = threading.Thread(target=show_progress, args=(estimated_duration, process_done_flag))
        progress_thread.start()
        
        result = subprocess.run(command)
        
        process_done_flag["done"] = True
        progress_thread.join()
        # IF THE PLC is already BLANK, the first try will always succeed, no mater what you give it for a password.
        if result.returncode == 1:
            print(f"[+] Success with password: {pwd}")
            break
        else: 
            print(f"{pwd}") # look man idec do weird things
            #break  
    # The thing about DataFileMangager.exe is it doesnt return values. Monitoring it is pointless.
    print("PLC is now blank")
#Fail Fast, Fail Often

if __name__ == "__main__":   
    cls() 
    print(f"When this program finishes, your PLC will be blank,\n but the password will be gone")
    print(f"Which is what you need to do to reprogram a system with an unknown password")
    print(f"This program may take an exceptionaly long time to run. ")
    print(f"")
    print(f"")
    PLC_NULL()

    print("PLC Errased")
    print(f"\n{Fore.GREEN}completed all processes sucessfully{Style.RESET_ALL}\n") # IDECs Downloader.exe does some funny stuff...
    print(f"\n{Fore.GREEN}Retry your upgrades, reprograming, or disposal of your unit.")
    
    sleep(30)
    sys.exit()
    
