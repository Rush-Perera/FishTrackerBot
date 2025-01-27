import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import math

# Setup Raspberry Pi GPIO pins
# Motor GPIO pins (Adjust these as per your robot wiring)
motor_left_forward = 17  # GPIO pin for left motor forward
motor_left_backward = 27  # GPIO pin for left motor backward
motor_right_forward = 22  # GPIO pin for right motor forward
motor_right_backward = 23  # GPIO pin for right motor backward

# Initialize GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_left_forward, GPIO.OUT)
GPIO.setup(motor_left_backward, GPIO.OUT)
GPIO.setup(motor_right_forward, GPIO.OUT)
GPIO.setup(motor_right_backward, GPIO.OUT)

# Function to move the robot forward
def move_forward():
    GPIO.output(motor_left_forward, GPIO.HIGH)
    GPIO.output(motor_left_backward, GPIO.LOW)
    GPIO.output(motor_right_forward, GPIO.HIGH)
    GPIO.output(motor_right_backward, GPIO.LOW)

# Function to stop the robot
def stop_robot():
    GPIO.output(motor_left_forward, GPIO.LOW)
    GPIO.output(motor_left_backward, GPIO.LOW)
    GPIO.output(motor_right_forward, GPIO.LOW)
    GPIO.output(motor_right_backward, GPIO.LOW)

# Function to rotate the robot
def rotate_robot(angle):
    # Rotate based on the angle
    if angle > 0:
        # Rotate right (clockwise)
        GPIO.output(motor_left_forward, GPIO.HIGH)
        GPIO.output(motor_left_backward, GPIO.LOW)
        GPIO.output(motor_right_forward, GPIO.LOW)
        GPIO.output(motor_right_backward, GPIO.HIGH)
    else:
        # Rotate left (counter-clockwise)
        GPIO.output(motor_left_forward, GPIO.LOW)
        GPIO.output(motor_left_backward, GPIO.HIGH)
        GPIO.output(motor_right_forward, GPIO.HIGH)
        GPIO.output(motor_right_backward, GPIO.LOW)

# Capture the image from the camera
def capture_image():
    # Use your camera setup here (USB camera or Pi Camera)
    # If using USB camera:
    camera = cv2.VideoCapture(0)
    ret, image = camera.read()
    camera.release()
    if not ret:
        print("Error: Failed to capture image.")
        return None
    return image

# Process the captured image and calculate the angle
def process_image(image):
    # Resize the image for easier processing
    image = cv2.resize(image, (800, 600))

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for orange/red colors (fish color)
    lower_range = np.array([0, 100, 100])  # Adjust values as needed
    upper_range = np.array([20, 255, 255])

    # Create a mask for the fish
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # Perform morphological operations to clean up the mask
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=3)

    # Find contours of the fish
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assume the largest contour is the fish
        largest_contour = max(contours, key=cv2.contourArea)

        # Get the convex hull of the largest contour
        hull = cv2.convexHull(largest_contour)

        # Get the bounding box for the fish (approximating the fish shape)
        x, y, w, h = cv2.boundingRect(hull)
        
        # Calculate the aspect ratio (width/height)
        aspect_ratio = float(w) / h

        # Identify head/tail points based on orientation
        if aspect_ratio > 1:
            # Horizontal orientation (head to right)
            head = tuple(hull[hull[:, :, 0].argmax()][0])  # Rightmost point (head)
            tail = tuple(hull[hull[:, :, 0].argmin()][0])  # Leftmost point (tail)
        else:
            # Vertical orientation (head upwards)
            head = tuple(hull[hull[:, :, 1].argmax()][0])  # Topmost point (head)
            tail = tuple(hull[hull[:, :, 1].argmin()][0])  # Bottommost point (tail)

        # Calculate the angle between the horizontal and the head-tail line
        delta_x = head[0] - tail[0]
        delta_y = head[1] - tail[1]
        angle = math.degrees(math.atan2(delta_y, delta_x))

        # Return the calculated angle
        return angle
    return None

# Main program loop
try:
    while True:
        image = capture_image()
        if image is not None:
            angle = process_image(image)
            if angle is not None:
                print(f"Angle from horizontal: {angle:.2f}°")

                # Adjust robot orientation based on angle
                if angle > 10:
                    rotate_robot(angle)  # Rotate right if angle is positive
                elif angle < -10:
                    rotate_robot(angle)  # Rotate left if angle is negative
                else:
                    move_forward()  # Move forward if angle is close to zero
            else:
                print("Fish not detected.")
                stop_robot()
        time.sleep(1)  # Wait before capturing the next image
except KeyboardInterrupt:
    # Stop robot if interrupted
    stop_robot()
    GPIO.cleanup()
    print("Program interrupted and stopped.")
