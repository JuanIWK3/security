from email import encoders
from email.mime.base import MIMEBase
from zipfile import ZipFile
import optparse
from threading import Thread
import ssl
import smtplib
from dotenv import load_dotenv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import shutil

load_dotenv()


# send email to myself
def send_email(pwd: str) -> None:
    sender = os.getenv('EMAIL')
    receiver = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')

    msg = MIMEMultipart()
    body = MIMEText('Password found: ' + pwd)
    msg['Subject'] = 'Password found'
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(body)

    dir_name = 'files'
    output_filename = dir_name
    shutil.make_archive(output_filename, 'zip', dir_name)

    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(output_filename + ".zip", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="files.zip"')
    msg.attach(part)

    context = ssl.create_default_context()
     
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, msg.as_string())
        print('Email sent')


def extract_file(file: ZipFile, password: str) -> None:
    try:
        file.extractall(path="files", pwd=password.encode())
        print('[+] Password found: ' + password + '\n')
        send_email(password)
    except:
        pass


def start():
    analyzer = optparse.OptionParser("use %prog " + "-f <arquivozip> -d <dicionario>")
    analyzer.add_option('-f', dest='name_zip', type='string', help='especifique o arquivo zip')
    analyzer.add_option('-d', dest='name_dic', type='string', help='especifique o arquivo dicionario')
    (options, args) = analyzer.parse_args()
    if (options.name_zip is None) | (options.name_dic is None):
        print(analyzer.usage)
        exit(0)
    else:
        name_zip = options.name_zip
        name_dic = options.name_dic

    zip_file = ZipFile(name_zip)
    dic_file = open(name_dic)

    for line in dic_file.readlines():
        password = line.strip('\n')
        t = Thread(target=extract_file, args=(zip_file, password))
        t.start()


if __name__ == '__main__':
    start()
