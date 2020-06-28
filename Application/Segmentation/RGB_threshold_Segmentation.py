# from skimage.color import rgb2gray

# import matplotlib.pyplot as plt
# %matplotlib inline
# from scipy import ndimage
import cv2
import argparse
import numpy as np
import sys

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'input image path')
ap.add_argument('-t', '--threshold', required=True,
                help = 'threshold value(for every channel only pixels more than threshold will be displayed')
args = ap.parse_args()

image = cv2.imread(args.image)
print(image.shape)
cv2.imshow("Original Image",image)

color=['blue','green','red']

for i in range(0,3):
	#cv2.imshow(""+color[i]+" component",image[:,:,i])

	comp=image[:,:,i]
	#cv2.imshow(color[i]+" component",comp)

	#Finding mean of each pixel in grayscale
	mean =np.mean(comp)
	print(mean)

	#Setting threshold
	threshold=int(args.threshold)

	#Setting mask with mean as threshold
	mask=(comp>threshold)*1
	mask2=(mask*255).astype(np.uint8)
	#cv2.imshow("Mask for "+color[i]+" component",mask2)

	image2=np.copy(image)
	for j in range(0,3):
		image2[:,:,j]=image[:,:,j]*mask

	cv2.imshow("Image with "+color[i]+" mask",image2)

	continue


	#cv2.imshow("Original Image After "+color[i]+" mask",image2)
	break

	


cv2.waitKey(0)
cv2.destroyAllWindows()

