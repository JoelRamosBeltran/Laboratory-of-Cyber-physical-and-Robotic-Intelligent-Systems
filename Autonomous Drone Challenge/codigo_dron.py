import WebGUI
import HAL
import Frequency
import math
import cv2
# Enter sequential code!


x_personas = [30,40]
y_personas = [-40,-30]

actual_x = 0
actual_y = 0

altura = 3

vx = 10
vy = 0
vz = 0
vz_raw = 0

kp_z = 1.2       # fuerte para que no se hunda
kd_z = 0.1        # suaviza sin quitar fuerza
max_vz = 1.2      # permite corregir rápido
dead_zone = 0.05    # Error pequeño donde no actuamos (evita jitter)

prev_error_z = 0

umbral = 0.2 #umbral de cercanía


x_obj = (abs(x_personas[0] - x_personas[1])/2) + x_personas[0]
y_obj = (abs(y_personas[0] - y_personas[1])/2) + y_personas[0]

xy_obj = (abs((x_obj-actual_x) ** 2 + (y_obj-actual_y) ** 2) ** (1/2))


yaw_obj = math.atan2(y_obj,x_obj)

#r = r_ant + step_dist * ang / (2 * math.pi)

original_pos = HAL.get_position()

HAL.takeoff(altura)

while( abs(HAL.get_yaw()) < abs(yaw_obj)):
    HAL.set_cmd_pos(0, 0, altura, yaw_obj)

while(xy_obj > 5):

    actual_pos = HAL.get_position()
    actual_x, actual_y, actual_z = actual_pos

    x_obj = (abs(x_personas[0] - x_personas[1]) / 2) + x_personas[0]
    y_obj = (abs(y_personas[0] - y_personas[1]) / 2) + y_personas[0]

    xy_obj = ((x_obj - actual_x)**2 + (y_obj - actual_y)**2)**0.5

    #----------------

    error_z = altura - actual_z
    d_error_z = error_z - prev_error_z
    prev_error_z = error_z

    if abs(error_z) < dead_zone:
        vz_raw = 0
    else:
        vz_raw = kp_z * error_z + kd_z * d_error_z

    vz = max(-max_vz, min(max_vz, vz_raw))

    #----------------

    HAL.set_cmd_vel(vx, vy, vz, 0)

    img_f = HAL.get_frontal_image()
    img_v = HAL.get_ventral_image()

    WebGUI.showImage(img_f)
    WebGUI.showLeftImage(img_v)


while True:
   # Enter iterative code!


   actual_pos = HAL.get_position()
   actual_yaw = HAL.get_yaw()

   HAL.set_cmd_pos(x_obj, y_obj, 4, yaw_obj)

   img_f = HAL.get_frontal_image()
   img_v = HAL.get_ventral_image()


   WebGUI.showImage(img_f)
   WebGUI.showLeftImage(img_v)

   x_actual, y_actual, _ = HAL.get_position()

   # Verificar si llegó al objetivo
   dist = math.sqrt((x_actual - x_obj)**2 + (y_actual - y_obj)**2)

   Frequency.tick()

   if (dist < umbral):
    print("Llegó a su destino")
    break




faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def cara_ya_detectada(pos_nueva, dict_caras, umbral=3.2):
    for id_cara, pos_guardada in dict_caras.items():
        dx = pos_nueva[0] - pos_guardada[0]
        dy = pos_nueva[1] - pos_guardada[1]
        dist = (dx*dx + dy*dy)**0.5
        if dist < umbral:
            return True   # Ya está registrada
    return False          # Es una nueva cara

def detectar_superviviente(img_v, dict_caras, pos_actual):
    detectado = False
    for angle in [0,45,-45,90,-90,135,-135,180]:
        height, width = img_v.shape[:2]
        rotationCenter = (width/2, height/2)
        rotationMatrix = cv2.getRotationMatrix2D(rotationCenter,angle,1)
        rotatedV = cv2.warpAffine(img_v, rotationMatrix, (width,height))
        rotatedGray = cv2.cvtColor(rotatedV, cv2.COLOR_BGR2GRAY)
        WebGUI.showImage(rotatedGray)
        faces = faceCascade.detectMultiScale(rotatedGray,scaleFactor=1.02, minNeighbors=2)
        
        for i in range(len(faces)):
            x_global = pos_actual[0]
            y_global = pos_actual[1]
            pos_cara = (x_global, y_global)
            # --- Comprobación ---
            if not cara_ya_detectada(pos_cara, dict_caras):
                # Asignar nuevo ID (siguiente número)
                new_id = len(dict_caras)
                # Guardar en el diccionario
                dict_caras[new_id] = pos_cara

                print(f"Nueva cara detectada con ID {new_id} en {pos_cara}")

            detectado = True
    if detectado:
        print("Cara detectada: :)")

waypoint_x = x_obj
waypoint_y = y_obj
r = 0          # radio inicial
dr = 0.2      # incremento de radio por ciclo
theta = 0      # ángulo
dtheta = 0.2   # incremento de ángulo
dict_caras = {}

while r < 10:


    # Medimos distancia
    x_actual, y_actual, _ = HAL.get_position()
    waypoint_yaw = math.atan2(waypoint_x-x_actual, waypoint_y-y_actual)
    dist = math.sqrt((x_actual - waypoint_x)**2 + (y_actual - waypoint_y)**2)

    # Mover al target actual (NO cambia a cada iteración)
    HAL.set_cmd_pos(waypoint_x, waypoint_y, 4, waypoint_yaw)

    # Si llegó, ENTREGAMOS EL SIGUIENTE punto de la espiral
    if dist < umbral:
        r += dr
        theta += dtheta
        
        waypoint_x = x_obj + r * math.cos(theta)
        waypoint_y = y_obj + r * math.sin(theta)

        print("Nuevo punto de espiral: ", r, theta)
    

    # Cámaras
    img_f = HAL.get_frontal_image()
    img_v = HAL.get_ventral_image()
    WebGUI.showImage(img_f)
    WebGUI.showLeftImage(img_v)
    detectar_superviviente(img_v, dict_caras, (x_actual, y_actual))

    Frequency.tick()


for id_cara, pos_guardada in dict_caras.items():

    print("La cara ", id_cara+1, " está en la pos: ", pos_guardada)

while True:
    HAL.set_cmd_pos(original_pos[0], original_pos[1], 2, waypoint_yaw)
    x_actual, y_actual, _ = HAL.get_position()
    dist = math.sqrt((x_actual - original_pos[0])**2 + (y_actual - original_pos[1])**2)
    if dist < 0.05:
        HAL.land()
    


