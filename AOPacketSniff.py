"""
TODO:
- Packet sniffing setup w/NPCAP; capture and decrypt all Albion traffic
- Decoding/Parsing: Identify loot & XP packets
- Internal representation: create "lootevent" or "xpevent" objects
    - Loot: Item ID, qty, who picked up, timestamp
    - XP: Fame type, qty, timestamp
- Append objects to JSON file
"""

import pcapy
import netifaces
import datetime
import socket
import sys
import re
import json

def list_interfaces():

    devices = pcapy.findalldevs()

    if not devices:
        raise Exception("No NPCAP interfaces found! Check your NPCAP installation...")

    print("NPCAP devices: ")
    for i, device in enumerate(devices):
        print(f"  {i}:  {device}")

    print("")
    return devices

def select_interface(interfaces):
    
    ranked_ifaces = []

    #this big loop here assigns a score to each network interface, ranking it by using keywords
    #...to increase or decrease scores that represent how likely it is to be a good interface.
    for interface in interfaces:
        score = 0
        #address = netifaces.ifaddresses(interface) #TODO: Fix this shit
        name_lower = interface.lower() # Making all names lowercase makes it easier to look for keywords

        print("checking interface: ", interface) #debug

        # logic chain from hell incoming

        # interface MUST have IPv4
        #if netifaces.AF_INET in address:
        #    score += 20
        #    print("  has ipv4") #debug

        # prefer wifi or ethernet wording, more likely to be what we want
        if "wi-fi" in name_lower:
            score += 5
            print("  has wifi") # debug
        elif "wifi" in name_lower:
            score += 5
            print("  has wifi") # debug
        elif "ethernet" in name_lower:
            score += 4 # slightly lower because I don't have ethernet all the time 
            print("  has wifi") # debug

        # Loopback will not work because it directs back to your own computer
        if "loopback" in name_lower:
            score -= 20
            print("  loopback :/") # debug

        # virtual machines are not good for this
        if "vmware" in name_lower:
            score -= 5
            print("  is a VM :/") # debug
        elif "virtual" in name_lower:
            score -= 5
            print("  is a VM :/") # debug
        elif "vbox" in name_lower:
            score -= 5
            print("  is a VM :/") # debug

        ranked_ifaces.append((score, interface))
        print("")

    # interfaces are sorted according to score
    ranked_ifaces.sort(reverse = True)
    bestScore, bestInterface = ranked_ifaces[0]
    print("\nSelected interface: ", bestInterface, "\nScore: ", bestScore)

    # return most desireable interface
    return bestInterface

def packet_handle(myIP, logfile, header, data):
        ts = header.getts()[0]
        timestamp = datetime.datetime.fromtimestamp(ts).isoformat()

        # Parse the first 20 bytes of IP header (safe enough)
        if len(data) < 34:  
            return  # too small to be useful

        # IP header fields
        srcIP = socket.inet_ntoa(data[26:30])
        dstIP = socket.inet_ntoa(data[30:34])

        # Only record packets addressed TO ME
        if myIP and dstIP != myIP:
            return

        entry = {
            "timestamp": timestamp,
            "src": srcIP,
            "dst": dstIP,
            "length": len(data),
            "raw_hex": data.hex()  # store encrypted Albion packet
        }

        logfile.write(json.dumps(entry) + "\n")

        print(f"[{timestamp}] {srcIP} → {dstIP}  ({len(data)} bytes)")

def resolve_real_interface(npcap_name):
    
    #Given NPCAP name like '\Device\NPF_{GUID}',
    #return real interface name like 'Wi-Fi' or 'Ethernet'.

    # Extract GUID from NPCAP name
    m = re.search(r'\{([0-9A-Fa-f\-]+)\}', npcap_name)
    if not m:
        return None

    target_guid = m.group(1).lower()

    # Now compare to the GUIDs in netifaces
    for iface in netifaces.interfaces():
        iface_lower = iface.lower()
        if target_guid in iface_lower:
            return iface

    return None

def main():
    # finds and selects optimal interface 
    interfaces = list_interfaces()
    bestInterface = select_interface(interfaces)

    # sniffer starts listening on best interface, filters for UDP packets because that is what Albion uses
    sniffer = pcapy.open_live(bestInterface, 999999, False, 50)
    sniffer.setfilter("udp")

    print("Listening for packets... Press any key to stop")

    #*****WRITE THE CODE HERE*******

    try:
        real_iface = resolve_real_interface(bestInterface)

        if real_iface is None:
            raise Exception(f"Could not map NPCAP interface '{bestInterface}' to a real interface name.")

        address = netifaces.ifaddresses(bestInterface)
        myIP = address[netifaces.AF_INET][0]['addr']

    except:
        raise Exception("Could not determine you IP address! what? how?")

    logFile = open("traffic_log.jsonl", "a")

    try:
        sniffer.loop(0, packet_handle(myIP, logFile))
    except KeyboardInterrupt:
        print("\nStopping capture...")
    
    logFile.close()

main()