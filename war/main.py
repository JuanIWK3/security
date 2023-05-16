from bs4 import BeautifulSoup
from PIL.ExifTags import TAGS
from PIL import Image
from shutil import copy2
import argparse
import requests
import os


def getPage(url):
    try:
        response = requests.get(url).content
        return response
    except:
        print('[-] Error retrieving page. Check URL')
        pass


def findImages(url): return [
    img for img in BeautifulSoup(getPage(url), 'html.parser').find_all('img')
]


def getImagesLinks(url):
    imgTags = findImages(url)
    imgLinks = []
    for imgTag in imgTags:
        if imgTag.has_attr('src'):
            imgUrl = imgTag['src']
            imgLinks.append(imgUrl)
    return imgLinks


def fixImageUrl(url):
    url = url.split('/')[-1].split('?')[0]
    if '.' not in url:
        url += '.jpg'
    return url


def downloadImages(url, destDir):
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    imgLinks = getImagesLinks(url)

    for imgLink in imgLinks:
        try:
            imgData = requests.get(imgLink).content
            imgName = fixImageUrl(imgLink)
            imgPath = destDir + '/' + imgName
            with open(imgPath, 'wb') as imgFile:
                imgFile.write(imgData)
            print('[+] Dowloaded ' + imgName)
        except:
            pass


def copyImage(fileName, destDir):
    if not os.path.exists(destDir):
        os.makedirs(destDir)

    copy2(fileName, destDir)


def exifTest(fileName):
    print('[*] Testing ' + fileName)
    try:
        exifData = {}
        imgFile = Image.open(fileName)
        info = imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded = TAGS.get(tag, tag)
                exifData[decoded] = value

            exifGPS = exifData['GPSInfo']
            if exifGPS:
                print('\t[+] ' + fileName + ' contains GPS MetaData')
                copyImage(fileName, 'images_gps')
            else:
                pass
                # print('[-] ' + fileName + ' does not contain GPS MetaData')
        else:
            pass
            # print('[-] ' + fileName + ' does not contain MetaData')
    except:
        pass


if __name__ == '__main__':
    args = argparse.ArgumentParser('use "-u <url>"')
    args.add_argument('-u', '--url', required=True)
    args = args.parse_args()
    url = args.url

    destDir = 'images'

    print('\n[+] Dowloading images from ' + url)
    downloadImages(url, destDir)

    print('\n[*] Testing images for GPS Exif Data')
    for fileName in os.listdir(destDir):
        exifTest(destDir + '/' + fileName)

    # Delete images that do not contain GPS info
    for fileName in os.listdir(destDir):
        os.remove('images/' + fileName)
