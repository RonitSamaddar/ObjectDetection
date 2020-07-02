# from skimage.color import rgb2gray

# import matplotlib.pyplot as plt
# %matplotlib inline
# from scipy import ndimage
import cv2
import argparse
import numpy as np
from sklearn.cluster import KMeans

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'input image path')
ap.add_argument('-c', '--num_clusters', required=True,
                help = 'Number of clusters')
args = ap.parse_args()

image = cv2.imread(args.image)
print(image.shape)
image=image/255
cv2.imshow("Original Image",image)
"""
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image",gray)
print(gray.shape)

"""
pic_n = image.reshape(image.shape[0]*image.shape[1],image.shape[2])
print(pic_n.shape)

kmeans = KMeans(n_clusters=int(args.num_clusters), random_state=0).fit(pic_n)
pic2show = kmeans.cluster_centers_[kmeans.labels_]
cluster_pic = pic2show.reshape(image.shape[0], image.shape[1], image.shape[2])
cv2.imshow("Clustereing segmented image",cluster_pic)





cv2.waitKey(0)
cv2.destroyAllWindows()