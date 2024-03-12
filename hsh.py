import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1

def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, img

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            roi_size = 20  # Define the size of the region of interest (ROI)
            roi_x = max(0, x - roi_size // 2)  # Calculate the top-left corner of the ROI
            roi_y = max(0, y - roi_size // 2)
            roi = img[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size]  # Extract the ROI
            blurred_roi = cv2.GaussianBlur(roi, (7, 7), 0)  # Apply Gaussian blur to the ROI
            img[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size] = blurred_roi  # Update the image

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

img = cv2.imread('image.jpg')  # Load your image here
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

while True:
    cv2.imshow('image', img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):  # Press 'q' to exit
        break

cv2.destroyAllWindows()