import logging
from scapy.all import sniff, Dot11, Dot11ProbeReq
from termcolor import colored, cprint
import argparse
import datetime
import sys

mac_list = []
interface = "mon0"

# csv format = Registry,Assignment,Organization Name,Organization Address
macs = open("oui.csv", "r")
macs = macs.read().split("\n")
for mac in macs:
    mac = mac.split(",")

    if len(mac) > 2:
        print(mac[1], mac[2])


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


def main:
    




# sniff(iface=interface, prn=analyzePacket, store=0)
