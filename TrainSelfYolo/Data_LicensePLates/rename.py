import os
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-t', '--target', required=True,
                help = 'Target Path (Path where files to be renamed are in)')
args = ap.parse_args()

TARGET_PATH=args.target+'/'
#TARGET_PATH="/media/ronit/DATA21/Programming/ObjectDetection/TrainSelfYolo/Data_LicensePLates/Google_Search/"
DEST_PATH="/media/ronit/DATA21/Programming/ObjectDetection/TrainSelfYolo/Data_LicensePLates/Google_Search/"

if(DEST_PATH==TARGET_PATH):
	count=1
else:
	count=len(os.listdir(DEST_PATH))+1

files=os.listdir(TARGET_PATH)
for f in files:
	f2=f.split('.')
	if(f2[-1]=='jpg' or f2[-1]=='jpeg' or f2[-1]=='png'):
		f3="i"+str(count)+"."+f2[-1]
		count=count+1
		os.rename(TARGET_PATH+f,TARGET_PATH+f3)
	else:
		os.remove(TARGET_PATH+f)