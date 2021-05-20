from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
import psycopg2
import csv
from datetime import datetime

#def insertMovementDatawithSecond(int time, int uploadsensorid, int displacementxy):
#    int displacementtime = time 
    # insert into videodisplacementhistory(uploadsensorid, displacementtime, displacementxy) values(displacement, uploadsensorid, displacementxy)
f = open('records.csv', 'w')
        
data_counter = 1
array = np.zeros(10)
records = []
def data_counter_checker(array, data_counter, value):
    data_counter += 1
    array[data_counter] = value
    if data_counter%10 == 0:
        #save current array avarage into csv
        average = np.average(array)
        record = [average, datetime.now()]
        records.append(record)
        #clear current array
        array = np.zeros(10)
    
def save_records_into_csv(records, f):
    with f:
        writer = csv.writer(f)
        writer.writerows(records)


def image_process():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video", help="path to the (optional) video file")
    ap.add_argument("-b", "--buffer", default=32, help="buffer exceed")
    
    args = vars(ap.parse_args())
    
    
    greenLower = (29, 86, 6)
    greenUpper = (64, 255, 255)
    # initialize the list of tracked points, the frame counter,
    # and the coordinate deltas
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""
    # if a video path was not supplied, grab the reference
    # to the webcam
    if not args.get("video", False):
    	vs = VideoStream(src=0).start()
    # otherwise, grab a reference to the video file
    else:
    	vs = cv2.VideoCapture(args["video"])
    # allow the camera or video file to warm up
    time.sleep(2.0)
    
    # keep looping
    while True:
    	# grab the current frame
    	frame = vs.read()
    	frame = frame[1] if args.get("video", False) else frame
    	if frame is None:
    		break
        
    	# color space
    	frame = imutils.resize(frame, width=600)
    	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        
    	# construct a mask for the color "green", then perform
    	mask = cv2.inRange(hsv, greenLower, greenUpper)
    	mask = cv2.erode(mask, None, iterations=2)
    	mask = cv2.dilate(mask, None, iterations=2)
    	# find contours in the mask and initialize the current
    	# (x, y) center of the ball
    	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    		cv2.CHAIN_APPROX_SIMPLE)
    	cnts = imutils.grab_contours(cnts)
    	center = None
    	if len(cnts) > 0:
    		# it to compute the minimum enclosing circle and
    		# centroid
    		c = max(cnts, key=cv2.contourArea)
    		((x, y), radius) = cv2.minEnclosingCircle(c)
    		M = cv2.moments(c)
    		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    		# only proceed if the radius meets a minimum size
    		if radius > 10:
    			# draw the circle and centroid on the frame,
    			# then update the list of tracked points
    			cv2.circle(frame, (int(x), int(y)), int(radius),
    				(0, 255, 255), 2)
    			cv2.circle(frame, center, 5, (0, 0, 255), -1)
    			pts.appendleft(center)
        	# loop over the set of tracked points
    	for i in np.arange(1, len(pts)):
    		# if either of the tracked points are None, ignore
    		# them
    		if pts[i - 1] is None or pts[i] is None:
    			continue

    		if counter >= 10 and i == 1 and pts[-10] is not None:

    			# text variables
    			dX = pts[-10][0] - pts[i][0]
    			dY = pts[-10][1] - pts[i][1]
    			(dirX, dirY) = ("", "")
    			# x-direction
    			if np.abs(dX) > 20:
    				dirX = "East" if np.sign(dX) == 1 else "West"
    			# y-direction
    			if np.abs(dY) > 20:
    				dirY = "North" if np.sign(dY) == 1 else "South"
    			if dirX != "" and dirY != "":
    				direction = "{}-{}".format(dirY, dirX)                                                              
    			# otherwise, only one direction is non-empty
    			else:
    				direction = dirX if dirX != "" else dirY

    		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    		thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
    		cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
    	# the frame
    	curr_date = datetime.now()
    	print(curr_date)
    	#data_counter_checker(array, data_counter, dirY, dirX)        
    	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
    		0.65, (0, 0, 255), 3)
    	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
    		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    		0.35, (0, 0, 255), 1)
    	cv2.imshow("Frame", frame)
    	key = cv2.waitKey(1) & 0xFF
    	counter += 1
    	# if the 'q' key is pressed, stop the loop
    	if key == ord("q"):
    		#save_records_into_csv(records, f)          
    		break
    # if we are not using a video file, stop the camera video stream
    if not args.get("video", False):
    	vs.stop()
    # otherwise, release the camera
    else:
    	vs.release()
    # close all windows
    cv2.destroyAllWindows()
    
def videoAnalysisResultsData(db_connection, userid, videolenght, uploaddate, cameradistancecm):
    # create a cursor
    cur = conn.cursor()
    
    singlequote = """'"""
    uploaddate = singlequote +  uploaddate + singlequote
    cur.execute("SET datestyle TO " + singlequote + "ISO, DMY" + singlequote + ";")
    sql_statement1 = f"INSERT INTO videoanalysisresults (userid, videolenght, uploaddate, cameradistancecm) VALUES({userid}, {videolenght}, {uploaddate}, {cameradistancecm});"
    cur.execute(sql_statement1)
    conn.commit()
    
    sql_statement2 = f"SELECT * FROM videoanalysisresults WHERE userid = {userid} ;"
    cur.execute(sql_statement2)
    newdata = cur.fetchall()
    
    
    print('PostgreSQL videoanalysisresults created:')
    print(newdata)


if __name__ == "__main__":
    ### Database Connection ###
    conn = psycopg2.connect(
    host="",
    database="capstone",
    user="root",
    password="")
    
    
    #videoAnalysisResultsData(conn, 1, 10 , "20-04-2020", 50)
    image_process()

    
