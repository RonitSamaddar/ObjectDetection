import cv2

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
	(h,w,c)=frame.shape
	for i in range(0,w):
		frame[h//2,i,1]=255
		frame[h//2+1,i,1]=255
		frame[h//2+2,i,1]=255
	cv2.imshow("preview", frame)
	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key == 27: # exit on ESC
		break
cv2.destroyWindow("preview")