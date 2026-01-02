#Detector aruco 3D https://www.youtube.com/watch?v=pwtiJ5CsvaI&t=9s
import cv2
import numpy as np
from Calibracion import *

#------------------Detector aruco-------------------------------
#Inicializamos los parametros del detector de arucos
parametros = cv2.aruco.DetectorParameters()

#Cargamos el diccionario de nuestro aruco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

#---------------------------Lectura de camara---------------------------
cap = cv2.VideoCapture(0)
cap.set(3,1280) #Definiremos un ancho y un alto definido por siempre
cap.set(4, 720)
cont = 0

#Calibracion
calibracion = calibracion()
matrix, dist = calibracion.calibracion_cam()
print("Matriz de la camara", matrix)
print("Coeficiente de Distorcion: ", dist)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Detectamos los marcadores en la imagen.
    #Camera matrix: Calibracion de la imagen.
    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)
    #esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters = parametros, cameraMatrix = matrix, distCoeff = dist)
    #En las esquinas esta guardadas las esquinas por fuera del marcador aruco.
    #ids se genera al crear el marcador.
    #Candidatos malos es por si hace una preseleccion antes de seleccionar nuestro aruco pero no se utiliza.

    try:
        #Si hay marcadores encontrados por el marcador
        if len(esquinas) > 0:
        #if np.all(ids != None):
            #Iterar en marcadores.
            for i in range(0, len(ids)):
                #Estime la pose de cada marcador y devuelva los valores rvec y tvec --- diferentes de los coeficientes de la camara.
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners=esquinas[i], markerLength=0.02, cameraMatrix=matrix, distCoeffs=dist)

                #Eliminamos el error de la matriz de valores numpy
                (rvec - tvec).any()

                #Dibuja un cuadrado alrededor de los marcadores
                cv2.aruco.drawDetectedMarkers(frame, esquinas)

                #Dibujamos los ejes
                cv2.drawFrameAxes(frame, matrix, dist, rvec, tvec, 0.01)

                #Coordenada X del centro del marcador
                c_x = (esquinas[i][0][0][0] + esquinas[i][0][1][0] + esquinas[i][0][2][0] + esquinas[i][0][3][0] / 4)

                #Coordenada Y del centro del marcador
                c_y = (esquinas[i][0][0][1] + esquinas[i][0][1][1] + esquinas[i][0][2][1] + esquinas[i][0][3][1] / 4)

                #Mostramos el ID
                cv2.putText(img=frame, text=("id" + str(ids[i])), org=((int(c_x)), (int(c_y))), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(50, 225, 250), thickness=2)

                #Extraemos los puntos de las esquinas en coordenadas separadas.
                c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
                c2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
                c3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
                c4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])
                v1, v2 = c1[0], c1[1]
                v3, v4 = c2[0], c2[1]
                v5, v6 = c3[0], c3[1]
                v7, v8 = c4[0], c4[1]

            #Dibujamos el cubo
                #Cara inferior
                cv2.line(frame, (int(v1), int(v2)), (int(v3), int(v4)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6)), (int(v7), int(v8)), (255, 255, 0), 3)
                cv2.line(frame, (int(v1), int(v2)), (int(v7), int(v8)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(v5), int(v6)), (255, 255, 0), 3)

                #Cara superior
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v3), int(v4 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v7), int(v8 - 200)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4 - 200)), (int(v5), int(v6 - 200)), (255, 255, 0), 3)

                # Cara laterales
                cv2.line(frame, (int(v1), int(v2 - 200)), (int(v1), int(v2)), (255, 255, 0), 3)
                cv2.line(frame, (int(v3), int(v4 - 200)), (int(v3), int(v4)), (255, 255, 0), 3)
                cv2.line(frame, (int(v5), int(v6 - 200)), (int(v5), int(v6)), (255, 255, 0), 3)
                cv2.line(frame, (int(v7), int(v8 - 200)), (int(v7), int(v8)), (255, 255, 0), 3)

            # Dibujamos la piramide
                # Cara inferior
                cv2.line(frame, (int(v1), int(v2)), (int(v3), int(v4)), (255, 0, 255), 3)
                cv2.line(frame, (int(v5), int(v6)), (int(v7), int(v8)), (255, 0, 255), 3)
                cv2.line(frame, (int(v1), int(v2)), (int(v7), int(v8)), (255, 0, 255), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(v5), int(v6)), (255, 0, 255), 3)

                # Esquinas
                cex1, cey1 = (v1 + v5) // 2, (v2 + v6) // 2
                cex2, cey2 = (v3 + v7) // 2, (v4 + v8) // 2
                cv2.line(frame, (int(v1), int(v2)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v5), int(v6)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v3), int(v4)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)
                cv2.line(frame, (int(v7), int(v8)), (int(cex1), int(cey2 - 200)), (255, 0, 255), 3)

    except:
        if ids is None or len(ids) == 0:
            print("**********Marker Detection Failed**********")

    cv2.imshow("Realidad virtual", frame)

    k = cv2.waitKey(1)

    #Almacenamos las fotos para la calibracion
    if k == 97:
        print("Imagen Guardada")
        cv2.imwrite("cali{}.png".format(cont), frame)
        cont = cont + 1

    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
