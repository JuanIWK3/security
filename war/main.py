import optparse
from time import sleep
from bs4 import BeautifulSoup
import urllib3
import os
from PIL.ExifTags import TAGS
from shutil import copy2
import exif
import PIL


def findImages(url):
    print('[+] Finding images on ' + url)
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    bs = BeautifulSoup(response.data, 'html.parser')
    imgTags = bs.findAll('img')
    return imgTags


def downloadImage(imgTag):
    try:
        imgSrc = imgTag['src']
        http = urllib3.PoolManager()
        response = http.request('GET', imgSrc)
        fileName = imgSrc.split('/')[-1]
        fileName = fileName.split('?')[0]

        with open("images/" + fileName, 'wb') as f:
            f.write(response.data)
    except:
        pass

# If the image contains GPS info, save it on images_gps folder


def copyImage(fileName):
    destDir = 'images_gps'
    if not os.path.exists(destDir):
        os.makedirs(destDir)
    copy2(fileName, destDir)


def exifTest(fileName):
    with open(fileName, 'rb') as f:
        img = exif.Image(f)
        if img.has_exif:
            print('[*] ' + fileName + ' contains GPS MetaData')
            print(img.list_all())
            copyImage(fileName)
        else:
            # print('[-] ' + fileName + ' does not contain GPS MetaData')
            pass


def start():
    args = optparse.OptionParser('use "-u <url>"')
    args.add_option('-u', dest='url', type='string', help='specify url')
    (options, args) = args.parse_args()
    url = options.url

    destDir = 'images'

    if not os.path.exists(destDir):
        os.makedirs(destDir)

    if url is None:
        print(args.usage)
        exit(0)
    else:
        imgTags = findImages(url)

        print('[+] Downloading images to ' + destDir)
        for imgTag in imgTags:
            downloadImage(imgTag)

        print('[+] Testing images for GPS Exif Data')
        for fileName in os.listdir(destDir):
            exifTest(destDir + '/' + fileName)

        # Delete images that do not contain GPS info
        for fileName in os.listdir(destDir):
            os.remove('images/' + fileName)


if __name__ == '__main__':
    start()
