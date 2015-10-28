import cv2
import numpy as np
import time
import serial

ser = serial.Serial('COM16', 9600, timeout=0, writeTimeout=0)

# Sleep to allow Arduino to boot
time.sleep(2)

class Motors:
    """Sends speed updates via serial."""
    def __init__(self):
        self.prev_left = 0
        self.prev_right = 0

    def set_speed(self, left, right):
        '''
        if left != self.prev_left or right != self.prev_right:
            self.update_speed()
        '''
        self.prev_left = left
        self.prev_right = right
        ser.write("M" + str(self.prev_left) + ":" + str(self.prev_right))

    def update_speed(self):
        ser.write("M" + str(self.prev_left) + ":" + str(self.prev_right))

def nothing(x):
    pass


def current_time_millis():
    return int(round(time.time() * 1000))

cap = cv2.VideoCapture(2)
cap.set(3, 700)
cap.set(4, 700)
cap.set(5, 15)

# Create color selection window
cv2.namedWindow("Color Selection")
img = np.zeros((100, 100, 1), np.uint8)
cv2.createTrackbar("U Lower", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("V Lower", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("U Upper", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("V Upper", "Color Selection", 0, 255, nothing)
cv2.createTrackbar("Speed Divisor", "Color Selection", 1, 255, nothing)

# Initialize classes
motors = Motors()

# Get capture properties
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
center_frame_x = int(frame_width / 2)
center_frame_y = int(frame_height / 2)

while 1:
    # Grab YUV bounds
    lower = np.array([0, cv2.getTrackbarPos("U Lower", "Color Selection"), cv2.getTrackbarPos("V Lower", "Color Selection")])
    upper = np.array([255, cv2.getTrackbarPos("U Upper", "Color Selection"), cv2.getTrackbarPos("V Upper", "Color Selection")])

    # Take each frames
    _, original_frame = cap.read()

    # Convert BGR to YUV
    object_outline = original_frame.copy()
    hsv = cv2.cvtColor(original_frame, cv2.COLOR_BGR2YUV)
    hsv = cv2.GaussianBlur(hsv, (3, 3), 0)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower, upper)

    # Clean up noise
    cv2.imshow('Mask Before', mask)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=3)
    mask = cv2.dilate(mask, kernel, iterations=3)
    cv2.imshow('Mask After', mask)

    # Draw box
    contours = cv2.findContours(mask, 1, 2)
    cnt = contours[0]
    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(object_outline, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.circle(object_outline, (x + w/2, y + h/2), 2, (0, 255, 0), 5)

    # Turn to keep the object centered
    x_pos = x + (w / 2)
    y_pos = y + (h / 2)

    speed = (abs(y_pos - center_frame_y)) / cv2.getTrackbarPos("Speed Divisor", "Color Selection")

    print speed

    if x_pos == 0 and y_pos == 0:
        # Do nothing
        print "No object found"
        motors.set_speed(0, 0)
    elif (y_pos > center_frame_y - 75) and (y_pos < center_frame_y + 75):
        speed = (abs(x_pos - center_frame_x)) / cv2.getTrackbarPos("Speed Divisor", "Color Selection")

        if x_pos > center_frame_x + 25:
            # Turn right
            print "Turning right..."
            motors.set_speed(speed / 2, "-" + str(speed / 2))
        elif x_pos < center_frame_x - 25:
            # Turn left
            print "Turning left..."
            motors.set_speed("-" + str(speed / 2), speed / 2)
        else:
            # Aligned
            print "Aligned"
            motors.set_speed(0, 0)
    elif y_pos > center_frame_y - 75:
        # Reverse
        print "Reversing..."
        motors.set_speed(-10, -10)
    elif y_pos < center_frame_y + 75:
        print "Driving..."
        motors.set_speed(10, 10)
    else:
        print "Nothing to do"
        motors.set_speed(0, 0)

    # Draw center target
    cv2.line(object_outline, (0, center_frame_y + 75), (frame_width, center_frame_y + 75), (0, 255, 255), 2)
    cv2.line(object_outline, (0, center_frame_y - 75), (frame_width, center_frame_y - 75), (0, 255, 255), 2)
    cv2.line(object_outline, (center_frame_x, center_frame_y + 75), (center_frame_x, center_frame_y - 75), (0, 255, 255), 2)
    cv2.line(object_outline, (center_frame_x - 25, center_frame_y), (center_frame_x + 25, center_frame_y), (0, 255, 255), 2)

    cv2.imshow('Detected Object', object_outline)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

time.sleep(1)
motors.set_speed(0, 0)
colors.set_color(0, 0, 0)
ser.close()
cv2.destroyAllWindows()
