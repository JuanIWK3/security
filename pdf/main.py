import optparse
from pypdf import PdfReader
import os


def imprimir_meta(pasta, nome):
    pdfs = []
    for file in os.listdir(pasta):
        if file.split('.')[1] == 'pdf':
            reader = PdfReader(pasta + '/' + file)
            if reader.metadata == None:
                continue
            if reader.metadata.author == None:
                continue
            print(reader.metadata.author)
            if reader.metadata.author == nome:
                pdfs.append(file)
    if len(pdfs) == 0:
        print('Nenhum pdf encontrado para o autor: ' + nome)
    else:
        print('Pdfs escritos por ' + nome)
        for pdf in pdfs:
            print("\t" + pdf)


def main():
    analisador = optparse.OptionParser("use %prog " +
                                       "-F <pasta com arquivos pdf> -N <nome do autor>")
    analisador.add_option('-F', dest='pasta',
                          type='string', help='especifique o arquivo PDF')
    analisador.add_option('-N', dest='nome',
                          type='string', help='especifique o nome do autor')

    (opcoes, args) = analisador.parse_args()
    pasta = opcoes.pasta
    nome = opcoes.nome

    if pasta == None or nome == None:
        print(analisador.usage)
        exit(0)
    else:
        imprimir_meta(pasta, nome)


if __name__ == '__main__':
    main()
