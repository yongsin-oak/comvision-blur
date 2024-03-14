import cv2
import gradio as gr
from Blur import background_gaussian_blur  # Update the import statement to match your script

def blur(img, kernel_size, sigma):  # Change function name and parameters accordingly
    return background_gaussian_blur(img, kernel_size, sigma)  # Update function call accordingly

iface = gr.Interface(fn=blur,
                     title="Background Gaussian Blur",  # Update title

                     inputs=[gr.Image(type='pil', label='Image'),
                             gr.Slider(label='Kernel Size', minimum=1, maximum=25, value=25),  # Update slider label and range
                             gr.Slider(label='Sigma', minimum=0.0, maximum=5.0, value=5)],  # Update slider label and range

                     outputs=gr.Image(label='Output'))  # Update output label

iface.gr.inputs[0].annotate = True
drawing = False  # True if mouse is pressed
ix, iy = -1, -1
iface.launch()