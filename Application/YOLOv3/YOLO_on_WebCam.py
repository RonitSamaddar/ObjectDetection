import cv2
import argparse
import numpy as np
import csv

CLASS_PATH="yolov3.txt"
WEIGHTS_PATH="yolov3.weights"
CONFIG_PATH="yolov3.cfg"
DIST_PATH="yolov3.csv"



def get_output_layers(net):
    #Get the names of the output layers into the architecture
    layer_names = net.getLayerNames()    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_bounding_box(img, classes,colors,class_id, confidence, x, y, x_plus_w, y_plus_h,dist):
	# function to draw bounding box on the detected object with class name

    label = str(classes[class_id])
    color = colors[class_id]

    #Extra code for marking midpoint
    x_mid=(x+x_plus_w)//2
    y_mid=(y+y_plus_h)//2
    cv2.rectangle(img,(x_mid-1,y_mid-1),(x_mid+1,y_mid+1),color,2)
    cv2.rectangle(img,(x_mid-2,y_mid-2),(x_mid+2,y_mid+2),color,2)

    
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label+". Distance = "+str(dist), (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def object_detect(image,classes,colors,object_dist,class_path,weights_path,config_path):
	Width = image.shape[1]
	Height = image.shape[0]
	scale = 0.00392
	   
	# Reading pre-trained model and configuration
	net = cv2.dnn.readNet(weights_path, config_path)

	# Creating and setting input blob from image
	blob = cv2.dnn.blobFromImage(image, scale, (416,416), (0,0,0), True, crop=False)
	net.setInput(blob)

	# Running inference through the network and gather predictions from output layers
	outs = net.forward(get_output_layers(net))

	# Initialization
	class_ids = []
	confidences = []
	boxes = []
	conf_threshold = 0.5
	nms_threshold = 0.4

	# For each detetion from each output layer we get the confidence, class id, bounding box params
	# and ignore weak detections (confidence < conf_threshold)

	for out in outs:
	    for detection in out:
	        scores = detection[5:]
	        class_id = np.argmax(scores)
	        confidence = scores[class_id]
	        if confidence > conf_threshold:
	            center_x = int(detection[0] * Width)
	            center_y = int(detection[1] * Height)
	            w = int(detection[2] * Width)
	            h = int(detection[3] * Height)
	            x = center_x - w / 2
	            y = center_y - h / 2
	            class_ids.append(class_id)
	            confidences.append(float(confidence))
	            boxes.append([x, y, w, h])

	# apply non-max suppression
	indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

	# go through the detections remaining
	# after nms and draw bounding box
	for i in indices:
	    i = i[0]
	    box = boxes[i]
	    x = box[0]
	    y = box[1]
	    w = box[2]
	    h = box[3]
	    class_type=classes[class_ids[i]]
	    if(object_dist[class_type]==[-1,-1,-1]):
	    	dist=float(input("Enter dist of "+str(class_type)+" (-1 if wrong prediction)  :  "))
	    	if(dist>0):
	    		object_dist[class_type]=[h,w,dist]
	    else:
	    	lambda_h=h/object_dist[class_type][0]
	    	lambda_w=w/object_dist[class_type][1]
	    	lambda_a=((h*w)/(object_dist[class_type][0]*object_dist[class_type][1]))**0.5
	    	lambda_r=min(lambda_h,lambda_w,lambda_a)
	    	dist=object_dist[class_type][2]/lambda_r


	    draw_bounding_box(image, classes,colors,class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h),dist)
	return image




cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

# Reading classes from txt file
with open(CLASS_PATH, 'r') as f:
	classes=[]
	for line in f.readlines():
		classes.append(line.strip())
# Generating different colors for different classes 
colors = np.random.uniform(0, 255, size=(len(classes), 3))

f=open(DIST_PATH,'r')
fr=csv.reader(f)

object_dist={}
index=0
for line in fr:
	if(index==0):
		index+=1
		continue
	object_dist[line[0]]=[]
	for i in range(1,len(line)):
		object_dist[line[0]].append(float(line[i]))
#print(object_dist)
f.close()



if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
	(h,w,c)=frame.shape
	image=object_detect(frame,classes,colors,object_dist,CLASS_PATH,WEIGHTS_PATH,CONFIG_PATH)
	cv2.imshow("preview", image)
	rval, frame = vc.read()
	key = cv2.waitKey(1)
	if key == 27: # exit on ESC
		break
cv2.destroyWindow("preview")


f=open(DIST_PATH,'w')
fr=csv.writer(f)
fr.writerow(["CLASS","INITIAL_HEIGHT","INITIAL_WEIGHT","DISTANCE"])
for x in object_dist.keys():
	lst=[]
	lst.append(x)
	lst.extend(object_dist[x])
	fr.writerow(lst)
f.close()




