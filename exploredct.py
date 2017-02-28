# import the necessary packages
import argparse
import cv2
from collections import namedtuple
import numpy as np
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []
cropping = False

Pt2 = namedtuple("Pt2",("x","y"))
Pt3 = namedtuple("Pt3",("x","y","z"))
 
def click_and_crop(event, x, y, flags, image):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		pass
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		pt = Pt2(x,y)
		pte = Pt2(min(image.shape[1],pt.x+8),min(image.shape[0],pt.y+8))

		region8x8 = image[pt.y:pte.y,pt.x:pte.x]
		region8x8dct = cv2.dct(region8x8.astype(np.float32))
		mima = (np.min(region8x8dct),np.max(region8x8dct))
		region8x8dct = (region8x8dct-mima[0])*(255.0/(mima[1]-mima[0]))
		mima = (np.min(region8x8dct),np.max(region8x8dct))
		print "minmax",mima
		cv2.imshow("roi",cv2.resize(region8x8,(80,80)))
		cv2.imshow("dct",cv2.resize(region8x8dct.astype(np.uint8),(80,80)))


def main():
	# construct the argument parser and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("image",help="Path to the image")
	args = vars(ap.parse_args())
	 
	# load the image, clone it, and setup the mouse callback function
	image = cv2.imread(args["image"],cv2.IMREAD_GRAYSCALE)
	clone = image.copy()
	cv2.namedWindow("image")
	cv2.namedWindow("roi",cv2.WINDOW_NORMAL)
	cv2.namedWindow("dct",cv2.WINDOW_NORMAL)
	cv2.resizeWindow("roi", 80, 80)
	cv2.resizeWindow("dct", 80, 80)
	cv2.setMouseCallback("image", click_and_crop, image)
	 
	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF
	 
		# if the 'r' key is pressed, reset the cropping region
		if key == ord("r"):
			image = clone.copy()
	 
		# if the 'c' key is pressed, break from the loop
		elif key == ord("c"):
			break
	 
	 
	# close all open windows
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()