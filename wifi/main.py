import logging
from scapy.all import sniff, Dot11, Dot11ProbeReq
from termcolor import colored, cprint
import argparse
import datetime
import sys

mac_list = []
interface = "mon0"

# csv format = Registry,Assignment,Organization Name,Organization Address


def get_oui_info(mac):

    pass


def printAccessPoint(mac, ssid):
    print(colored("* Encontrado * ", "red", attrs=["bold"]) + "%s" % (mac),
          colored("Ponto de Acesso", "yellow", attrs=["bold"]), "do SSID:",
          colored(ssid, "green", attrs=["bold"]))


def printClient(mac, ssid):
    print(colored("* Encontrado * ", "red", attrs=["bold"]) + "%s" % (mac),
          colored("Cliente", "yellow", attrs=["bold"]), "do SSID:",
          colored(ssid, "green", attrs=["bold"]))


def analyzePacket(packet):
    if packet.haslayer(Dot11):
        if packet.type == 0 and packet.subtype == 8:
            if packet.addr2 not in mac_list:
                mac_list.append(packet.addr2)
                printAccessPoint(packet.addr2, packet.info)

        if packet.haslayer(Dot11ProbeReq):
            if packet.addr2 not in mac_list:
                mac_list.append(packet.addr2)
                if packet.info != "":
                    printClient(packet.addr2, packet.info)


if __name__ == '__main__':
    print('---------')
    if len(sys.argv) == 1:
        mac = [input("Enter MAC Address: ")]
    else:
        mac = [item for item in sys.argv[1::]]
    for addr in mac:
        get_oui_info(addr)


# sniff(iface=interface, prn=analyzePacket, store=0)
