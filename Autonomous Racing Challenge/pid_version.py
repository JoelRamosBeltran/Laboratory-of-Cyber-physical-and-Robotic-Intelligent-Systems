import WebGUI
import HAL
import time
import cv2

i = 0

KP_CURVA = 0.0075
KP_RECTA = 0.0105
KD = 0.025
KI = 0.00002
I_TERM_MAX = 25.0

UMBRAL_ERROR = 80
err_prev = 0.0
err_sum = 0.0
t_prev = time.time()
err_filtro = 0.0

V_MAX = 8.0
V_MIN = 2.0
IMG_ANCHO_MEDIO = 320.0
W_MAX = 1.5

# --- BUCLE PRINCIPAL ---
while True:
    img = HAL.getImage()
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Detección de color rojo
    red_mask = cv2.inRange(hsv, (0,120,120), (25,255,255))
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
    else:
        M = {"m00": 0, "m10": 0, "m01": 0}

    if M["m00"] != 0:
        cX = M["m10"] / M["m00"]
        cY = M["m01"] / M["m00"]
    else:
        cX, cY = 0, 0

    if cX > 0:
        err = IMG_ANCHO_MEDIO - cX

        alfa = 0.6
        err_filtro = alfa * err + (1 - alfa) * err_prev

        t = time.time()
        der_t = t - t_prev

        if der_t > 0:
            der_err = (err_filtro - err_prev) / der_t
            err_sum += err_filtro
            err_sum = max(min(err_sum, I_TERM_MAX), -I_TERM_MAX)
        else:
            der_err = 0.0

        error_norm = abs(err_filtro) / IMG_ANCHO_MEDIO
        velocidad = V_MAX - (V_MAX - V_MIN) * (error_norm ** 0.7)
        velocidad = max(velocidad, V_MIN)
        HAL.setV(velocidad)

        if abs(err_filtro) > UMBRAL_ERROR:
            Kp = KP_CURVA
        else:
            Kp = KP_RECTA

        W = (Kp * err_filtro) + (KI * err_sum) + (KD * der_err)
        W = max(min(W, W_MAX), -W_MAX)
        HAL.setW(W)

        err_prev = err_filtro
        t_prev = t

    WebGUI.showImage(img)
    i += 1
