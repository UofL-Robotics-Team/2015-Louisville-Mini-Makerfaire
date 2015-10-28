import cv2
import numpy as np
import serial
import time

ser = serial.Serial('COM15', 9600, timeout=0, writeTimeout=100)

# Sleep to allow Arduino to boot
time.sleep(2)

cap = cv2.VideoCapture(2)
cap.set(3, 500)
cap.set(4, 500)
cap.set(5, 15)

while 1:
    # Take each frame
    (_, frame) = cap.read()

    # Get capture properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    center_frame_x = int(frame_width / 2)
    center_frame_y = int(frame_height / 2)

    # Highlight ROI
    cv2.rectangle(frame, (center_frame_x - 110, center_frame_y - 85), (center_frame_x + 110, center_frame_y + 85), (255, 255, 0), 2)

    # Convert to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray[(center_frame_x - 110):(center_frame_y - 85), (center_frame_x + 110):(center_frame_y + 85)]
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    edges = cv2.Canny(gray, 225, 250)

    (_, contours, h) = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop through contours
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)

        if len(approx) == 7:
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), -1)

            # Follow shape by calculating center point with a bounding box
            x, y, w, h = cv2.boundingRect(cnt)

            # Turn to keep the object centered
            x_pos = x + (w / 2)

            # Send command
            if x_pos == 0:
                # Do nothing
                print "No object found"
                ser.write("l0r0R0G0B0")
            elif x_pos > center_frame_x + 50:
                # Turn right
                print "Turning right..."
                ser.write("l20r-20R255G0B0")
            elif x_pos < center_frame_x - 50:
                # Turn left
                print "Turning left..."
                ser.write("l-20r20R255G0B0")
            else:
                # Aligned
                print "Aligned"
                ser.write("l0r0R0G255B0")

        elif len(approx) == 3:
            cv2.drawContours(frame, [cnt], -1, (255, 0, 0), -1)

    #cv2.imshow("Gray", gray)
    #cv2.imshow("Edges", edges)
    cv2.imshow("Final", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

time.sleep(1)
ser.close()
cv2.destroyAllWindows()
