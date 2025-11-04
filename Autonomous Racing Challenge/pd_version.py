import WebGUI
import HAL
import time

import cv2

i = 0
KP_CURVA = 0.007
KP_RECTA = 0.005
UMBRAL_ERROR = 100
KD = 0.05
err_prev = 0
t_prev = time.time()

while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsv, 
                            (0,125,125),
                            (30,255,255))
    contours, hierarchy = cv2.findContours(red_mask, 
                                            cv2.RETR_TREE, 
                                            cv2.CHAIN_APPROX_SIMPLE)
    
    M = cv2.moments(contours[0])
        # --- Constantes que debes ajustar ---
    V_MAX = 8.0  # Velocidad máxima en rectas
    V_MIN = 3.0  # Velocidad mínima en curvas cerradas
    IMG_ANCHO_MEDIO = 320.0 # Asumiendo imagen de 640px

    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    else:
        cX, cY = 0,0

    if cX > 0:
        err = IMG_ANCHO_MEDIO - cX
        t = time.time()

        der_err = err - err_prev
        der_t = t - t_prev
        
        error_norm = abs(err) / IMG_ANCHO_MEDIO 
        
        velocidad = V_MAX - (V_MAX - V_MIN) * error_norm
        
        # Asegurarnos de que nunca sea menor que V_MIN
        velocidad = max(velocidad, V_MIN) 
        
        HAL.setV(velocidad)

        if abs(err) > UMBRAL_ERROR:
            Kp = KP_CURVA
        else:
            Kp = KP_RECTA
        HAL.setW(Kp * err + KD * der_err) # ¡Ganancia variable!

        err_prev = err
        t_prev = t

    WebGUI.showImage(img)
    print('%d cX: %.2f cY: %.2f' % (i, cX,cY))
    i = i + 1
