# Detector aruco 3D https://www.youtube.com/watch?v=pwtiJ5CsvaI&t=9s
import cv2
import numpy as np
from Calibracion import *

# ------------------Detector aruco-------------------------------
# Inicializamos los parametros del detector de arucos
parametros = cv2.aruco.DetectorParameters()

# Cargamos el diccionario de nuestro aruco
diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

# Creamos el detector de ArUco
detector = cv2.aruco.ArucoDetector(diccionario, parametros)

# ---------------------------Lectura de camara---------------------------
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Definiremos un ancho y un alto definido por siempre
cap.set(4, 720)
cont = 0

# Calibracion
calibracion = calibracion()
matrix, dist = calibracion.calibracion_cam()
print("\n" + "=" * 60)
print("Matriz de la cámara:")
print(matrix)
print("\nCoeficiente de Distorsión:")
print(dist)
print("=" * 60)

# Verificar si la calibración fue exitosa
if np.allclose(matrix, np.eye(3)) and np.allclose(dist, np.zeros((5, 1))):
    print("\n⚠ ADVERTENCIA: Usando calibración por defecto")
    print("Para mejor precisión, calibra la cámara primero:")
    print("1. Presiona 'a' para capturar imágenes del tablero")
    print("2. Captura 10-15 imágenes desde diferentes ángulos")
    print("3. Reinicia el programa")
    print("=" * 60 + "\n")

print("\nControles:")
print("- Presiona 'a' para guardar imagen de calibración")
print("- Presiona ESC para salir\n")

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Error al leer el frame de la cámara")
        break
    
    # Cambiar a escala de grises (BGR2GRAY, no RGB)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectamos los marcadores en la imagen
    esquinas, ids, candidatos_malos = detector.detectMarkers(gray)

    try:
        # Si hay marcadores encontrados por el marcador
        if ids is not None and len(esquinas) > 0:
            # Iterar en marcadores
            for i in range(0, len(ids)):
                # Definir los puntos 3D del marcador (tamaño real en metros)
                markerLength = 0.02  # 2 cm
                objPoints = np.array([
                    [-markerLength/2,  markerLength/2, 0],
                    [ markerLength/2,  markerLength/2, 0],
                    [ markerLength/2, -markerLength/2, 0],
                    [-markerLength/2, -markerLength/2, 0]
                ], dtype=np.float32)
                
                # Estimar la pose usando solvePnP
                success, rvec, tvec = cv2.solvePnP(
                    objPoints, 
                    esquinas[i], 
                    matrix, 
                    dist, 
                    flags=cv2.SOLVEPNP_IPPE_SQUARE
                )

                if success:
                    # Dibuja un cuadrado alrededor de los marcadores
                    cv2.aruco.drawDetectedMarkers(frame, esquinas)

                    # Dibujamos los ejes
                    cv2.drawFrameAxes(frame, matrix, dist, rvec, tvec, 0.01)

                if success:
                    # Dibuja un cuadrado alrededor de los marcadores
                    cv2.aruco.drawDetectedMarkers(frame, esquinas)

                    # Dibujamos los ejes
                    cv2.drawFrameAxes(frame, matrix, dist, rvec, tvec, 0.01)

                    # Coordenadas del centro del marcador (corregidas)
                    c_x = (esquinas[i][0][0][0] + esquinas[i][0][1][0] + 
                           esquinas[i][0][2][0] + esquinas[i][0][3][0]) / 4
                    c_y = (esquinas[i][0][0][1] + esquinas[i][0][1][1] + 
                           esquinas[i][0][2][1] + esquinas[i][0][3][1]) / 4

                    # Mostramos el ID
                    cv2.putText(
                        img=frame, 
                        text=("ID: " + str(ids[i][0])), 
                        org=(int(c_x), int(c_y)), 
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, 
                        fontScale=0.5, 
                        color=(50, 225, 250), 
                        thickness=2
                    )

                    # Extraemos los puntos de las esquinas en coordenadas separadas
                    c1 = (esquinas[i][0][0][0], esquinas[i][0][0][1])
                    c2 = (esquinas[i][0][1][0], esquinas[i][0][1][1])
                    c3 = (esquinas[i][0][2][0], esquinas[i][0][2][1])
                    c4 = (esquinas[i][0][3][0], esquinas[i][0][3][1])
                    v1, v2 = int(c1[0]), int(c1[1])
                    v3, v4 = int(c2[0]), int(c2[1])
                    v5, v6 = int(c3[0]), int(c3[1])
                    v7, v8 = int(c4[0]), int(c4[1])

                    # Dibujamos el cubo
                    # Cara inferior
                    cv2.line(frame, (v1, v2), (v3, v4), (255, 255, 0), 3)
                    cv2.line(frame, (v5, v6), (v7, v8), (255, 255, 0), 3)
                    cv2.line(frame, (v1, v2), (v7, v8), (255, 255, 0), 3)
                    cv2.line(frame, (v3, v4), (v5, v6), (255, 255, 0), 3)

                    # Cara superior
                    cv2.line(frame, (v1, v2 - 200), (v3, v4 - 200), (255, 255, 0), 3)
                    cv2.line(frame, (v5, v6 - 200), (v7, v8 - 200), (255, 255, 0), 3)
                    cv2.line(frame, (v1, v2 - 200), (v7, v8 - 200), (255, 255, 0), 3)
                    cv2.line(frame, (v3, v4 - 200), (v5, v6 - 200), (255, 255, 0), 3)

                    # Caras laterales
                    cv2.line(frame, (v1, v2 - 200), (v1, v2), (255, 255, 0), 3)
                    cv2.line(frame, (v3, v4 - 200), (v3, v4), (255, 255, 0), 3)
                    cv2.line(frame, (v5, v6 - 200), (v5, v6), (255, 255, 0), 3)
                    cv2.line(frame, (v7, v8 - 200), (v7, v8), (255, 255, 0), 3)

                    # Dibujamos la pirámide
                    # Cara inferior
                    cv2.line(frame, (v1, v2), (v3, v4), (255, 0, 255), 3)
                    cv2.line(frame, (v5, v6), (v7, v8), (255, 0, 255), 3)
                    cv2.line(frame, (v1, v2), (v7, v8), (255, 0, 255), 3)
                    cv2.line(frame, (v3, v4), (v5, v6), (255, 0, 255), 3)

                    # Ápice de la pirámide
                    cex1, cey1 = (v1 + v5) // 2, (v2 + v6) // 2
                    cey2 = ((v2 + v4 + v6 + v8) // 4) - 200
                    cv2.line(frame, (v1, v2), (cex1, cey2), (255, 0, 255), 3)
                    cv2.line(frame, (v5, v6), (cex1, cey2), (255, 0, 255), 3)
                    cv2.line(frame, (v3, v4), (cex1, cey2), (255, 0, 255), 3)
                    cv2.line(frame, (v7, v8), (cex1, cey2), (255, 0, 255), 3)

    except Exception as e:
        if ids is None or len(ids) == 0:
            pass  # No imprimir mensaje si simplemente no hay marcador
        else:
            print(f"Error al procesar marcador: {e}")

    cv2.imshow("Realidad Aumentada 3D", frame)

    k = cv2.waitKey(1)

    # Almacenamos las fotos para la calibración
    if k == 97:  # Tecla 'a'
        filename = f"cali{cont}.png"
        cv2.imwrite(filename, frame)
        print(f"✓ Imagen guardada: {filename}")
        cont = cont + 1

    if k == 27:  # Tecla ESC
        break

cap.release()
cv2.destroyAllWindows()
