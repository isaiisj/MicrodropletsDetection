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
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo, showerror
import imutils
from PIL import Image, ImageTk
import openpyxl
from openpyxl import Workbook

param2_all = 6
param2_positive = 6
low_threshold_all = 50
low_threshold_positive = 111
min_radius_active = 19  # Valor inicial de Radio mínimo
max_radius_active = 22  # Valor inicial de Radio máximo

# Variables que se ajustan con los sliders
param2_active = param2_all
low_threshold_active = low_threshold_all

manual_circles_high = []
manual_circles_low = []
add_high_tone_circle = False
add_low_tone_circle = False
file_path = None

# Variables para control negativo
negative_control_image = None
negative_control_tonalidades = []
umbral_control = None
desviacion_estandar_control = None

def show_Total(variable_value):
    showinfo("Total droplets", f"Number of droplets: {variable_value}")

def show_ratio(variable_value):
    showinfo("Ratio", f"Ratio of droplets: {variable_value}")

def rotate_image():
    global image
    if image is not None:
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        display_image()

def display_image():
    if image is not None:
        imageToShow = imutils.resize(image, width=180)
        im = Image.fromarray(imageToShow)
        img = ImageTk.PhotoImage(image=im)
        lblOutputImage.configure(image=img)
        lblOutputImage.image = img
        apply_canny()

def apply_canny():
    global tonalidades
    global umbral_tonalidad
    global tonalidades_bajas, tonalidades_altas
    global detected_circles
    if image is not None:
        b, g, r = cv2.split(image)
        alpha = 1.9
        beta = 0
        enhanced_green = cv2.convertScaleAbs(g, alpha=alpha, beta=beta)

        # Suavizar la imagen para reducir el ruido
        blurred = cv2.GaussianBlur(enhanced_green, (9, 9), 2)

        # Aplicar la detección de bordes de Canny
        edges = cv2.Canny(blurred, low_threshold_active, low_threshold_active * 2)

        # Mejorar los bordes mediante dilatación y erosión
        edges = cv2.dilate(edges, None, iterations=2)
        edges = cv2.erode(edges, None, iterations=1)

        # Detección de círculos usando HoughCircles
        detected_circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                                            param1=50, param2=int(param2_active),
                                            minRadius=int(min_radius_active), maxRadius=int(max_radius_active))
        
        tonalidades = []
        result_image = image.copy()

        all_circles = []

        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                all_circles.append((pt[0], pt[1], pt[2]))

        for (a, b, r) in all_circles:
            y1, y2 = max(int(b) - int(r), 0), min(int(b) + int(r), image.shape[0])
            x1, x2 = max(int(a) - int(r), 0), min(int(a) + int(r), image.shape[1])
            if y2 > y1 and x2 > x1:
                sub_image = image[y1:y2, x1:x2]
                if sub_image.size > 0:
                    tonalidad = np.mean(sub_image)
                    if not np.isnan(tonalidad):
                        tonalidades.append(tonalidad)

        # Calcular y agregar tonalidades reales para círculos manuales
        for (x, y, r) in manual_circles_high + manual_circles_low:
            y1, y2 = max(int(y) - int(r), 0), min(int(y) + int(r), image.shape[0])
            x1, x2 = max(int(x) - int(r), 0), min(int(x) + int(r), image.shape[1])
            if y2 > y1 and x2 > x1:
                sub_image = image[y1:y2, x1:x2]
                if sub_image.size > 0:
                    tonalidad = np.mean(sub_image)
                    if not np.isnan(tonalidad):
                        tonalidades.append(tonalidad)

        # Utilizar el umbral del control negativo
        if umbral_control is not None:
            # Ajustar el umbral utilizando la desviación estándar
            umbral_tonalidad = umbral_control + 3 * desviacion_estandar_control
        elif len(tonalidades) > 0:
            if len(tonalidades) >= 2:
                # Aplicar K-means para encontrar el umbral
                tonalidades = np.array(tonalidades).reshape(-1, 1).astype(np.float32)
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
                k = 2
                _, labels, centers = cv2.kmeans(tonalidades, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
                centers = sorted(centers.flatten())
                umbral_tonalidad = sum(centers) / 2
            else:
                umbral_tonalidad = np.mean(tonalidades) + 10  # Umbral alternativo si hay menos de 2 tonos
        else:
            umbral_tonalidad = 0

        # Convertir tonalidades a un arreglo de NumPy y aplanarlo
        tonalidades = np.array(tonalidades).flatten()
        tonalidades_bajas = [tono for tono in tonalidades if tono <= umbral_tonalidad]
        tonalidades_altas = [tono for tono in tonalidades if tono > umbral_tonalidad]

        # Dibujar círculos detectados automáticamente
        for (a, b, r) in all_circles:
            tonalidad = np.mean(image[max(int(b) - int(r), 0):min(int(b) + int(r), image.shape[0]), max(int(a) - int(r), 0):min(int(a) + int(r), image.shape[1])])
            if tonalidad > umbral_tonalidad:
                cv2.circle(result_image, (a, b), r, (255, 0, 0), 2)  # rojo para círculos de tonalidad alta
            else:
                cv2.circle(result_image, (a, b), r, (0, 0, 255), 2)  # azul para círculos de tonalidad baja

        for (x, y, r) in manual_circles_high:
            cv2.circle(result_image, (x, y), r, (255, 0, 0), 2)  # rojo para círculos de tonalidad alta

        for (x, y, r) in manual_circles_low:
            cv2.circle(result_image, (x, y), r, (0, 0, 255), 2)  # azul para círculos de tonalidad baja

        # Actualizar etiquetas
        lblTonalidadesBajas.config(text=f"Negative droplets: {len(tonalidades_bajas)}")
        lblTonalidadesAltas.config(text=f"Positive droplets: {len(tonalidades_altas)}")

        # Añadir el texto en la imagen
        total_circles = len(tonalidades_bajas) + len(tonalidades_altas)
        text = f'Total de microgotas: {total_circles}'
        font_scale = 0.5
        thickness = 1
        color = (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX

        text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
        text_w, text_h = text_size
        pos_x = result_image.shape[1] - text_w - 10
        pos_y = result_image.shape[0] - 10

        cv2.putText(result_image, text, (pos_x, pos_y), font, font_scale, color, thickness)

        im = Image.fromarray(result_image)
        img = ImageTk.PhotoImage(image=im)

        lblOutputImage.configure(image=img)
        lblOutputImage.image = img

        print("El umbral de la tonalidad está en ", umbral_tonalidad)
        print("El número total de microgotas es: ", total_circles)
        print("Tonalidades bajas: ", len(tonalidades_bajas))
        print("Tonalidades altas: ", len(tonalidades_altas))

def plot_droplets():
    global tonalidades_bajas, tonalidades_altas
    if tonalidades_bajas or tonalidades_altas:
        plt.figure()
        y_bajas = np.arange(len(tonalidades_bajas))
        y_altas = np.arange(len(tonalidades_altas))
        y = np.concatenate((y_bajas, y_altas))
        x = np.concatenate((tonalidades_bajas, tonalidades_altas))
        colors = ['blue'] * len(tonalidades_bajas) + ['red'] * len(tonalidades_altas)
        plt.scatter(y, x, color=colors)
        plt.xlabel('Numero de gota')
        plt.ylabel('Tonalidad')
        plt.title('Distribución de Tonalidad de las Gotas Detectadas')
        plt.show()

        plt.hist(tonalidades_bajas, bins=30, color='blue', alpha=0.5, label='Tonalidades Bajas')
        plt.hist(tonalidades_altas, bins=30, color='red', alpha=0.5, label='Tonalidades Altas')
        plt.title('Histograma de Tonalidades de las Gotas')
        plt.xlabel('Tonalidad')
        plt.ylabel('Número de Gotas')
        plt.legend()
        plt.grid(True)
        plt.show()

    else:
        showinfo("Info", "No hay datos de tonalidades para mostrar.")

def update_params(value):
    global low_threshold_active, param2_active, min_radius_active, max_radius_active
    low_threshold_active = w.get()
    param2_active = x.get()
    min_radius_active = y_slider.get()
    max_radius_active = z_slider.get()
    apply_canny()

def set_all_droplets():
    global param2_active, low_threshold_active, min_radius_active, max_radius_active
    param2_active = param2_all
    low_threshold_active = low_threshold_all
    min_radius_active = 19
    max_radius_active = 22
    w.set(low_threshold_all)
    x.set(param2_all)
    y_slider.set(19)
    z_slider.set(22)
    apply_canny()

def set_positive_droplets():
    global param2_active, low_threshold_active, min_radius_active, max_radius_active
    param2_active = param2_positive
    low_threshold_active = low_threshold_positive
    min_radius_active = 19
    max_radius_active = 22
    w.set(low_threshold_positive)
    x.set(param2_positive)
    y_slider.set(19)
    z_slider.set(22)
    apply_canny()

def elegir_imagen():
    path_image = fd.askopenfilename(filetypes=[("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")])
    if len(path_image) > 0:
        global image
        image = cv2.imread(path_image)
        image = imutils.resize(image, height=600)
        display_image()

        imageToShow = imutils.resize(image, width=180)
        im = Image.fromarray(imageToShow)
        img = ImageTk.PhotoImage(image=im)

        lblInputImage.configure(image=img)
        lblInputImage.image = img
        apply_canny()

def elegir_imagen_control():
    path_image = fd.askopenfilename(filetypes=[("image", ".jpg"), ("image", ".jpeg"), ("image", ".png")])
    if len(path_image) > 0:
        global negative_control_image, negative_control_tonalidades, umbral_control, desviacion_estandar_control
        negative_control_image = cv2.imread(path_image)
        negative_control_image = imutils.resize(negative_control_image, height=600)
        
        # Calcular tonalidades del control negativo
        b, g, r = cv2.split(negative_control_image)
        alpha = 1.9
        beta = 0
        enhanced_green = cv2.convertScaleAbs(g, alpha=alpha, beta=beta)
        blurred = cv2.GaussianBlur(enhanced_green, (9, 9), 2)
        edges = cv2.Canny(blurred, low_threshold_all, low_threshold_all * 2)
        edges = cv2.dilate(edges, None, iterations=2)
        edges = cv2.erode(edges, None, iterations=1)
        detected_circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, 1, 20,
                                            param1=50, param2=int(param2_all),
                                            minRadius=int(min_radius_active), maxRadius=int(max_radius_active))
        
        negative_control_tonalidades = []
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]
                y1, y2 = max(int(b) - int(r), 0), min(int(b) + int(r), negative_control_image.shape[0])
                x1, x2 = max(int(a) - int(r), 0), min(int(a) + int(r), negative_control_image.shape[1])
                if y2 > y1 and x2 > x1:
                    sub_image = negative_control_image[y1:y2, x1:x2]
                    if sub_image.size > 0:
                        tonalidad = np.mean(sub_image)
                        if not np.isnan(tonalidad):
                            negative_control_tonalidades.append(tonalidad)
        if len(negative_control_tonalidades) > 0:
            umbral_control = np.mean(negative_control_tonalidades)
            desviacion_estandar_control = np.std(negative_control_tonalidades)
            showinfo("Control Negativo", f"Control negativo cargado con {len(negative_control_tonalidades)} tonalidades.")
        else:
            umbral_control = None
            desviacion_estandar_control = None
            showerror("Error", "No se detectaron gotitas en el control negativo.")

def add_or_remove_circle(event):
    global manual_circles_high, manual_circles_low, detected_circles, add_high_tone_circle, add_low_tone_circle
    x, y = event.x, event.y
    min_radius = y_slider.get()
    max_radius = z_slider.get()
    radius = (min_radius + max_radius) // 2
    if event.num == 3:  # Clic derecho para agregar
        if add_high_tone_circle:
            manual_circles_high.append((x, y, radius))  # Agregar círculo con tonalidad alta
        elif add_low_tone_circle:
            manual_circles_low.append((x, y, radius))  # Agregar círculo con tonalidad baja
        apply_canny()
    elif event.num == 1:  # Clic izquierdo para eliminar
        for circle in manual_circles_high:
            cx, cy, r = circle
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                manual_circles_high.remove(circle)
                apply_canny()
                return
        for circle in manual_circles_low:
            cx, cy, r = circle
            if (x - cx) ** 2 + (y - cy) ** 2 <= r ** 2:
                manual_circles_low.remove(circle)
                apply_canny()
                return
        if detected_circles is not None:
            for i, pt in enumerate(detected_circles[0, :]):
                a, b, r = pt[0], pt[1], pt[2]
                if (x - a) ** 2 + (y - b) ** 2 <= r ** 2:
                    detected_circles = np.delete(detected_circles, i, axis=1)
                    apply_canny()
                    return

def toggle_high_tone_circle():
    global add_high_tone_circle, add_low_tone_circle
    add_high_tone_circle = True
    add_low_tone_circle = False
    btn_high_tone_circle.config(relief=tk.SUNKEN)
    btn_low_tone_circle.config(relief=tk.RAISED)

def toggle_low_tone_circle():
    global add_high_tone_circle, add_low_tone_circle
    add_high_tone_circle = False
    add_low_tone_circle = True
    btn_high_tone_circle.config(relief=tk.RAISED)
    btn_low_tone_circle.config(relief=tk.SUNKEN)

def reset_manual_circles():
    global manual_circles_high, manual_circles_low
    manual_circles_high = []
    manual_circles_low = []
    apply_canny()

def save_to_excel():
    global file_path
    if file_path is None:
        file_path = fd.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", ".xlsx")])
        if not file_path:
            return
        workbook = Workbook()
        sheet = workbook.active
        sheet.append(["Total de Gotitas", "Gotitas Positivas", "Gotitas Negativas", "Umbral de Tonalidad"])
    else:
        try:
            workbook = openpyxl.load_workbook(file_path)
            sheet = workbook.active
        except Exception as e:
            showerror("Error", f"Error al abrir el archivo: {e}")
            return

    total_droplets = len(tonalidades_bajas) + len(tonalidades_altas)
    positive_droplets = len(tonalidades_altas)
    negative_droplets = len(tonalidades_bajas)
    sheet.append([total_droplets, positive_droplets, negative_droplets, umbral_tonalidad])
    
    try:
        workbook.save(file_path)
        showinfo("Información guardada", "Los datos han sido guardados exitosamente.")
    except PermissionError:
        showerror("Error", "Permiso denegado: No se pudo guardar el archivo. Asegúrate de que el archivo no esté abierto en otra aplicación y que tienes permisos de escritura en el directorio.")

def choose_excel_file():
    global file_path
    path = fd.askopenfilename(filetypes=[("Excel files", ".xlsx")])
    if path:
        file_path = path
        showinfo("Archivo seleccionado", f"Archivo seleccionado: {file_path}")

image = None
detected_circles = None
tonalidades_bajas = []
tonalidades_altas = []
file_path = None

root = tk.Tk()

lblInputImage = tk.Label(root)
lblInputImage.grid(column=0, row=2)

lblOutputImage = tk.Label(root)
lblOutputImage.grid(column=1, row=1, rowspan=12)
lblOutputImage.bind("<Button-1>", add_or_remove_circle)
lblOutputImage.bind("<Button-3>", add_or_remove_circle)

btn_rotate = tk.Button(root, text="Rotate Image", command=rotate_image)
btn_rotate.grid(column=1, row=0)

btn = tk.Button(root, text="Choose image", width=25, command=elegir_imagen)
btn.grid(column=0, row=0, padx=5, pady=5)

btn_control = tk.Button(root, text="Choose control image", width=25, command=elegir_imagen_control)
btn_control.grid(column=0, row=1, padx=5, pady=5)

w = tk.Scale(root, from_=0, to=254, resolution=1, orient=tk.HORIZONTAL, label="Umbral", command=update_params)
w.set(low_threshold_active)
w.grid(column=0, row=3, padx=5, pady=5)

x = tk.Scale(root, from_=1, to=30, resolution=1, orient=tk.HORIZONTAL, label="Sensibilidad de detección", command=update_params)
x.set(param2_active)
x.grid(column=0, row=4, padx=5, pady=5)

y_slider = tk.Scale(root, from_=0, to=100, resolution=1, orient=tk.HORIZONTAL, label="Radio mínimo", command=update_params)
y_slider.set(min_radius_active)
y_slider.grid(column=2, row=1, padx=5, pady=5)

z_slider = tk.Scale(root, from_=0, to=200, resolution=1, orient=tk.HORIZONTAL, label="Radio máximo", command=update_params)
z_slider.set(max_radius_active)
z_slider.grid(column=2, row=2, padx=5, pady=5)

btn_all = tk.Button(root, text="All Droplets", command=set_all_droplets)
btn_all.grid(column=0, row=5, padx=5, pady=5)

btn_positive = tk.Button(root, text="Positive Droplets", command=set_positive_droplets)
btn_positive.grid(column=0, row=6, padx=5, pady=5)

btn_plot = tk.Button(root, text="Plot Droplets", width=25, command=plot_droplets)
btn_plot.grid(column=0, row=7, padx=5, pady=5)

btn_save = tk.Button(root, text="Save to Excel", command=save_to_excel)
btn_save.grid(column=2, row=8, padx=5, pady=5)

btn_choose_excel = tk.Button(root, text="Choose Excel File", command=choose_excel_file)
btn_choose_excel.grid(column=2, row=9, padx=5, pady=5)

# Añadir etiquetas para mostrar tonalidades bajas y altas
lblTonalidadesBajas = tk.Label(root, text="Negative Droplets: 0")
lblTonalidadesBajas.grid(column=2, row=3, padx=5, pady=5)

lblTonalidadesAltas = tk.Label(root, text="Positive Droplets: 0")
lblTonalidadesAltas.grid(column=2, row=4, padx=5, pady=5)

# Botones para agregar círculos manualmente
btn_high_tone_circle = tk.Button(root, text="Add Positive Droplet", command=toggle_high_tone_circle)
btn_high_tone_circle.grid(column=2, row=5, padx=5, pady=5)

btn_low_tone_circle = tk.Button(root, text="Add Negative Droplet", command=toggle_low_tone_circle)
btn_low_tone_circle.grid(column=2, row=6, padx=5, pady=5)

# Botón de reset
btn_reset = tk.Button(root, text="Reset", command=reset_manual_circles)
btn_reset.grid(column=2, row=7, padx=5, pady=5, sticky="se")

root.mainloop()
