import cv2
import argparse
import numpy as np



def get_output_layers(net):
    #Get the names of the output layers into the architecture
    layer_names = net.getLayerNames()    
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    return output_layers


def draw_bounding_box(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
	# function to draw bounding box on the detected object with class name
    label = str(classes[class_id])
    color = colors[class_id]
    cv2.rectangle(img, (x,y), (x_plus_w,y_plus_h), color, 2)
    cv2.putText(img, label, (x-10,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)




# Handling command line arguments
ap = argparse.ArgumentParser()
ap.add_argument('-w', '--weights', required=True,
                help = 'pretrained yolo weights path')
ap.add_argument('-co', '--config', required=True,
                help = 'config file path')
ap.add_argument('-i', '--image', required=True,
                help = 'input image path')
ap.add_argument('-cl', '--classes', required=True,
                help = 'class names txt file path')
args = ap.parse_args()


# Handling the input image

# Reading Input Image
image = cv2.imread(args.image)
Width = image.shape[1]
Height = image.shape[0]
scale = 0.00392

# Reading classes from txt file
classes = None
with open(args.classes, 'r') as f:
	classes=[]
	for line in f.readlines():
		classes.append(line.strip())
   

# Generating different colors for different classes 
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# Reading pre-trained model and configuration
net = cv2.dnn.readNet(args.weights, args.config)

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
    
    draw_bounding_box(image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))

# display output image    
cv2.imshow("object detection", image)

# wait until any key is pressed
cv2.waitKey()
    
 # save output image to disk
cv2.imwrite("object-detection.jpg", image)

# release resources
cv2.destroyAllWindows()



