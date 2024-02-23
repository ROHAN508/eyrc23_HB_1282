import cv2
import numpy as np

# Read the image
image = cv2.imread('/home/akshar/eyrc_hb/hb_task5_ws/src/hb_task5a/hb_task5a/image_mode.png')

# Resize the image to 500x500 pixels
resized_image = cv2.resize(image, (500, 500))

# Convert the image to grayscale
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Adaptive thresholding to create a binary image
binary = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 4)

# Find contours in the binary image
contours, hierarchy = cv2.findContours(binary, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

# Create a copy of the original image to draw contours on
contour_image = resized_image.copy()

# Save the coordinates of the contours into separate lists in the text file
with open('contours_coordinates.txt', 'w') as file:
    for i, contour in enumerate(contours):
        contour_list = contour.tolist()  # Convert contour to Python list
        file.write(f'Contour {i+1}: {contour_list}\n')
        
        # Draw contours on the image
        cv2.drawContours(contour_image, [contour], -1, (0, 0, 255), 2)

# Show the contour image
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
