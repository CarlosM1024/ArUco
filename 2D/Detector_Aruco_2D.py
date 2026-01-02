#Detector de aruco https://www.youtube.com/watch?v=hKyWMmKTyeU
import cv2
import numpy as np

#Inicializamos los parametros del detector de arucos
parametros = cv2.aruco.DetectorParameters()

#Cargamos el diccionario de nuestro aruco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

#---------------------------Lectura de camara---------------------------
cap = cv2.VideoCapture(0)
cap.set(3,1280) #Definiremos un ancho y un alto definido por siempre
cap.set(4, 720)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #Detectamos los marcadores en la imagen.
    esquinas, ids, candidatos_malos = cv2.aruco.detectMarkers(gray, diccionario, parameters=parametros)
    #En las esquinas esta guardadas las esquinas por fuera del marcador aruco.
    #ids se genera al crear el marcador.
    #Candidatos malos es por si hace una preseleccion antes de seleccionar nuestro aruco pero no se utiliza.

    if np.all(ids != None):
        aruco = cv2.aruco.drawDetectedMarkers(frame, esquinas)
        #Se dibuja el contorno del aruco.

        #Extraemos los puntos de las esquinas en coordenadas separadas.
        c1 = (esquinas[0][0][0][0], esquinas[0][0][0][1])
        c2 = (esquinas[0][0][1][0], esquinas[0][0][1][1])
        c3 = (esquinas[0][0][2][0], esquinas[0][0][2][1])
        c4 = (esquinas[0][0][3][0], esquinas[0][0][3][1])

        copy = frame #Se hace una copia

        #Leemos la imagen que vamos a sobreponer
        #imagen = cv2.imread("jojo.jpg")
        imagen = cv2.imread("OnePiece.jpg")
        #imagen = cv2.imread("OPM.jpg")

        #Extraemos el tamaño de la imagen
        tamaño = imagen.shape

        #Organizaremos las coordenadas del aruco en una matriz
        puntos_aruco = np.array([c1, c2, c3, c4])

        #Organizaos las coordenadas del aruco en una matriz
        puntos_imagen = np.array([
            [0, 0],
            [tamaño[1]-1, 0],
            [tamaño[1]-1, tamaño[0]-1],
            [0, tamaño[0]-1]
        ], dtype=float)

        #Realizamos una superposicion de la imagen (Homografia), poner la imagen encima del aruco
        h, estado = cv2.findHomography(puntos_imagen, puntos_aruco)

        #Realizamos la transformacion de perspectiva, para que se mueva la imagen con el aruco
        perspectiva = cv2.warpPerspective(imagen, h, (copy.shape[1], copy.shape[0]))
        cv2.fillConvexPoly(copy,puntos_aruco.astype(int), 0, 16)
        copy = copy + perspectiva
        cv2.imshow("Realidad virtual", copy)

    else:
        cv2.imshow("Realidad virtual", frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
