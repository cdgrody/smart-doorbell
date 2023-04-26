import numpy as np
import cv2
import imutils
import time
import os

def mask_image(img):
	mask = np.zeros((img.shape[0], img.shape[1]), dtype="uint8")

	#for i in range(0,1):
	#	bbox = cv2.selectROI(img, False)
	#	print(bbox)

	pts = np.array([[3, 687], [3, 205], [421, 211], [433, 31], [731, 17], [737, 183], [901,693]]) 
	cv2.fillConvexPoly(mask, pts, 255)

	masked = cv2.bitwise_and(img, img, mask=mask)
	
	gray = imutils.resize(masked, width = 200)

	gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)

	gray = cv2.GaussianBlur(gray, (11,11), 0)


	return masked, gray

#Counter variable for analysis
counter = 0

while True:

	counter=counter+1
	print(" ")
	print( "----Times through loop since starting:", counter, "------")
	print(" ")

	# take a first and second image to compare
	command = 'raspistill -w 1280 -h 720 -vf -hf -t 1000 -tl 1000 -o test%d.jpg'
	os.system(command)

	print("Captured 1st & 2nd image for analysis...")

	# mask images
	test1 = cv2.imread("test0.jpg")
	test2 = cv2.imread("test1.jpg")
	masked1, gray1 = mask_image(test1)
	masked2, gray2 = mask_image(test2)

	cv2.imwrite("gray1.jpg", gray1)
	cv2.imwrite("gray2.jpg", gray2)
	cv2.imwrite("masked1.jpg", masked1)
	cv2.imwrite("masked2.jpg", masked2)

	# compare the two images
	pixel_threshold = 50
	
	detector_total = np.uint64(0)
	detector=np.zeros((gray2.shape[0], gray2.shape[1]), dtype="uint8")

	# pixel by pixel comparison
	for i in range(0, gray2.shape[0]):
		for j in range(0,gray2.shape[1]):
			if abs(int(gray2[i,j] - gray1[i,j]))> pixel_threshold: 
				detector[i,j] = 255
	# sum the detector array
	detector_total=np.uint64(np.sum(detector))
	print("detect_total = ", detector_total)
	print(" ")

	time.sleep(1)

	if detector_total > 30000:

		print("Smart Doorbell has detected someone/something")

		# define a unique name for the video file
		timestr = time.strftime("doorbell -%Y%m%d-%H%M%S")

		command2 = 'raspivid -t 15000 -w 1280 -h 720 -vf -hf -fps 30 -o ' + timestr + '.h264' 
		os.system(command2)

		print("Finished recording...converting to mp4...")

		command3 = 'MP4Box -fps 30 -add ' + timestr + '.h264' + timestr + '.mp4'
		os.system(command3)

		print("Finished converting file available for viewing")

			# write masked images to file

