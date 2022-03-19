from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np

from skimage.data import astronaut
from skimage.segmentation import quickshift
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float


def segmentation(img):
    segments_quick = quickshift(img, kernel_size=25, max_dist=50, ratio=0.5)

    print("quickshift's number of segments: %d" % len(np.unique(segments_quick)))

    listGrains = []
    moy_B = 0
    moy_G = 0
    moy_R = 0
    cptMoyB = 0
    cptMoyG = 0
    cptMoyR = 0
    for i in segments_quick:
        print(i)
        cptModulo = 0
        for j in i:
            if (cptModulo == 0):
                moy_B += i[j]
                cptModulo += 1
                cptMoyB += 1
            elif (cptModulo == 1):
                moy_G += i[j]
                cptModulo += 1
                cptMoyG += 1
            elif (cptModulo == 2):
                moy_R += i[j]
                cptModulo = 0
                cptMoyR += 1
        moy_B /= cptMoyB
        moy_G /= cptMoyG
        moy_R /= cptMoyR
        listGrains.append((moy_B, moy_G, moy_R))
        moy_B = 0
        moy_G = 0
        moy_R = 0
        cptMoyB = 0
        cptMoyG = 0
        cptMoyR = 0

    for grain1 in listGrains:
        for grain2 in listGrains:
            if (grain1[0] == grain2[0] and grain1[1] == grain2[1] and grain1[2] == grain2[2]):
                listGrains.remove(grain2)
    print(len(listGrains))

    stringGrains = "Grains \n"
    for g in listGrains:
        stringGrains += "Moyenne de B : " + str(round(g[0])) + ' | ' +  "Moyenne de G : " + str(round(g[1])) + ' | ' + "Moyenne de G : " + str(round(g[2])) + '\n'


    plt.subplot(121)
    plt.imshow(img)
    plt.title("Originale")
    plt.subplot(122)
    plt.text(0.5, 0.5, stringGrains, horizontalalignment='center', verticalalignment='center', size = 5)
    plt.show()
