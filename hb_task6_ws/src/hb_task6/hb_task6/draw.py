import cv2
import ast
import numpy as np

# Create a white background image
white_image = 255 * np.ones((500, 500, 3), dtype=np.uint8)

# Read contours from the text file
contours = []
with open('/home/akshar/eyrc_hb/contours_coordinates.txt', 'r') as file:
    for line in file:
        # Extract contour coordinates from the line
        if line.startswith('Contour'):
            # Parse contour coordinates from string to list
            contour_str = line.split(': ')[1].strip()
            contour = ast.literal_eval(contour_str)
            contours.append(contour)

# Draw contours on the white image
for contour in contours:
    # Convert contour to numpy array
    contour = np.array(contour)
    # Reshape contour to have correct dimensions
    contour = contour.reshape((-1, 1, 2))
    # Draw contour on the white image
    cv2.drawContours(white_image, [contour], -1, (0, 0, 0), 2)

# Show the image with contours
cv2.imshow('Contours', white_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
