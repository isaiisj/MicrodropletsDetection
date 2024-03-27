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

# Función para mostrar el número de gotas
def show_variable(variable_value):
    root = tk.Tk()
    root.withdraw()
    showinfo("Total droplets", f"Number of droplets: {variable_value}")

# Función para mostrar la relación entre las gotas
def show_ratio(variable_value):
    root = tk.Tk()
    root.withdraw()
    showinfo("Ratio", f"Ratio of droplets: {variable_value}")

# Clase para seleccionar la imagen
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

        self.select_button = tk.Button(master, text="Select Image", command=self.select_image, font="Helvetica 12", width=35, height=3)
        self.select_button.pack(pady=10)

        self.selected_image_path = None

    def select_image(self):
        image_path = fd.askopenfilename(title="Select an image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if image_path:
            relative_path = os.path.relpath(image_path)
            self.image_path_var.set(relative_path)
            self.selected_image_path = relative_path

# Inicializar la aplicación Tkinter
root = tk.Tk()
app = ImageSelectorApp(root)
root.mainloop()

# Verificar si se seleccionó una imagen
path = app.selected_image_path
if not path:
    print("No image selected.")
    exit()

# Leer la imagen
img = cv2.imread(path, cv2.IMREAD_COLOR)
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
copia = cv2.resize(img, (1000, 700), interpolation=cv2.INTER_AREA)

# Separar en canales RGB y aumentar el contraste del canal verde
b, g, r = cv2.split(copia)
enhanced_green = cv2.equalizeHist(g)
enhanced_image = cv2.merge([b, enhanced_green, r])
cv2.imshow("Original", copia)
cv2.waitKey(0)
# Umbralizar
_, th = cv2.threshold(enhanced_green, 150, 255, cv2.THRESH_BINARY)

# Difuminar
g2 = cv2.medianBlur(th, 3)

# Detección de bordes
g2 = cv2.Canny(g2, 0, 10)
g2 = cv2.dilate(g2, None, iterations=1)
g2 = cv2.erode(g2, None, iterations=1)

# HoughCircles para detectar gotas
detected_circles = cv2.HoughCircles(g2, cv2.HOUGH_GRADIENT, 1, 20, param1=100, param2=6, minRadius=5, maxRadius=12)
count = 0
tonalidades = []

if detected_circles is not None:
    detected_circles = np.uint16(np.around(detected_circles))

    for pt in detected_circles[0, :]:
        a, b, r = pt[0], pt[1], pt[2]
        cv2.circle(copia, (a, b), r, (0, 255, 0), 2)
        cv2.circle(copia, (a, b), 1, (0, 0, 255), 3)
        count += 1

        # Obtener la tonalidad de la gota
        tonalidad = np.mean(copia[b - r:b + r, a - r:a + r])
        tonalidades.append(tonalidad)

# Calcular el ratio de gotas para mostrar
count2 = len(tonalidades)
ratio = count / count2

# Mostrar la imagen con las gotas detectadas
cv2.imshow("Detected Droplets", copia)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Mostrar el número de gotas y el ratio
show_variable(count)
show_variable(count2)
show_ratio(ratio)

# Graficar la dispersión de las tonalidades
plt.figure()
plt.scatter(range(1, count2 + 1), tonalidades, color='green')
plt.title('Tonalidades de las Gotas')
plt.xlabel('Número de Gota')
plt.ylabel('Tonalidad')
plt.grid(True)
plt.show()
