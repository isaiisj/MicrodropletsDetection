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

import cv2
import numpy as np
from matplotlib import pyplot as plt
import tkinter as tk
from tkinter import ttk
import os
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from scipy import fftpack
import imutils
from PIL import Image,ImageTk

def show_variable(variable_value):
    showinfo("Total droplets", f"Number of droplets: {variable_value}")

def show_ratio(variable_value):
    showinfo("Ratio", f"Ratio of droplets: {variable_value}")

def update_canny_low(value):
    global low_threshold
    low_threshold = value
    apply_canny()

def apply_canny():
    global image, low_threshold

    if image is not None:
        b, g, r = cv2.split(image)
        #enhanced_green = cv2.equalizeHist(g)
        alpha = 1.9
        beta = 0
        enhanced_green = cv2.convertScaleAbs(g, alpha=alpha, beta=beta)
    
        _, th = cv2.threshold(enhanced_green, int(low_threshold), 255, cv2.THRESH_BINARY)#Parametro importante umbral menor
        g2 = cv2.medianBlur(th, 3)
        g2 = cv2.Canny(g2, 0, 10)
        g2 = cv2.dilate(g2, None, iterations=1)
        g2 = cv2.erode(g2, None, iterations=1)

        detected_circles = cv2.HoughCircles(g2, cv2.HOUGH_GRADIENT, 1, 25, param1=100, param2=7 , minRadius=5, maxRadius=10) #parametro importante

        count = 0
        tonalidades = []
        
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                cv2.circle(image, (a,b), r, (0, 255, 0), 2)
                #count += 1
                #cv2.imshow("All", image)

                #Obtener la tonalidad de la gota
                #tonalidad = np.mean(image[b - r:b + r, a - r:a + r])
                #tonalidades.append(tonalidad)

        #imageToShowOutput = cv2.imshow(g2)

        g2 = Image.fromarray(image)
        img = ImageTk.PhotoImage(image=g2)
        lblOutputImage.configure(image=img)
        lblOutputImage.image = img

        lblInfo3 = tk.Label(root, text="Salida", font="bold")
        lblInfo3.grid(column=1,row=0,padx=5,pady=5)


def elegir_imagen():
    #Files types
    path_image = fd.askopenfilename(filetypes=[("image",".jpg"),
                                                       ("image",".jpeg"),
                                                       ("image",".png")])
    
    if len(path_image) > 0:
        global image

        #Read input image
        image = cv2.imread(path_image)
        image = imutils.resize(image, height=380)
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

        #Para visualizar la imagen
        imageToShow = imutils.resize(image, width=180)
        #imageToShow = cv2.cvtColor(imageToShow, cv2.COLOR_BGR2RGB)
        im = Image.fromarray(imageToShow)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img

        lblInfo1 = tk.Label(root, text="Imagen de entrada")
        lblInfo1.grid(column=0,row=1,padx=5,pady=5)


image = None
low_threshold = 100


root = tk.Tk()

#Label of the input image 
lblInputImage = tk.Label(root)
lblInputImage.grid(column=0,row=2)

#LAbel of the output image
lblOutputImage = tk.Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=6)

lblInfo2 = tk.Label(root, text="Parámetros", width=25)
lblInfo2.grid(column=0, row=3, padx=5, pady=5)


w = tk.Scale(root, from_=0, to=254,tickinterval=10, orient=tk.HORIZONTAL, command=update_canny_low)
w.set(low_threshold)
w.grid(column=0, row=3, padx=5, pady=5)

#create the button for the selected image
btn = tk.Button(root,text="Choose image", width=25, command=elegir_imagen)
btn.grid(column=0,row=0,padx=5,pady=5)

root.mainloop()





#img = cv2.imread(path, cv2.IMREAD_COLOR)
#img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
#copia = cv2.resize(img, (1000, 700), interpolation=cv2.INTER_AREA)

#######################################################################33
    
'''

count3 = len(tonalidades)
print("El total de gotas es:", f"{count3}")

cv2.waitKey(0)
img2 = cv2.imread(path, cv2.IMREAD_COLOR)
img2 = cv2.rotate(img2, cv2.ROTATE_90_CLOCKWISE)
copia2 = cv2.resize(img2, (1000, 700), interpolation=cv2.INTER_AREA)

b3, g3 , r3  = cv2.split(copia2)
alpha = 1.9  # Contrast control (1.0-3.0)
beta = 0    # Brightness control (0-100)

g3 = cv2.convertScaleAbs(g3, alpha=alpha, beta=beta)
_, th2 = cv2.threshold(g3, 89, 255, cv2.THRESH_BINARY)

g4 = cv2.medianBlur(th2, 3)
g4 = cv2.Canny(g4, 0, 10)
g4 = cv2.dilate(g4, None, iterations=1)
g4 = cv2.erode(g4, None, iterations=1)
#cv2.imshow("Alpha & Beta Control", g4)
#cv2.waitKey(0)

detected_circles3 = cv2.HoughCircles(g4, cv2.HOUGH_GRADIENT, 1, 15, param1=100, param2=10, minRadius=10, maxRadius=25)

count2 = 0
if detected_circles3 is not None:
    detected_circles3 = np.uint16(np.around(detected_circles3))

    for pt in detected_circles3[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        cv2.circle(copia2, (a,b), r, (243, 122, 245), 2)
        count2 += 1
        cv2.imshow("Positive", copia2)
    
    
ratio = count / count2 if count2 != 0 else 0

show_variable(count)
show_variable(count2)
show_ratio(ratio)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Graficar la dispersión de las tonalidades
threshold = 68
plt.figure()
plt.scatter(range(1, count3 + 1), tonalidades, color=['green' if y <= threshold else 'red' for y in tonalidades])
plt.title('Tonalidades de las Gotas')
plt.xlabel('Número de Gota')
plt.ylabel('Tonalidad')
plt.grid(True)
plt.show()

# Crear histograma de tonalidades
plt.figure()
# Definir umbrales para categorizar las tonalidades
umbral1 = 20
umbral2 = 70
    
# Separar tonalidades en diferentes categorías basadas en los umbrales
tonalidades_bajas = [tono for tono in tonalidades if tono <= umbral1]
tonalidades_medias = [tono for tono in tonalidades if umbral1 < tono <= umbral2]
tonalidades_altas = [tono for tono in tonalidades if tono > umbral2]
    
# Crear histogramas separados para cada categoría
plt.hist(tonalidades_bajas, bins=30, color='blue', alpha=0.5, label='Tonalidades Bajas')
plt.hist(tonalidades_medias, bins=30, color='green', alpha=0.5, label='Tonalidades Medias')
plt.hist(tonalidades_altas, bins=30, color='red', alpha=0.5, label='Tonalidades Altas')

plt.title('Histograma de Tonalidades de las Gotas')
plt.xlabel('Tonalidad')
plt.ylabel('Número de Gotas')
plt.legend()
plt.grid(True)
plt.show()
'''
