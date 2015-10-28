import cv2
import numpy as np
import time
import serial

cap = cv2.VideoCapture(2)
cap.set(3, 500)
cap.set(4, 500)
cap.set(5, 25)

cv2.namedWindow("Color Selection")
img = np.zeros((100, 100, 1), np.uint8)
cv2.createTrackbar("U Lower", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("V Lower", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("U Upper", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("V Upper", "Color Selection", 0, 255, nothing)


def nothing(x):
    pass


while 1:
    # Grab YUV bounds
    lower = np.array([0, cv2.getTrackbarPos("U Lower", "Color Selection"), cv2.getTrackbarPos("V Lower", "Color Selection")])
    upper = np.array([255, cv2.getTrackbarPos("U Upper", "Color Selection"), cv2.getTrackbarPos("V Upper", "Color Selection")])

    # Take each frame
    _, original_frame = cap.read()

    cv2.imshow("Original Image", original_frame)

    # Convert BGR to HSV
    object_outline = original_frame.copy()
    hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (3, 3), 0)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Clean up noise
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=4)
    mask = cv2.dilate(mask, kernel, iterations=4)
    cv2.imshow('Mask After', mask)

    # Edge detection
    edges = cv2.Canny(mask, 200, 225)

    cv2.imshow("Edge Detection", edges)

    # Draw box
    _, contours, h = cv2.findContours(mask, 1, 2)

    # Loop through contours
    for cnt in contours:
        cv2.drawContours(object_outline, [cnt], -1, (193, 192, 255), -1)

        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(object_outline, (x, y), (x + w, y + h), (0, 255, 0), 2)

    x = 0
    y = 0
    w = 0
    h = 0

    # Turn to keep the object centered
    x_pos = x + (w / 2)

    # Get capture properties
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    center_frame_x = int(frame_width / 2)
    center_frame_y = int(frame_height / 2)

    if x_pos == 0:
        # Do nothing
        print "No object found"
    elif x_pos > center_frame_x + 50:
        # Turn right
        print "Turning right..."
    elif x_pos < center_frame_x - 50:
        # Turn left
        print "Turning left..."
    else:
        # Aligned
        print "Aligned"

    # Draw center target
    cv2.line(object_outline, (center_frame_x - 50, center_frame_y), (center_frame_x + 50, center_frame_y), (255, 0, 0), 2)
    cv2.line(object_outline, (center_frame_x, center_frame_y - 50), (center_frame_x, center_frame_y + 50), (255, 0, 0), 2)

    cv2.imshow('Detected Object', object_outline)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

time.sleep(1)
cv2.destroyAllWindows()
