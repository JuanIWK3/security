import netaddr
import sys

from tempfile import mkstemp
from os import remove, fdopen

import requests

ouilist = requests.get("http://standards-oui.ieee.org/oui.txt")

tmpfd, tmpfile = mkstemp()

with fdopen(tmpfd, "w") as fp:
    fp.write(ouilist.text)

with open(tmpfile, "r") as fp:
    for line in fp:
        if "(base 16)" in line:
            split_line = line.split()
            oui = split_line[0]
            company_name = " ".join(split_line[3:])
            address1 = fp.readline().strip()
            address2 = fp.readline().strip()
            country = fp.readline().strip()
            print("\"{}\",\"{}\",\"{}\",\"{}\",\"{}\"".format(
                oui, company_name, address1, address2, country))

remove(tmpfile)


if __name__ == '__main__':
    print('---------')
    if len(sys.argv) == 1:
        mac = [input("Enter MAC Address: ")]
    else:
        mac = [item for item in sys.argv[1::]]
    for addr in mac:
        get_oui_info(addr)

#     remove_chars = '.-:ghijklmnopqrstuvwxyz!@#$%^&*()_+={};,<>/?"\''
#     mac = mac.lower()
#     for char in remove_chars:
#         mac = mac.replace(char, '')
#     print(f'MAC Address: {mac}')
#     if len(mac) != 12:
#         print('Unformatted Input is not 12 characters')
#     else:
#         try:
#             oui = netaddr.EUI(mac).oui
#             print(
#                 f'''OUI: {oui.registration().oui}
# Organization: {oui.registration().org}
# Address: {", ".join(oui.registration().address)}
# ---------''')
#         except:
#             print('OUI Not Registered or Invalid\n---------')
