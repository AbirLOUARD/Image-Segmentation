import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import cv2


from skimage.feature import peak_local_max
from skimage.segmentation import watershed

def segmentation(imgOri):
    imageGray = cv2.cvtColor(imgOri, cv2.COLOR_BGR2GRAY)

    distance = ndi.distance_transform_edt(imageGray)
    local_maxi = peak_local_max(distance, indices=False, footprint=np.ones((3, 3)), labels=imageGray)
    markers = ndi.label(local_maxi)[0]
    labels = watershed(-distance, markers, mask=imageGray)

    fig, axes = plt.subplots(ncols=3, figsize=(8, 2.7), sharex=True, sharey=True, subplot_kw={'adjustable': 'box'})
    ax0, ax1, ax2 = axes

    ax0.imshow(imageGray, cmap=plt.cm.gray, interpolation='nearest')
    ax0.set_title('Image NG')
    ax1.imshow(-distance, cmap=plt.cm.gray, interpolation='nearest')
    ax1.set_title('Distances')
    ax2.imshow(labels, cmap=plt.cm.Spectral, interpolation='nearest')
    ax2.set_title('Segmentation')

    for ax in axes:
        ax.axis('off')

    fig.tight_layout()
    plt.show()