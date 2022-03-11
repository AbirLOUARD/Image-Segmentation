import argparse
import os
import cv2

def parserInit():
    parser = argparse.ArgumentParser()
    parser.add_argument("pathFolder", help = "path to the images folder")
    args = vars(parser.parse_args())
    return args

def loadImages(pathFolder):
    folder = os.fsencode(pathFolder)
    listImagesToCompare = []
    for file in os.listdir(folder):
        listImagesToCompare.append(file.decode("utf-8"))
    return listImagesToCompare

def foundBackground(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x1 = gray.shape[0]
    y1 = gray.shape[1]
    listPixel = []

    for i in range(x1) :
        for j in range(y1) :
            if (gray[i, j] not in listPixel):
                listPixel.append(gray[i, j])

    cptCurrentPixel = 0
    cptMaxPixel = 0
    backgroundPixel = 0
    for pixel in listPixel:
        for i in range(x1) :
            for j in range(y1) :
                if (pixel == gray[i, j]):
                    cptCurrentPixel += 1
        if (cptCurrentPixel > cptMaxPixel):
            cptMaxPixel = cptCurrentPixel
            backgroundPixel = pixel
            

    return backgroundPixel

def colorOthersPixels(image, pixel):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    x1 = gray.shape[0]
    y1 = gray.shape[1]
    for i in range(x1) :
        for j in range(y1) :
            if (pixel != gray[i, j]):
                image[i, j] = [255, 0, 255]
    cv2.imshow("diff", image)
    