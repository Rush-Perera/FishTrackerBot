import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

# Folder paths
input_folder = 'snaps/'
output_folder = 'output/centerplot/'

# List all PNG files in the 'snaps' folder
image_files = [f for f in os.listdir(input_folder) if f.endswith('.png')]

# Prepare list to store center positions
centers = []

# Process each image in the folder
for file_name in image_files:
    # Load the image
    image_path = os.path.join(input_folder, file_name)
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Image {file_name} not loaded. Check the file path or file format.")
        continue

    # Resize the image for easier processing
    image_resized = cv2.resize(image, (800, 600))

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)

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

        # Get the bounding box for the fish (approximating the fish shape)
        x, y, w, h = cv2.boundingRect(largest_contour)

        # Calculate the center coordinates of the fish (bounding box center)
        center_x = x + w // 2
        center_y = y + h // 2

        # Store the center position
        centers.append((center_x, center_y))

        # Draw the bounding box and center on the image
        cv2.rectangle(image_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(image_resized, (center_x, center_y), 5, (0, 0, 255), -1)

    # Save the processed image with bounding box and center
    output_path = os.path.join(output_folder, file_name)
    cv2.imwrite(output_path, image_resized)
    print(f"Processed image saved at {output_path}")

# Plot the fish center positions
centers_np = np.array(centers)
plt.scatter(centers_np[:, 0], centers_np[:, 1], color='red')
plt.title('Fish Centers in Images')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.show()
