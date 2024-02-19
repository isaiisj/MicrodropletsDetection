import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from scipy import fftpack
from PIL import Image

####Function that creates a dialog box to show the number of droplets###
def show_variable(variable_value):
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    showinfo("Total droplets",f"Number of droplets {variable_value}")

########################################
'''
class CanvasImage:
    def __init__(self, title = "Image Loader"):
        self.master = tk.Tk()
        self.master.withdraw()
        self.master.title(title)
        self.canvas = tk.Canvas(self.master)
        self.canvas.grid(row = 0, column = 0, sticky = tk.NSEW)
        self.image_button = tk.Button(
            self.master, font = "Helvetica 12",
            text = "Choose Image", command = self.choose_image)
        self.image_button.grid(row = 1, column = 0, sticky = tk.NSEW)
        self.master.update()
        self.master.resizable(False, False)
        self.master.deiconify()
        self.image_path = None  # Variable to store the image path
    def choose_image(self):
        image_name = fd.askopenfilename(title = "Pick your image")
        print(image_name)
        if image_name:
            self.image_path = image_name  # Save the image path to the variable
            self.image = tk.PhotoImage(file = image_name, master = self.master)
            w, h = self.image.width(),self.image.height()
            self.canvas.config(width = w, height = h)
            self.canvas.create_image((0,0), image = self.image, anchor = tk.NW)
        return self.image_path '''
'''
if __name__ == "__main__":
    loader = CanvasImage()
    loader.master.mainloop()'''
'''
loader = CanvasImage()
path = loader.choose_image()
loader.master.mainloop()'''
###########################################################33

import tkinter as tk
from tkinter import filedialog as fd

class ImageSelectorApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Image Selector")
        self.master.resizable(False, False)

        self.label = tk.Label(master, text="Choose Image:")
        self.label.pack()

        self.image_path_var = tk.StringVar()
        self.image_path_label = tk.Label(master, textvariable=self.image_path_var)
        self.image_path_label.pack()

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image,font="Helvetica 12", width=35, height=3)
        #self.select_button.pack()
        self.select_button.pack(pady=10)

        self.selected_image_path = None

        #self.selected_image_paths = []

    def select_image(self):
        image_path = fd.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if image_path:
            relative_path = os.path.relpath(image_path)
            self.image_path_var.set(relative_path)
            self.selected_image_path = relative_path


#if __name__ == "__main__":
root = tk.Tk()
app = ImageSelectorApp(root)
root.mainloop()

path = app.selected_image_path
if path:
    print("Selected image path:", path)
else:
    print("No image selected.")

########################################################################

#Read image
img = cv2.imread(path, cv2.IMREAD_COLOR)

#Rotate image
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

#Resizing image
copia = img
copia = cv2.resize(copia,(1000,700),interpolation = cv2.INTER_AREA)
cv2.imshow("resized", copia)
cv2.waitKey(0)


#Separamos en 3 canales y Aumentamos contrasted del canal verde
#RGB split
b, g , r  = cv2.split(copia)
enhanced_green = cv2.equalizeHist(g)
# Merge the channels back
enhanced_image = cv2.merge([b, enhanced_green, r])
# Display the original and enhanced images
#cv2.imshow('Enhanced Image', enhanced_image)
#cv2.waitKey(0)


#Thresholding
_,th = cv2.threshold(enhanced_green,150,255, cv2.THRESH_BINARY)
#cv2.imshow("binary", th)
#cv2.waitKey(0)


#Bluring image
g2 = cv2.medianBlur(th,3)
#g2 = cv2.medianBlur(th,5)
#cv2.imshow("blurred", g2)
#cv2.waitKey(0)


#Border detection
g2 = cv2.Canny(g2,0,10)
#g2 = cv2.Canny(g2,0,20)
#cv2.imshow("canny", g2)
#cv2.waitKey(0)

#Border dilation and erode
g2 = cv2.dilate(g2, None, iterations=1)
g2 = cv2.erode(g2, None, iterations=1)
#cv2.imshow("dilate and erode", g2)
#cv2.waitKey(0)


#rows = g2.shape[0]
detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 6, minRadius = 5, maxRadius = 12)
#detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 11, minRadius = 13, maxRadius = 29)
detected_circles2 = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2  = 30, minRadius = 3, maxRadius = 27)

count = 0

if detected_circles is not None and detected_circles2 is not None:

    detected_circles = np.uint16(np.around(detected_circles))
    detected_circles2 = np.uint16(np.around(detected_circles2))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        cv2.circle(copia, (a,b), r, (0, 255, 0), 2)

        cv2.circle(copia, (a,b), 1, (0, 0, 255), 3)
        count += 1
        cv2.imshow("Circles", copia)
    
    '''for pt in detected_circles2[0, :]:
        a,b,r = pt[0], pt[1], pt[2]

        cv2.circle(copia, (a,b), r, (255,0,30),2)

        cv2.circle(copia, (a,b), r, (255, 65,30),3)

        cv2.imshow("l",copia)'''

 
############################################################################

#Read image
img2 = cv2.imread(path, cv2.IMREAD_COLOR)

#Rotate image
img3 = cv2.rotate(img2, cv2.ROTATE_90_CLOCKWISE)

#Resizing image
copia2 = img3
copia2 = cv2.resize(copia,(1000,700),interpolation = cv2.INTER_AREA)
cv2.imshow("resized", copia2)
cv2.waitKey(0)


#Separamos en 3 canales y Aumentamos contrasted del canal verde
#RGB split
b, g , r  = cv2.split(copia2)
#enhanced_green = cv2.equalizeHist(g)
# Merge the channels back
#enhanced_image = cv2.merge([b, enhanced_green, r])
# Display the original and enhanced images
#cv2.imshow('Enhanced Image', enhanced_image)
#cv2.waitKey(0)


#Thresholding
_,th = cv2.threshold(g,150,255, cv2.THRESH_BINARY)
#cv2.imshow("binary", th)
#cv2.waitKey(0)


#Bluring image
g2 = cv2.medianBlur(th,3)
#g2 = cv2.medianBlur(th,5)
#cv2.imshow("blurred", g2)
#cv2.waitKey(0)


#Border detection
g2 = cv2.Canny(g2,0,10)
#g2 = cv2.Canny(g2,0,20)
#cv2.imshow("canny", g2)
#cv2.waitKey(0)

#Border dilation and erode
g2 = cv2.dilate(g2, None, iterations=1)
g2 = cv2.erode(g2, None, iterations=1)
#cv2.imshow("dilate and erode", g2)
#cv2.waitKey(0)


#rows = g2.shape[0]
detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 6, minRadius = 5, maxRadius = 12)
#detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 11, minRadius = 13, maxRadius = 29)
detected_circles2 = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2  = 30, minRadius = 3, maxRadius = 27)

count2 = 0

if detected_circles is not None and detected_circles2 is not None:

    detected_circles = np.uint16(np.around(detected_circles))
    detected_circles2 = np.uint16(np.around(detected_circles2))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        cv2.circle(copia2, (a,b), r, (0, 255, 0), 2)

        cv2.circle(copia2, (a,b), 1, (0, 0, 255), 3)
        count2 += 1
        cv2.imshow("Circles", copia2)

############################################################################
#Displaying image
#cv2.imshow('image',copia)
#cv2.imshow('Green', g2)
#print(count)
show_variable(count)
sshow_variable(count2)
cv2.waitKey(0)
cv2.destroyAllWindows()
