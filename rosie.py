#! /usr/bin/env python3
import scapy.all as scapy
import sys
#import os
import time



request = scapy.ARP()

request.pdst = '137.112.228.214/24'
broadcast = scapy.Ether()

broadcast.dst = 'ff:ff:ff:ff:ff:ff'

request_broadcast = broadcast / request
clients = scapy.srp(request_broadcast, timeout=1)[0]
for element in clients:
    print(element[1].psrc + "     " + element[1].hwsrc)

