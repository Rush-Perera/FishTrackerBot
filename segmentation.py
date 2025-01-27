import cv2
import numpy as np
import os

# Folder paths
input_folder = 'snaps/'
output_folder = 'output/'

# List all PNG files in the 'snaps' folder
image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Process each image in the folder
for file_name in image_files:
    # Load the image
    image_path = os.path.join(input_folder, file_name)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Image {file_name} not loaded. Check the file path or file format.")
        continue

    # Resize the image for easier processing
    image = cv2.resize(image, (800, 600))

    # Convert the image to HSV color space for better segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for orange/red colors (assuming fish color is reddish-orange)
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
        
        # Draw the bounding box on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Calculate the aspect ratio (width/height)
        aspect_ratio = float(w) / h

        # If the aspect ratio is high, assume horizontal orientation
        if aspect_ratio > 1:
            # Identify head/tail by comparing the left and right parts
            head = tuple(hull[hull[:, :, 0].argmax()][0])  # Rightmost point (head)
            tail = tuple(hull[hull[:, :, 0].argmin()][0])  # Leftmost point (tail)
        else:
            # Otherwise, assume vertical orientation
            head = tuple(hull[hull[:, :, 1].argmax()][0])  # Topmost point (head)
            tail = tuple(hull[hull[:, :, 1].argmin()][0])  # Bottommost point (tail)

        # Draw the head and tail points
        cv2.circle(image, head, 8, (0, 0, 255), -1)  # Head: red circle
        cv2.circle(image, tail, 8, (255, 0, 0), -1)  # Tail: blue circle

        # Draw an arrow from tail to head
        cv2.arrowedLine(image, tail, head, (255, 255, 0), 3, tipLength=0.2)

    # Save or display the processed image
    output_path = os.path.join(output_folder, file_name)
    cv2.imwrite(output_path, image)
    print(f"Processed image saved at {output_path}")
