import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
import torch
import torchvision.transforms as transforms
from torchvision import models

class ImageBlurApp:
    def __init__(self, window, window_title, image_path):
        self.window = window
        self.window.title(window_title)
        
        self.cv_image = cv2.imread(image_path)
        self.cv_image_rgb = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
        
        self.height, self.width, _ = self.cv_image.shape
        
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.cv_image_rgb))
        
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)
        self.canvas.pack()
        
        self.blur_weight = 5  
        self.is_mouse_pressed = False  
        self.start_x, self.start_y = 0, 0  
        
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        self.blur_slider = tk.Scale(window, from_=1, to=20, orient=tk.HORIZONTAL, label="Blur Weight",
                                    command=self.update_blur_weight)
        self.blur_slider.pack()  
    
    def on_mouse_press(self, event):
        self.is_mouse_pressed = True   
        self.start_x, self.start_y = event.x, event.y   
    
    def on_mouse_drag(self, event):
        if self.is_mouse_pressed:   
            end_x, end_y = event.x, event.y   
            start_x, start_y = self.start_x, self.start_y   
            
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(self.width, end_x)
            end_y = min(self.height, end_y)
            
            roi = self.cv_image_rgb[start_y:end_y, start_x:end_x]   
            blurred_roi = cv2.GaussianBlur(roi, (self.blur_weight, self.blur_weight), 0)   
            self.cv_image_rgb[start_y:end_y, start_x:end_x] = blurred_roi   
            self.update_display()   
    
    def on_mouse_release(self, event):
        self.is_mouse_pressed = False   
    
    def update_blur_weight(self, value):
        self.blur_weight = int(value)
    
    def update_display(self):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.cv_image_rgb))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)   

def main():
    image_path = "image.jpg"
    window = tk.Tk()   
    app = ImageBlurApp(window, "Image Blur App", image_path)   
    window.mainloop()   

if __name__ == "__main__":
    main()   
