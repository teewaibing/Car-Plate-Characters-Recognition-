import cv2
import numpy as np
import os
from difflib import SequenceMatcher

import DetectChars
import DetectPlates
import PossiblePlate
import collections


SCALAR_BLACK = (0.0, 0.0, 0.0)

SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = True

def similar(a, b):
    return round(SequenceMatcher(None, a, b).ratio(), 2)

def main(fileName):

    imgOriginalScene  = cv2.imread(fileName)
    if imgOriginalScene is None:
        print("\nerror: image not read from file \n\n")
        os.system("pause")
        return

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    #cv2.imshow("imgOriginalScene", imgOriginalScene)

    if len(listOfPossiblePlates) == 0:
        print("\nno license plates were detected\n")
    else:

        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

        licPlate = listOfPossiblePlates[0]

        if len(licPlate.strChars) == 0:
             print("\nno characters were detected\n\n")
             return 'none'

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

        #cv2.imshow("imgOriginalScene", imgOriginalScene)
        #cv2.imwrite("imgOriginalScene.png", imgOriginalScene)
        cv2.waitKey(0)
        return licPlate.strChars

    return 'none'

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)
    cv2.line(imgOriginalScene, p2fRectPoints[0].astype(int), p2fRectPoints[1].astype(int), SCALAR_RED, 2)         # draw 4 red lines
    cv2.line(imgOriginalScene, p2fRectPoints[1].astype(int), p2fRectPoints[2].astype(int), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, p2fRectPoints[2].astype(int), p2fRectPoints[3].astype(int), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, p2fRectPoints[3].astype(int), p2fRectPoints[0].astype(int), SCALAR_RED, 2)
# end function

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0
    intFontThickness = int(round(fltFontScale * 1.5))

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)


    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)

    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))

    textSizeWidth, textSizeHeight = textSize

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))

    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)


if __name__ == "__main__":

    size = len(os.listdir("./img_rain/"))# if want detetct original images change to ./img_ori/

    accuracy = []
    count = 0
    charData = {}
    char1Data = {}

    for fileName in os.listdir("./img_rain/"):   # if want detetct original images change to ./img_ori/
        print(fileName)
        recognizeText = main("./img_rain/" + fileName)# if want detetct original images change to ./img_ori/
        print(type(recognizeText))
        acutalText = os.path.splitext(fileName)[0]
        print(recognizeText)
        print(acutalText)
        accuracy.append(similar(acutalText, recognizeText))
        count = count + 1
        print(str(count) + "/" + str(size) + " => " + "(Recognized Plate Value = " + recognizeText + ")" + " (Actual Plate value = " + acutalText + ")") #Accuracy = " + str(similar(acutalText, recognizeText) * 100) + "%

        chars = list(recognizeText)


        for i in range(len(chars)):
            if charData.__contains__(chars[i]):
                charData[chars[i]] = charData[chars[i]] + i
            else:
                charData[chars[i]] = 1

        chars1 = list(acutalText)
        for i in range(len(chars1)):
            if char1Data.__contains__(chars1[i]):
                char1Data[chars1[i]] = char1Data[chars1[i]] + i
            else:
                char1Data[chars1[i]] = 1


    print("\n Accuracy of the algorithm is " + str(sum(accuracy) / len(accuracy) * 100)+"\n")
    print ("character in recognized text")
    print(collections.OrderedDict(charData))
    print ("characters in actual text")
    print(collections.OrderedDict(char1Data))
    print(sum(accuracy))
    print(len(accuracy))