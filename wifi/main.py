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
    mac = mac.replace(":", "").upper().strip()[0:6]

    # find the oui in the csv file

    with open("oui.csv", "r") as f:
        for line in f.readlines():
            info = line.split(",")
            if len(info) > 2:
                if info[1] == mac:
                    return info[2].strip()


def printAccessPoint(mac, ssid):
    print(colored("* Encontrado * ", "red", attrs=["bold"]) + "%s" % (mac),
          colored("Ponto de Acesso", "yellow", attrs=["bold"]), "do SSID:",
          colored(ssid, "green", attrs=["bold"]))
    print("OUI: %s" % (get_oui_info(mac)))


def printClient(mac, ssid):
    print(colored("* Encontrado * ", "red", attrs=["bold"]) + "%s" % (mac),
          colored("Cliente", "yellow", attrs=["bold"]), "do SSID:",
          colored(ssid, "green", attrs=["bold"]))
    print("OUI: %s" % (get_oui_info(mac)))


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
    if len(sys.argv) == 1:
        mac = input("Enter MAC Address: ")
    else:
        mac = sys.argv[1]

    sniff(iface=interface, prn=analyzePacket, store=0)
