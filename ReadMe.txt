HOW TO SETUP NPCAP AND OTHER TOOLS
- download NPCAP from NPCAP website
	- in 'download' section of website, a section with 
	different versions will list a version called 
	'NPCAP SDK 1.15 (ZIP)'

	- Extract this zip to a folder in your C drive called
	"Npcap-sdk"

	- in order to ensure compatability with pcap-ng,
	create another folder in the same place called 
	"wpdpack"
	
	- copy the folder Npcap-sdk/Include/ into your
	wpdpack folder, and also copy Npcap-sdk/Lib/
	into the same folder so wpdpack has both Include
	and Lib and nothing else. 

	- this is needed because 	
	pcapy-ng was build using WinPcap SDK which is now
	obselete, and the library still looks for the old folder
	called wpdpack, so we need to create it ourselves now.

- download pcapy-ng python library
	- After setting up NPCAP, type 
	"pip install pcapy-ng" into your windows console

	- wait for compilation, then run
	"pip install pcapy-ng dpkt" for WinPcap compatability