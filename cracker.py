#!/usr/bin/python
import hashlib
import colorama
from colorama import Fore, Style, init
import http.client
import _thread
import sys

found = False
guesses = 0

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def thr_cracking(hash, chunk, complete):
    global found
    global guesses
    for i in range(len(chunk)):
        if found == False:
            guesses += 1
            text = chunk[i].strip()
            if len(hash) == 32: #md5
                if hash == hashlib.md5(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
            elif len(hash) == 40: #sha1
                if hash == hashlib.sha1(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
            elif len(hash) == 56: #sha224
                if hash == hashlib.sha224(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
            elif len(hash) == 64: #sha256
                if hash == hashlib.sha256(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
            elif len(hash) == 96: #sha384
                if hash == hashlib.sha384(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
            elif len(hash) == 128: #sha512
                if hash == hashlib.sha512(str.encode(text)).hexdigest():
                    found = True
                    print(Fore.GREEN + "\n[+] Found " + hash + " -> " + text)
                    return
        else:
            return

def hashing():
    print("What kind of HASHING")
    print("1. md5")
    print("2. sha1")
    print("3. sha224")
    print("4. sha256")
    print("5. sha384")
    print("6. sha512")
    hash_algorythm = input("Enter the number: ")
    text = input("Enter the thing to be Hashed: ")

    if hash_algorythm == "1":
        result = hashlib.md5(str.encode(text))
    elif hash_algorythm == "2":
        result = hashlib.sha1(str.encode(text))
    elif hash_algorythm == "3":
        result = hashlib.sha224(str.encode(text))
    elif hash_algorythm == "4":
        result = hashlib.sha256(str.encode(text))
    elif hash_algorythm == "5":
        result = hashlib.sha384(str.encode(text))
    elif hash_algorythm == "6":
        result = hashlib.sha512(str.encode(text))
    else:
        print(Fore.RED + "Option not Found!")
        hashing()
        return

    print(text, "=", result.hexdigest())

def cracking():
    global found
    global guesses
    hash = input("Enter the Hash: ")
    oh = input("DO YOU WANT ONLINE DATASET? [Y/N]: ")

    d = []

    if oh.lower() == "y":
        print("Loading data...")
        conn = http.client.HTTPSConnection("raw.githubusercontent.com")
        conn.request("GET", "/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt")
        r1 = conn.getresponse()
        if r1.code != 200 or r1.code != 304:
            od = str(r1.read()).split('\\')
            for i in range(len(od)):
                d.append(od[i][1:])
        else:
            print(Fore.RED + "\nError while fetching data")
            return
        
    elif oh.lower() == "n":
        pwlist = input("Enter name of password list: ")
        print("Loading data...")
        try:
            with open(pwlist) as f:
                line = f.readline()
                while line:
                    line = line[:-1]
                    d.append(line)
                    line = f.readline()
        except FileNotFoundError:
            print(Fore.RED + "File not found!")
            return

    else:
        print("Please choose y or n")
        return
            
    data = list(chunks(d, 100))
    print("Processing " + str(len(data)) + " chunks and " + str(len(d)) + " words")
    complete = len(d)
    for i in range(len(data)):
        if found == False:
            chunk = data[i]
            _thread.start_new_thread(thr_cracking, (hash, chunk, complete))
    while found == False:
        if guesses >= complete:
            print(Fore.RED + "\nNot Found")
            break
            
    print("\n")

def main():
    global guesses
    global found
    init(autoreset=True)
    print("HashCracker")
    try:
        while True:
            ch = input("To Hash press 1 and to Crack Hash press 2: ")
            if ch == "1":
                hashing()
            elif ch == "2":
                guesses = 0
                found = False
                cracking()
            else:
                print("This option is not found please select 1 or 2")
    except KeyboardInterrupt:
        print("\nBye")
        print(Style.RESET_ALL)

if __name__ == '__main__':
    main()