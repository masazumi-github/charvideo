import os
import sys
import cv2
import time
import argparse
from PIL import Image

CHAR_LIST = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")

# 返回像素对应的字符
def getChar(r, g, b, alpha = 256):
    if alpha == 0:
        return ' '
    length = len(CHAR_LIST)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)
    unit = (256.0 + 1)/length
    return CHAR_LIST[ int(gray/unit) ]

def showCharImg(image, width, height):
    image = image.resize((width, height), Image.NEAREST)

    txt = ''
    for i in range(height):
        for j in range(width):
            txt += getChar( *image.getpixel((j,i)) )
        txt += '\n'
    print(txt)

def GetVideoFrame(videoURI, width, height, gap):
    videocapture = cv2.VideoCapture(videoURI)
    #frameCount = videocapture.get(7)
    #frameRate =  videocapture.get(5)
    #duration = frameCount / frameRate
    #delay = (duration / frameCount) / 2
    #具体的延时与机器速度有关，不应该通过这个计算来确定
    delay = 0.012
    if videocapture.isOpened() is not True:
        exit('Fail to load video')

    os.system("mode con cols=%d" % width)
    
    _i = 0 
    success, frame = videocapture.read()
    while success: 
        if (_i % gap == 0):
            image = Image.fromarray(frame)
            showCharImg(image, width, height)
            time.sleep(delay)
        _i += 1
        success, frame = videocapture.read()
    videocapture.release()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('--width', type = int, default = 180)
    parser.add_argument('--height', type = int, default = 65)
    parser.add_argument('--gap', type = int, default = 1)

    args = parser.parse_args()
    videoURI = args.file
    gap = args.gap
    width = args.width
    height = args.height
    
    GetVideoFrame(videoURI, width, height, gap)
   
