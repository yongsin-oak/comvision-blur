import cv2
from PIL import Image
import numpy as np
from rembg import remove

drawing_left = False
drawing_right = False 
roi_size = 20  # Define the size of the region of interest (ROI)
def draw_blur(event, x, y, flags, param):
    global drawing_left, drawing_right, img_result, backup_img, roi_size
    
    roi_x = max(0, x - roi_size // 2)  # Calculate the left corner of the ROI
    roi_y = max(0, y - roi_size // 2) # Calculate the top corner of the
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing_left = True #left clicked
    
    if event == cv2.EVENT_RBUTTONDOWN:
        drawing_right = True #right clicked

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing_left == True:
            roi = img_result[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size]  # Extract the ROI
            blurred_roi = cv2.GaussianBlur(roi, (7, 7), 0)  # Apply Gaussian blur to the ROI
            img_result[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size] = blurred_roi  # Update the image

        if drawing_right == True:
            roi = backup_img[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size]  # Extract the ROI from backup_img
            img_result[roi_y:roi_y + roi_size, roi_x:roi_x + roi_size] = roi  # Restore the original ROI
            
    elif event == cv2.EVENT_LBUTTONUP:
        drawing_left = False #Mouse released

    elif event == cv2.EVENT_RBUTTONUP:
        drawing_right = False #Mouse released

def cv_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
def pil_to_cv(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
def background_gaussian_blur(background, kernel_size, sigma):
    
    # Remove background
    subject = remove(background)

    # Blur the background
    background_blur = gaussian_blur(background, kernel_size, sigma)
    
    # Put the subject on top of the blur background
    subject_on_blur_background = background_blur.copy()
    subject_on_blur_background.paste(background, (0, 0), subject)

    # Blend the subject and the blur background
    result = Image.blend(background_blur, subject_on_blur_background, 1)
    
    # pil to cv
    result_cv = pil_to_cv(result)

    return result_cv
def gaussian_blur(img, kernel_size, sigma):
    # Convert PIL image to numpy array
    cv_img = pil_to_cv(img)

    # Apply Gaussian blur
    blurred_img = cv2.GaussianBlur(cv_img, (kernel_size, kernel_size), sigma)

    # Convert numpy array back to PIL image
    blurred_pil_img = cv_to_pil(blurred_img)

    return blurred_pil_img
# import image
img = cv2.imread('bts.jpg')
# cv to pil
img_pil = cv_to_pil(img)
#image original
backup_img = pil_to_cv(img_pil)
img_result = background_gaussian_blur(img_pil, 25, 5)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_blur)
while True:
    cv2.imshow('image', img_result)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):  # Press 'q' to exit
        break
cv2.destroyAllWindows()
