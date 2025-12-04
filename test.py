import netifaces
import pcap

devs = pcap.findalldevs()
for i, dev in enumerate(devs):
    print(f"  {i}:  {dev}")

#print(netifaces.gateways())

address = netifaces.ifaddresses(devs[5])