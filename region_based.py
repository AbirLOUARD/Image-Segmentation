import numpy as np
import matplotlib.pyplot as plt
import cv2

from skimage.feature import canny
from scipy import ndimage as ndi
from skimage import morphology
from skimage.filters import sobel
from skimage import data
from skimage.color import label2rgb

from skimage.segmentation import watershed

def segmentation(imgOri):
    imageGray = cv2.cvtColor(imgOri, cv2.COLOR_BGR2GRAY)
    
    margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)

    elevation_map = sobel(imageGray)

    markers = np.zeros_like(imageGray)
    markers[imageGray < 30] = 1
    markers[imageGray > 150] = 2

    segmentation = watershed(elevation_map, markers)

    segmentation = ndi.binary_fill_holes(segmentation - 1)
    labeled, _ = ndi.label(segmentation)
    image_label_overlay = label2rgb(labeled, image=imageGray)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3), sharex=True, sharey=True)
    ax1.imshow(imageGray, cmap=plt.cm.gray, interpolation='nearest')
    ax1.contour(segmentation, [0.5], linewidths=1.2, colors='y')
    ax1.axis('off')
    ax1.set_adjustable('box')
    ax2.imshow(image_label_overlay, interpolation='nearest')
    ax2.axis('off')
    ax2.set_adjustable('box')

    fig.subplots_adjust(**margins)

    plt.show()