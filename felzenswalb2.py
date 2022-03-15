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



def segmentation(pathImage, threshold):
    image = cv2.imread(pathImage)
    image_felzenswalb = seg.felzenszwalb(image)
    
    #RAG - Region Adjacency Graph
    rag = graph.rag_mean_color(image, image_felzenswalb + 1)
    # Regionprops ignores zero, but we want to include it, so add one
    regions = measure.regionprops(image_felzenswalb + 1)  

    # Pass centroid data into the graph
    for region in regions:
        rag.nodes[region['label']]['centroid'] = region['centroid']

    edges_drawn_all = display_edges(image_felzenswalb, rag, np.inf)
    final_labels = graph.cut_threshold(image_felzenswalb + 1, rag, threshold)
    final_label_rgb = color.label2rgb(final_labels, image, kind='avg')

    cv2.imshow("test", final_label_rgb)
    print(np.unique(final_labels).size)


def display_edges(image, g, threshold):
    image = image.copy()
    for edge in g.edges():
        n1, n2 = edge
 
        r1, c1 = map(int, g.nodes[n1]['centroid'])
        r2, c2 = map(int, g.nodes[n2]['centroid'])
 
        line  = draw.line(r1, c1, r2, c2)
        circle = draw.circle_perimeter(r1,c1,2)
        
        """"
        if g[n1][n2]['weight'] < threshold :
            image[line] = 0,255,0
        image[circle] = 255,255,0
        
        image = image.astype(np.uint8)
        cv2.imshow("edges_drawn_all", image)
        """
 
    return image