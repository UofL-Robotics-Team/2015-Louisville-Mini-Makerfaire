import cv2
import numpy as np


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

    # detect circles in the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 500)

    # ensure at least some circles were found
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

    cv2.imshow("Final", frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
