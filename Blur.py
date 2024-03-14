import cv2
from PIL import Image
import numpy as np
from rembg import remove

def cv_to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA))
def pil_to_cv(img):
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
def background_gaussian_blur(background, kernel_size, sigma):
    # Remove background
    subject = remove(background)
    amount_subject = 1

    # Blur the background
    background_blur = gaussian_blur(background, kernel_size, sigma)

    # Put the subject on top of the blur background
    subject_on_blur_background = background_blur.copy()
    subject_on_blur_background.paste(background, (0, 0), subject)

    # Blend the subject and the blur background
    result = Image.blend(background_blur, subject_on_blur_background, amount_subject)
    
    result_cv = pil_to_cv(result)
    return result
def gaussian_blur(img, kernel_size, sigma):
    # Convert to RGBA
    img = img.convert('RGBA')
    
    # Convert PIL image to numpy array
    cv_img = pil_to_cv(img)

    # Apply Gaussian blur
    blurred_img = cv2.GaussianBlur(cv_img, (kernel_size, kernel_size), sigma)

    # Convert numpy array back to PIL image
    blurred_pil_img = cv_to_pil(blurred_img).convert('RGBA')

    return blurred_pil_img
