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

    ranked_ifaces.sort(reverse = True)
    bestScore, bestInterface = ranked_ifaces[0]
    print("\nSelected interface: ", bestInterface, "\nScore: ", bestScore)

    return bestInterface


interfaces = list_interfaces()
bestInterface = select_interface(interfaces)

print("program done goodbye!")