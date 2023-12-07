import cv2
import numpy as np
from matplotlib import pyplot as plt

path = input("Introduce la ruta de la imagen: ")

#Read image
img = cv2.imread(path, cv2.IMREAD_COLOR)

#Rotate image
img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

#Resizing image
copia = img
copia = cv2.resize(copia,(900,700),interpolation = cv2.INTER_AREA)

#RGB split
b, g , r  = cv2.split(img)
b2 = cv2.resize(b,(900,700),interpolation = cv2.INTER_AREA)
g2 = cv2.resize(g,(900,700),interpolation = cv2.INTER_AREA)
r2 = cv2.resize(r,(900,700),interpolation = cv2.INTER_AREA)

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