import cv2               # Import OpenCV library for image processing
import numpy as np       # Import NumPy library for numerical computations
import tkinter as tk     # Import Tkinter library for GUI
from PIL import Image, ImageTk   # Import modules from Pillow library for image handling

class ImageBlurApp:
    def __init__(self, window, window_title, image_path):
        self.window = window   # Reference to the Tkinter window
        self.window.title(window_title)   # Set the title of the window
        
        # Load the image using OpenCV and convert it from BGR to RGB format
        self.cv_image = cv2.imread(image_path)
        self.cv_image_rgb = cv2.cvtColor(self.cv_image, cv2.COLOR_BGR2RGB)
        
        # Get the height and width of the image
        self.height, self.width, _ = self.cv_image.shape
        
        # Convert the OpenCV image to a format compatible with Tkinter
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.cv_image_rgb))
        
        # Create a Tkinter canvas to display the image
        self.canvas = tk.Canvas(window, width=self.width, height=self.height)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)  # Display the image on the canvas
        self.canvas.pack()   # Pack the canvas into the window
        
        self.blur_weight = 5  # Initial blur weight
        self.is_mouse_pressed = False  # Flag to track mouse press state
        self.start_x, self.start_y = 0, 0  # Variables to store starting coordinates of mouse drag
        
        # Bind mouse events to corresponding methods
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        
        # Create a Tkinter scale widget for adjusting blur weight
        self.blur_slider = tk.Scale(window, from_=1, to=20, orient=tk.HORIZONTAL, label="Blur Weight",
                                    command=self.update_blur_weight)
        self.blur_slider.pack()   # Pack the scale widget into the window
    
    # Method to handle mouse press event
    def on_mouse_press(self, event):
        self.is_mouse_pressed = True   # Set the mouse press flag to True
        self.start_x, self.start_y = event.x, event.y   # Store starting coordinates of mouse drag
    
    # Method to handle mouse drag event
    def on_mouse_drag(self, event):
        if self.is_mouse_pressed:   # Check if mouse is pressed
            end_x, end_y = event.x, event.y   # Get current mouse coordinates
            start_x, start_y = self.start_x, self.start_y   # Get starting coordinates
            
            # Ensure selected region is within image boundaries
            start_x = max(0, start_x)
            start_y = max(0, start_y)
            end_x = min(self.width, end_x)
            end_y = min(self.height, end_y)
            
            # Update the selected region with blur effect
            if start_x < end_x and start_y < end_y:
                roi = self.cv_image_rgb[start_y:end_y, start_x:end_x]# Extract selected region
                if roi.size > 0:  # Check if ROI is not empty
                    blurred_roi = cv2.GaussianBlur(roi, (self.blur_weight, self.blur_weight), 0)# Apply blur
                    self.cv_image_rgb[start_y:end_y, start_x:end_x] = blurred_roi # Update image
                    self.update_display() # Update the displayed image
    
    # Method to handle mouse release event
    def on_mouse_release(self, event):
        self.is_mouse_pressed = False   # Set the mouse press flag to False
    
    # Method to update the blur weight based on slider value
    def update_blur_weight(self, value):
        self.blur_weight = int(value)   # Update blur weight
    
    # Method to update the displayed image on the canvas
    def update_display(self):
        self.image = ImageTk.PhotoImage(image=Image.fromarray(self.cv_image_rgb))   # Convert image format
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)   # Display the updated image

# Main function
def main():
    image_path = "image.jpg"   # Path to the input image
    window = tk.Tk()   # Create a Tkinter window
    app = ImageBlurApp(window, "Image Blur App", image_path)   # Create an instance of the ImageBlurApp
    window.mainloop()   # Start the Tkinter event loop

# Entry point of the program
if __name__ == "__main__":
    main()   # Call the main function
