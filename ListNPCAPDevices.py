"""
This program is for finding all interfaces sniffable by NPCAP; To find which one connects to the internet, 
1. find your own IP address (you can use the ipconfig command)
2. Run this program to list all NPCAP devices
3. 
3. in powershell, run: powershell -command "Get-NetAdapter | Format-List Name,InterfaceDescription,InterfaceGuid"
4. This will list all your devices network interfaces, match the one 
"""

import pcapy

for dev in pcapy.findalldevs():
    print(dev)