import cv2
import matplotlib.pyplot as plt

def detectShapes(image, imageToReturn):
    listPixelsContours = []
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    i = 0
    for contour in contours:
        #premier == toute l'image
        if i == 0:
            i = 1
            continue

        perimeter = cv2.arcLength(contour,True)
        if (perimeter > 50):
            area = cv2.contourArea(contour)
            print(area)        
            approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
            cv2.drawContours(imageToReturn, [contour], 0, (0, 255, 0), 2)
            
            M = cv2.moments(contour)
            if M['m00'] != 0.0:
                x = int(M['m10']/M['m00'])
                y = int(M['m01']/M['m00'])
                center = (x,y)
                listPixelsContours.append(center)
    
    return imageToReturn, listPixelsContours


# Colorie en rose les pixels des grains
def threshold(image, listPixels):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageWithDifferences = image.copy()
    x = gray.shape[0]
    y = gray.shape[1]
    listValues = []
    for pixel in listPixels:
        listValues.append(gray[pixel])
    listValues.sort()

    for value in listValues:
        x = gray.shape[0]
        y = gray.shape[1]
        for i in range(x):
            for j in range(y):
                if (gray[i,j] > value - 10 and gray[i,j] < value + 10 and gray[i,j] > 100):
                    imageWithDifferences[i,j] = (255, 0, 255)
    
    return imageWithDifferences
    

def calculateValueGrains(originalImage, imageWithDifferences):
    moy_B = 0
    moy_G = 0
    moy_R = 0
    cpt = 0
    x = originalImage.shape[0]
    y = originalImage.shape[1]
    for i in range(x):
        for j in range(y):
            if (imageWithDifferences[i,j][0] == 255 and imageWithDifferences[i,j][1] == 0 and imageWithDifferences[i,j][2] == 255):
                moy_B += originalImage[i,j][0]
                moy_G += originalImage[i,j][1]
                moy_R += originalImage[i,j][2]
                cpt += 1
    moy_B /= cpt
    moy_G /= cpt
    moy_R /= cpt
    return originalImage, imageWithDifferences, moy_B, moy_G, moy_R


def displayAll(image1, image2, moy_B, moy_G, moy_R) :
    b1, g1, r1 = cv2.split(image1)
    b2, g2, r2 = cv2.split(image2)
    image1PLT = cv2.merge([r1, g1, b1])
    image2PLT = cv2.merge([r2, g2, b2])
    
    plt.subplot(121)
    plt.imshow(image1PLT)
    plt.title("Originale")
    plt.subplot(122)
    plt.text(0.5, 0.5, "Moyenne de B : " + str(round(moy_B)) + '\n' +  "Moyenne de G : " + str(round(moy_G)) + '\n' + "Moyenne de G : " + str(round(moy_R)), horizontalalignment='center', verticalalignment='center')
    
    plt.show()



def segmentation(imageEq, image):
    imageSeg, listPixels = detectShapes(imageEq, image)
    imageSeg = threshold(imageSeg, listPixels)
    originalImage, imageWithDifferences, moy_B, moy_G, moy_R = calculateValueGrains(image, imageSeg)
    displayAll(originalImage, imageWithDifferences, moy_B, moy_G, moy_R)

    

