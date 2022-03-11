import numpy as np
import matplotlib.pyplot as plt
import skimage.data as data
import skimage.segmentation as seg
import cv2
import skimage.future.graph as graph
import skimage.measure as measure


from skimage import filters
from skimage import draw
from skimage import color
from skimage import exposure

def segmentation(pathImage, n_segments):
    image = cv2.imread(pathImage)
    imageSlic = seg.slic(image, n_segments)
    imageSlicColor = color.label2rgb(imageSlic, image, kind='avg')
    return imageSlicColor