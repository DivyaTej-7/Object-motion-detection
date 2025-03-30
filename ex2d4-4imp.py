import cv2
import time
import imutils
import csv
import math

# Initialize camera
cam = cv2.VideoCapture(0)
time.sleep(1)

if not cam.isOpened():
    print("Error: Could not access the camera.")
    exit()

firstFrame = None
area = 500
start_time = time.time()
duration = 10  # Run for 10 seconds
max_retries = 5  # Max attempts to read a frame
error_count = 0

# Open CSV file for writing
with open("object_coordinates.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Frame", "Object_ID", "X", "Y", "Width", "Height", "Distance_to_Next", "Error"])
    
    frame_count = 0
    retries = 0
    
    while True:
        if time.time() - start_time > duration:
            break
        
        ret, img = cam.read()
        if not ret or img is None:
            print("Error: Could not read frame from camera")
            retries += 1
            error_count += 1
            writer.writerow([frame_count, "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "Frame Read Error"])
            if retries >= max_retries:
                print("Error: Maximum retry limit reached. Exiting.")
                break
            continue
        
        retries = 0  # Reset retry counter on success
        text = "Normal"
        img = imutils.resize(img, width=500)
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaussianImg = cv2.GaussianBlur(grayImg, (21, 21), 0)

        if firstFrame is None:
            firstFrame = gaussianImg
            continue
        
        imgDiff = cv2.absdiff(firstFrame, gaussianImg)
        threshImg = cv2.threshold(imgDiff, 25, 255, cv2.THRESH_BINARY)[1]
        threshImg = cv2.dilate(threshImg, None, iterations=2)
        cnts = cv2.findContours(threshImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        object_data = []
        object_id = 0
        
        for c in cnts:
            if cv2.contourArea(c) < area:
                continue
            
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = "Moving Object detected"
            
            object_data.append((object_id, x, y, w, h))
            object_id += 1
        
        # Calculate distances between detected objects
        distances = []
        for i in range(len(object_data)):
            for j in range(i + 1, len(object_data)):
                x1, y1 = object_data[i][1], object_data[i][2]
                x2, y2 = object_data[j][1], object_data[j][2]
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                distances.append((object_data[i][0], object_data[j][0], distance))

        # Write object data to CSV
        for obj in object_data:
            obj_id, x, y, w, h = obj
            nearest_distance = min([dist[2] for dist in distances if dist[0] == obj_id or dist[1] == obj_id], default=0)
            writer.writerow([frame_count, obj_id, x, y, w, h, nearest_distance, "No Error"])

        frame_count += 1
        
        print(text)
        cv2.putText(img, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.imshow("cameraFeed", img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

cam.release()
cv2.destroyAllWindows()
