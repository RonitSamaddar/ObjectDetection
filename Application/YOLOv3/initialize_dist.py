import csv

CLASS_PATH="yolov3.txt"
DIST_PATH="yolov3.csv"

# Reading classes from txt file
with open(CLASS_PATH, 'r') as f:
	classes=[]
	for line in f.readlines():
		classes.append(line.strip())


f=open(DIST_PATH,'w')
fr=csv.writer(f)
fr.writerow(["CLASS","INITIAL_HEIGHT","INITIAL_WEIGHT","DISTANCE"])

# SCALE = min(lambda_h,lambda_w) that is as both h and w changes if object moves,
# h' = lambda_h * h
# w' = lambda_w * w
# SCALE = min(lambda_h,lambda_w)
# SCALE * DISTANCE

for c in classes:
	fr.writerow([c,-1,-1,-1])