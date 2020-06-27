# from skimage.color import rgb2gray

# import matplotlib.pyplot as plt
# %matplotlib inline
# from scipy import ndimage
import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'input image path')
args = ap.parse_args()

image = cv2.imread(args.image)
print(image.shape)
cv2.imshow("Original Image",image)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Image",gray)
print(gray.shape)


#Finding mean of each pixel in grayscale
mean =np.mean(gray)
print(mean)

#Setting threshold
threshold=mean

#Setting mask with mean as threshold
mask=(gray>threshold)*1

gray[gray<mean]=0
cv2.imshow("Grayscale Image After Mask",gray)
nc=image.shape[2]
image2=image
for i in range(0,nc):
	image2[:,:,i]=mask*image[:,:,i]
cv2.imshow("Original Image After Mask",image2)



cv2.waitKey(0)
cv2.destroyAllWindows()