import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


def getInput(): 
    inp = inputtxt.get(1.0, "end-1c") 
    #lbl.config(text = "Provided Input: "+inp) 
    return inp

def setPath():
    global path
    path = getInput()
    frame.destroy()

# Top level window 
frame = tk.Tk() 
frame.title("Introduzca imagen") 
frame.geometry('400x200') 
# Function for getting Input 
# from textbox and printing it  
# at label widget 

inputtxt = tk.Text(frame, height=5, width=20)
inputtxt.pack()

printButton = tk.Button(frame, text="Scan", command=setPath)
printButton.pack()


'''
# Get the current working directory (directory where the script is located)
script_directory = os.path.dirname(os.path.abspath(__file__))

# Top level window 
frame = tk.Tk() 
frame.title("Introduzca imagen") 
frame.geometry('400x200') 
# Function for getting Input 
# from textbox and printing it  
# at label widget 

def select_file():
    global path

    filetypes = (
        ('Image files', '*.jpg'),
        ('Image files', '*.JPG'),
        ('All files', '*.*')
    )


    path = fd.askopenfilename(
        title='Open a file',
        initialdir=script_directory,
        filetypes=filetypes)

    showinfo(
        title='Selected File',
        message=path
    )

    if path:
        frame.destroy()


# open button
open_button = ttk.Button(
    frame,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)


# run the application
#frame.mainloop()


if path:
    # Make the path relative to the script's directory
    relative_path = os.path.relpath(path, script_directory)

    # Remove leading and trailing whitespace
    trimmed_path = relative_path.strip()

    print("Script Directory:", script_directory)
    print("Relative Path:",relative_path)
'''


path = " "

# run the application
frame.mainloop()

# Now, you can use the 'path' variable after the mainloop, and it will be updated when the "Scan" button is clicked.
print(path)

#Read image
img = cv2.imread(path, cv2.IMREAD_COLOR)

#Rotate image
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

#Resizing image
copia = img
copia = cv2.resize(copia,(1000,700),interpolation = cv2.INTER_AREA)
cv2.imshow("resized", copia)
cv2.waitKey(0)

'''#Aumentamos contraste
gamma = 25
lookUpTable = np.empty((1,256),np.uint8)
for i in range(256):
    lookUpTable[0,i] = np.clip(pow(i/255.0,gamma)*255.0,0,255)
copia = cv2.LUT(copia, lookUpTable)
cv2.imshow('img contrastada', copia)
cv2.waitKey(0)'''


#RGB split
b, g , r  = cv2.split(copia)
enhanced_green = cv2.equalizeHist(g)
# Merge the channels back
enhanced_image = cv2.merge([b, enhanced_green, r])
# Display the original and enhanced images
cv2.imshow('Enhanced Image', enhanced_image)
cv2.waitKey(0)

#Thresholding
_,th = cv2.threshold(enhanced_green,150,255, cv2.THRESH_BINARY_INV)
cv2.imshow("binary", th)
cv2.waitKey(0)

#Umbralizacion de pixeles
'''
_, thresh1 = cv2.threshold(g2, 79, 255, cv2.THRESH_BINARY_INV)
thresh1 = cv2.medianBlur(thresh1,5,0)
thresh1 = cv2.Canny(thresh1, 10, 60)
thresh1 = cv2.dilate(thresh1, (3,3), iterations=1)
'''

#cv2.imshow('Binary Threshold', thresh1)

'''hist = cv2.calcHist([g2], [0], None, [256], [0, 256])
plt.plot(hist, color='gray' )

plt.xlabel('intensidad de iluminacion')
plt.ylabel('cantidad de pixeles')
plt.show()'''


#Bluring image
g2 = cv2.medianBlur(g2,5)

#Border detection
g2 = cv2.Canny(g2,0,20)

#Border dilation and erode
g2 = cv2.dilate(g2, None, iterations=1)
g2 = cv2.erode(g2, None, iterations=1)

#rows = g2.shape[0]
detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 20, minRadius = 8, maxRadius = 29)
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



###########################################################################
'''
detected_circles = cv2.HoughCircles(g2,cv2.HOUGH_GRADIENT, 1, 20, param1 = 100, param2 = 35, minRadius = 2, maxRadius = 29)
count = 0

if detected_circles is not None:

    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]

        cv2.circle(copia, (a,b), r, (0, 0, 255), 2)

        cv2.circle(copia, (a,b), 1, (0, 0, 255), 3)
        count += 1
        cv2.imshow("Circles", copia)

'''
#**************************************************
'''
detected_circles2 = cv2.HoughCircles(thresh1,cv2.HOUGH_GRADIENT,1,20, param1 = 100, param2 = 22, minRadius = 2, maxRadius = 26) 

count2 = 0

if detected_circles2 is not None:
    detected_circles2 = np.uint16(np.around(detected_circles2))

    for pt in detected_circles2[0, :]:
        a, b,r = pt[0], pt[1], pt[2]

        cv2.circle(copia, (a,b), r, (255,0,0),2)

        cv2.circle(copia, (a,b),1,(255,0,0),3)

        cv2.imshow("Circles", copia)
'''
#*************************************************************************************************************

#Finding contours
#_,cnts = cv2.findContours(g2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#Drwaing contours
#for c in cnts:
#    epsilon = 0.01 * cv2.arcLength(c,True)
#    approx = cv2.approxPolyDP(c,epsilon,True)
    
#***************************************************************************************************************

#Displaying image
#cv2.imshow('image',copia)
#cv2.imshow('Green', g2)
print(count)
cv2.waitKey(0)
cv2.destroyAllWindows()
