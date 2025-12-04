"""
TODO:
- Packet sniffing setup w/NPCAP; capture and decrypt all Albion traffic
- Decoding/Parsing: Identify loot & XP packets
- Internal representation: create "lootevent" or "xpevent" objects
    - Loot: Item ID, qty, who picked up, timestamp
    - XP: Fame type, qty, timestamp
- Append objects to JSON file
"""
#Sam's laptop IP: 192.168.1.146

import pcapy
import socket
import json
import time
import netifaces

def pick_interface():

    #search for all available interfaces with NPCAP
    interfaces = pcapy.findalldevs()
    if not interfaces:
        raise Exception("No NPCAP interfaced Detected. Check internet connection!")
    
    print ("Found NPCAP interfaces:")

    #lists out all interfaces (debug)
    for i in enumerate(interfaces):
        print(i)