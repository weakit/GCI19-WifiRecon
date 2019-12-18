#!/usr/bin/env python3
import ipaddress
import netifaces
import subprocess
import time
import os
from concurrent.futures import ThreadPoolExecutor

addrs = []
IP = "127.0.0.1"
CLEAR_WHEN_DONE = True


def get_mac(ip):
    """Gets the mac + name from the ARP cache"""
    p = os.popen('arp -e ' + str(ip))
    try:
        li = [x for x in p.readlines()[1].split(' ') if x]
    except IndexError:
        return None
    return li[2], ('Unknown' if li[0] == str(ip) else li[0])


def check_addr(ip):
    """Check if address is reachable"""
    if ping(str(ip)):
        addrs.append(ip)


def ping(ip):
    """Pings an address"""
    # if 0, connection didn't fail
    return subprocess.call(['ping', '-c', '1', ip]) == 0


def choose_iface():
    print("Available Interfaces:\n")
    ifaces = netifaces.interfaces()
    for n, x in enumerate(ifaces):
        print('%s: %s' % (n, x))
    return ifaces[int(input('\nChoose interface to scan for devices: '))]


def get_addresses(iface):
    global IP
    addresses = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]
    IP = addresses['addr']
    return ipaddress.ip_network(addresses['addr'] + '/' + addresses['netmask'], strict=False)


def executePool(addrs):
    print("\nPinging all addresses in subnet %s." % str(addrs))
    print("\n --------  IGNORE TEXT --------\n")
    time.sleep(2)
    with ThreadPoolExecutor(max_workers=len(list(addrs))) as exec:
        exec.map(check_addr, addrs)
    print(" --------  IGNORE TEXT --------\n")


if __name__ == '__main__':
    executePool(get_addresses(choose_iface()))
    if CLEAR_WHEN_DONE:
        subprocess.call('clear')
    print("%s device(s) found.\n" % len(addrs))
    for addr in addrs:
        if str(addr) == IP:
            print(IP, (15 - len(IP)) * ' ', "This Device")
            continue
        mac = get_mac(addr)
        print(addr, (15 - len(str(addr))) * ' ', mac[0], mac[1])
