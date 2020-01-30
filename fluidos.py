# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 22:33:25 2020

@author: Caro
"""
#Codigo para usar en la practica de fluidos
#%%
#Primera forma
#Metodo para trackear un objeto a partir de su color
#%%
import numpy as np
import cv2
#%%
#Defino funciones utiles para capturar video e imagenes

def testVideo():  
    cap = cv2.VideoCapture(0)
    while(True):
        # Capturo frame por frame
        ret, frame = cap.read()
        #Muestro el frame resultante
        cv2.imshow('frame',frame) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Cuando todo este listo, realizo la captura
    cap.release()
    cv2.destroyAllWindows()
    
def takeFoto(): 
    cap = cv2.VideoCapture(0)
    salir = False
    foto = False   

    while (not salir):
        # Capturar frame por frame
        ret, frame = cap.read()
        #Muestro el frame resultante
        cv2.imshow('Presione f para tomar foto',frame)
        key = cv2.waitKey(1)
        if not key == -1 :
            if key == ord('q'):
                salir = True
            if key == ord('f'):
                salir = True
                foto = True
    cap.release()
    cv2.destroyAllWindows()   

    if foto:
        return frame


#Paso a escala de grisis
def showresta(imagen,color,gris=False,tolerancia=20,destroy=False):
    imagen = np.int16(imagen)
    color = np.int16(color)
    mostrar = np.zeros(imagen.shape,np.int16)
    mostrar[:,:,0] = imagen[:,:,0] - color[0]
    mostrar[:,:,1] = imagen[:,:,1] - color[1]
    mostrar[:,:,2] = imagen[:,:,2] - color[2]
    mostrar = np.abs(mostrar)
    mostrar = np.uint8(mostrar)
    if gris:
        tituloVentana = 'Imagen al restar color'
        cv2.destroyWindow(tituloVentana)
        cv2.namedWindow(tituloVentana)
        cv2.imshow(tituloVentana, mostrar)
    mostrar[:,:,0] = (mostrar[:,:,0] < tolerancia) * 255 
    mostrar[:,:,1] = (mostrar[:,:,1] < tolerancia) * 255 
    mostrar[:,:,2] = (mostrar[:,:,2] < tolerancia) * 255 
    tituloVentana = 'Imagen binarizada'
    if destroy:
        cv2.destroyWindow(tituloVentana)
        cv2.namedWindow(tituloVentana)
    cv2.imshow(tituloVentana, mostrar)

    
def mainrutine(umbral=20):

    # Definimos parametros y cosas para el recorte
    refPt = []
    cropping = False
    lastPosition = None
    ventanaRecorte = 'Recorte'
    title = 'Seleccione la zona con el color a reconocer'
    ventanaColor = 'Color promedio seleccionado'
    sizeColor = (100,100,3)
    color = None
    colorchange = False

    

    def windowsEvents(event, x, y, flags, param):
        nonlocal refPt
        nonlocal cropping
        nonlocal lastPosition
        nonlocal image
        nonlocal bkp
        nonlocal color
        nonlocal colorchange

        #  Si se presiona el boton izquierdo del mouse, comienza a grabar
        # las coordendas (x, y) e indica que el recorte se esta realizando
        if event == cv2.EVENT_LBUTTONDBLCLK:
            # Hacemos el color y lo mostramos
            colorshow = np.zeros(sizeColor,np.uint8)
            color = image[y,x]
            colorchange = True
            colorshow[:,:,:] = image[y,x]
            cv2.destroyWindow(ventanaColor)
            cv2.namedWindow(ventanaColor)
            cv2.imshow(ventanaColor, colorshow)       

        elif event == cv2.EVENT_LBUTTONDOWN:
            refPt = [(x, y)]
            cropping = True 

        #Chequear si se apreto el boton izquierdo
        elif event == cv2.EVENT_LBUTTONUP:
            # Se graba las coordenadas (x,y) finales e indica que el recorte fue finalizado
            refPt.append((x, y))
            cropping = False
            image = bkp.copy()
            cv2.imshow(title, image)

                     

            # Calculamos la zona a recortar
            xstart = min(refPt[0][0],refPt[1][0])
            xend = max(refPt[0][0],refPt[1][0])
            ystart = min(refPt[0][1],refPt[1][1])
            yend = max(refPt[0][1],refPt[1][1])          

            # Hacemos el recorte y lo mostramos
            recorte = image[ystart:yend,xstart:xend]
            if len(recorte):
                cv2.destroyWindow(ventanaRecorte)
                cv2.namedWindow(ventanaRecorte)
                cv2.imshow(ventanaRecorte, recorte)
                
                # Hacemos el color medio y lo mostramos

                colorshow = np.zeros(sizeColor,np.uint8)
                colorshow[:,:,0] = np.average(recorte[:,:,0])
                colorshow[:,:,1] = np.average(recorte[:,:,1])
                colorshow[:,:,2] = np.average(recorte[:,:,2])
                color = colorshow[0,0]
                colorchange = True
                cv2.destroyWindow(ventanaColor)
                cv2.namedWindow(ventanaColor)
                cv2.imshow(ventanaColor, colorshow)

        elif event == cv2.EVENT_MOUSEMOVE:
            lastPosition = (x,y)            

    # tomamos una foto
    image = takeFoto()
    if image is None:
        return
    bkp=image.copy()   

    # La mostramos
    cv2.namedWindow(title)
    cv2.setMouseCallback(title, windowsEvents)
    cv2.imshow(title, image)
  

    # Iniciamos el loop de seleccion de color

    salir = False
    video = False
    while (not salir):
        key = cv2.waitKey(1)
        if key == ord('q'):
            salir = True
        if cropping:
            image = cv2.rectangle(bkp.copy(), refPt[0], lastPosition, (0, 255, 0), 2)
            cv2.imshow(title, image)
        if colorchange:
            print ('cucu')
            showresta(image.copy(),color.copy(),tolerancia=umbral,gris=True)
            colorchange=False
        if key == ord('s'):
            salir = True
            video = True
    cv2.destroyAllWindows()    

    if video:
        # inicializamos el modo video
        cap = cv2.VideoCapture(0)
        salir = False
        while (not salir):
            key = cv2.waitKey(1)
            if key == ord('q'):
                salir = True
                
            # Capturar frame por frame
            ret, frame = cap.read()
            showresta(frame.copy(),color.copy(),tolerancia=umbral,gris=False)
            
        cap.release()
        cv2.destroyAllWindows()

#%%
#Segunda forma a partir de PIV
#%%
#PAGINAS UTILES

# https://github.com/OpenPIV/openpiv-python
#http://www.openpiv.net/openpiv-python/
#https://pivlab.blogspot.com/p/blog-page_19.html
#https://nbviewer.jupyter.org/github/OpenPIV/openpiv-python/blob/master/openpiv/examples/notebooks/tutorial_multipass.ipynb


#%%
#VER UTILMO ENLACE 



