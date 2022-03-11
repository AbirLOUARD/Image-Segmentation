
import numpy as np
import matplotlib.pyplot as plt
import cv2

from skimage import data
from skimage.feature import canny
from scipy import ndimage as ndi
from skimage import morphology

def segmentation(pathImage):
    image = cv2.imread(pathImage)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    hist = np.histogram(image, bins=np.arange(0, 256))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
    ax1.imshow(image, cmap=plt.cm.gray, interpolation='nearest')
    ax1.axis('off')
    ax2.plot(hist[1][:-1], hist[0], lw=2)
    ax2.set_title('histogram of grey values')

    # Threshold
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 3), sharex=True, sharey=True)
    ax1.imshow(image > 100, cmap=plt.cm.gray, interpolation='nearest')
    ax1.set_title('coins > 100')
    ax1.axis('off')
    ax1.set_adjustable('box')
    ax2.imshow(image > 150, cmap=plt.cm.gray, interpolation='nearest')
    ax2.set_title('coins > 150')
    ax2.axis('off')
    ax2.set_adjustable('box')
    margins = dict(hspace=0.01, wspace=0.01, top=1, bottom=0, left=0, right=1)
    fig.subplots_adjust(**margins)


    # Edge-based segmentation
    edges = canny(image/255.)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(edges, cmap=plt.cm.gray, interpolation='nearest')
    ax.axis('off')
    ax.set_title('Canny detector')

    # Traitements
    fill_coins = ndi.binary_fill_holes(edges)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(fill_coins, cmap=plt.cm.gray, interpolation='nearest')
    ax.axis('off')
    ax.set_title('Filling the holes')

    coins_cleaned = morphology.remove_small_objects(fill_coins, 21)

    fig, ax = plt.subplots(figsize=(4, 3))
    ax.imshow(coins_cleaned, cmap=plt.cm.gray, interpolation='nearest')
    ax.axis('off')
    ax.set_title('Removing small objects')

    plt.show()
