from pexpect import pxssh
import os

class Client :
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        # self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print("[-] Error Connecting")

clients = []

def start():
    for file in os.listdir("./clients"):
        client_file = open("./clients/" + file, 'r')
        lines = client_file.readlines()
        host = lines[0].strip('\r').strip('\n')
        user = lines[1].strip('\r').strip('\n')
        password = lines[2].strip('\r').strip('\n')

        client = Client(host, user, password)
        clients.append(client)


if __name__ == '__main__':
    start()
