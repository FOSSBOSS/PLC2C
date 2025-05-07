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

# Full path to the Data File Manager EXE
# r"" raw string litteral -- dont interepret BS as escapes chars
ao_exe = r"C:\Program Files (x86)\IDEC\IDEC Automation Organizer\Data File Manager\DataFileManager.exe"

# Optional: Verify the file exists
if not os.path.isfile(ao_exe):
    print(f"Executable not found: {ao_exe}")
    exit(1)

'''
Compile exe:
pyinstaller --onefile  PLC_Brute.py

Why compile an open source project?
You populate your passwords list, and distribute the program.. maybe

Use of this project is at your own risk, educational purposes only.
Zero liability implied.  
 
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
    print(f"{Fore.YELLOW}Disclaimer:{Style.RESET_ALL}")
    print("This tool is provided strictly for educational purposes.")
    print("The author assumes no responsibility for damage, data loss, or unintended behavior.")
    print("Use entirely at your own risk.")
    print("By continuing, you acknowledge that you understand and accept these conditions.\n")
    input("If you agree to these terms, press Enter, or CTRL+C to exit")

    print(f"{Fore.GREEN}#### Welcome to IDEC PLC BRUTE ####{Style.RESET_ALL}")
    print(f"This program uses a password dictionary to remove the password from an IDEC PLC.")
    print(f"{Fore.GREEN}NOTE: Requires Automation Organizer 4.8 or later.{Style.RESET_ALL}")

    print(f"\nWhy use this program?\n")
    print(f"  1. Recover forgotten passwords")
    print(f"  2. Erase and blank a PLC")
    print(f"  3. Prepare a device for secure disposal")

    print(f"\n{Fore.RED}WARNING: This operation will ERASE your PLC completely!{Style.RESET_ALL}")
    print("As a result, the password will be removed, but all logic/program data will be lost.")

    print(f"\nIf you need the program code on the PLC, {Fore.RED}DO NOT USE THIS TOOL.{Style.RESET_ALL}")
    print(f"\nEstimated run time: number of passwords × ~10 seconds each.")
    print("Choose your password list wisely.")
    print(f"\nMake sure an IDEC PLC is {Fore.GREEN}connected via USB{Style.RESET_ALL} before proceeding.")
    
    input(f"\nPress {Fore.GREEN}ENTER{Style.RESET_ALL} to continue,\nor press {Fore.RED}CTRL+C{Style.RESET_ALL} to cancel and exit: ")

    sleep(0.5)

    input(f"\n{Fore.RED}FINAL WARNING:{Style.RESET_ALL} This will permanently erase your PLC.\n"
          f"Press {Fore.GREEN}ENTER{Style.RESET_ALL} to proceed, or {Fore.RED}CTRL+C{Style.RESET_ALL} to abort: ")

    #print(f"{Fore.GREEN}   {Style.RESET_ALL}") 
    #print(f"{Fore.RED}     {Style.RESET_ALL}") 
    #print(f"{Fore.YELLOW}  {Style.RESET_ALL}") 

guide()
cls()
   
################ 6. Verify Hardware & Conectivity  #########################
print(f"{Fore.GREEN}Verifying Hardware Connectivity:{Style.RESET_ALL}")
wait_for_plc_connection()
'''
# on IDEC systems Passwords are Alpha numeric, and case senitive, 
# this means there is 62^8th possiblities. A successful write takes 
about 90 seconds to run, while a fail should happen in under 10s. 
Choose your password list wisely. Lest ye wittness 
the heat death of the universe before completion...
'''

def show_progress(estimated_duration, process_done_flag):
    start = time.time()
    max_percent = 95
    while not process_done_flag["done"]:
        elapsed = time.time() - start
        percent = int((elapsed / estimated_duration) * max_percent)
        percent = min(percent, max_percent)
        print(f"\rProgress: {percent}% completed", end='', flush=True)
        time.sleep(1)

passwords = [
    "",  # sometimes you get lucky with a blank password
    "userp1ss",
    "password",
    "userpass",
    "ThatPass",
    "HardPass",
    "sage420"
]

THRESHOLD = 10  # seconds
INSTALL_DURATION = 90  # estimated real install time

def PLC_NULL():
    run_time = 0

    for index, pwd in enumerate(passwords):
        print(f"\n[{index}] Trying password: {pwd}")

        # Setup shared flag and progress thread
        process_done_flag = {"done": False}
        progress_thread = threading.Thread(
            target=show_progress,
            args=(INSTALL_DURATION, process_done_flag)
        )

        # Start timer and progress bar
        start = time.time()
        progress_thread.start()

        try:
            subprocess.run([ao_exe, "\\PLC", "-S", "\\download",
                "-C", ".\\null.zld", "USB", f"pass-{pwd}"
            ], timeout=120)
        except subprocess.TimeoutExpired:
            print(f"\n[!] Timeout occurred with: {pwd}")
            process_done_flag["done"] = True
            progress_thread.join()
            continue

        duration = time.time() - start
        run_time += duration

        # Stop progress bar now that the process is done
        process_done_flag["done"] = True
        progress_thread.join()

        if duration > THRESHOLD:
            print(f"\n[+] Success likely with password: {pwd} index: {index}")
            break
        #else:
        #    print("\n[-] Failed quickly — continuing...")
    else:
        print(f"\n[×] All passwords failed.\nTotal runtime: {run_time:.2f} seconds")



if __name__ == "__main__":
    
    cls() 
    print("When this program completes, the PLC will be fully erased — including its password.")
    print("This is necessary in order to reprogram a system when the password is unknown.")
    print("Please note: this process may take a significant amount of time to complete.")
    print("The program will also display the most likely former password used.")
    print()

    PLC_NULL()

    sleep(30)
    sys.exit()
