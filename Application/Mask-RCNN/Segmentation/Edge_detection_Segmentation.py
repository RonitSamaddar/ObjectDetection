# from skimage.color import rgb2gray

# import matplotlib.pyplot as plt
# %matplotlib inline
# from scipy import ndimage
import cv2
import argparse
import numpy as np
from scipy import ndimage

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True,
                help = 'input image path')
args = ap.parse_args()

image = cv2.imread(args.image)
print(image.shape)
cv2.imshow("Original Image",image)
#gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#cv2.imshow("Grayscale Image",gray)
#print(gray.shape)

# defining the edge detection filters
sobel_horizontal = np.array([np.array([1, 2, 1]), np.array([0, 0, 0]), np.array([-1, -2, -1])])
sobel_vertical = np.array([np.array([-1, 0, 1]), np.array([-2, 0, 2]), np.array([-1, 0, 1])])
kernel_laplace = np.array([np.array([1, 1, 1]), np.array([1, -8, 1]), np.array([1, 1, 1])])

#Convolving the above filters
out_h=np.copy(image)
out_v=np.copy(image)
out_l=np.copy(image)
for i in range(0,3):
	out_h[:,:,i] = ndimage.convolve(image[:,:,i], sobel_horizontal, mode='reflect')
	out_v[:,:,i] = ndimage.convolve(image[:,:,i], sobel_vertical, mode='reflect')
	out_l[:,:,i] = ndimage.convolve(image[:,:,i], kernel_laplace, mode='reflect')

cv2.imshow("Horizontal edges",out_h)
cv2.imshow("Vertical edges",out_v)
cv2.imshow("Both edges",out_l)






cv2.waitKey(0)
cv2.destroyAllWindows()