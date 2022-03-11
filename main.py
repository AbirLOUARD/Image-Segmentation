import cv2
import utils
import os
import edge_segmentation as er
import felzenswalb_segmentation as fs
import slic
import boundingBox

def main():
    args = utils.parserInit()
    pathFolder = args["pathFolder"]
    listImagesToCompare = utils.loadImages(pathFolder)

    image = cv2.imread(pathFolder + "/" +listImagesToCompare[0])
    #image = cv2.resize(image, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    backgroundPixel = utils.foundBackground(image)
    print(backgroundPixel)
    utils.colorOthersPixels(image, backgroundPixel)
    cv2.waitKey(0)
    cv2.destroyAllWindows

    """
    #fs.segmentation(pathFolder + "/" +listImagesToCompare[0], 15)
    image = cv2.imread(pathFolder + "/" +listImagesToCompare[0])
    imageSlicColor = slic.segmentation(pathFolder + "/" +listImagesToCompare[0], 50)
    boundingBox.findAndDrawBB(imageSlicColor, image)
    cv2.imshow("bb", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows
    """
    """
    for image in listImagesToCompare:
        #er.segmentation(pathFolder + "/" +image)
        fs.segmentation(pathFolder + "/" +image, 100)
        cv2.waitKey(0)
        cv2.destroyAllWindows
    """


if __name__ == "__main__":
    main()