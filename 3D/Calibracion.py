import cv2
import numpy as np
import glob
import os

class calibracion():
    def __init__(self):
        self.tablero = (6, 4)
        self.tam_frame = (1280, 720)

        # Criterio
        self.criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Preparamos los puntos del tablero
        self.puntos_obj = np.zeros((self.tablero[0] * self.tablero[1], 3), np.float32)
        self.puntos_obj[:,:2] = np.mgrid[0: self.tablero[0], 0: self.tablero[1]].T.reshape(-1, 2)

        # Preparamos las listas para almacenar los puntos del mundo real y de la imagen
        self.puntos_3d = []
        self.puntos_img = []

    def calibracion_cam(self):
        # Buscar archivos tanto .jpg como .png
        fotos = glob.glob('*.jpg') + glob.glob('*.png')
        
        if len(fotos) == 0:
            print("=" * 60)
            print("ERROR: No se encontraron imágenes para calibración")
            print("=" * 60)
            print("Asegúrate de tener imágenes del tablero de ajedrez")
            print("en el directorio actual.")
            print(f"Directorio actual: {os.getcwd()}")
            print("=" * 60)
            print("\nPasos para calibrar:")
            print("1. Ejecuta el detector 3D")
            print("2. Presiona 'a' para capturar imágenes del tablero")
            print("3. Captura al menos 10-15 imágenes desde diferentes ángulos")
            print("4. Presiona ESC para salir")
            print("5. Vuelve a ejecutar el programa")
            print("=" * 60)
            
            # Retornar matrices por defecto para que no crashee
            return np.eye(3), np.zeros((5, 1))
        
        print(f"\nEncontradas {len(fotos)} imágenes para calibración")
        print("-" * 60)
        
        for foto in fotos:
            print(f"Procesando: {foto}")
            img = cv2.imread(foto)
            
            if img is None:
                print(f"  ⚠ No se pudo leer la imagen: {foto}")
                continue
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Buscamos las esquinas del tablero
            ret, esquinas = cv2.findChessboardCorners(gray, self.tablero, None)

            if ret == True:
                self.puntos_3d.append(self.puntos_obj)
                esquinas2 = cv2.cornerSubPix(gray, esquinas, (11, 11), (-1, -1), self.criterio)
                self.puntos_img.append(esquinas)
                cv2.drawChessboardCorners(img, self.tablero, esquinas2, ret)
                print(f"  ✓ Tablero detectado correctamente")
                cv2.imshow("Calibracion - Tablero detectado", img)
                cv2.waitKey(200)  # Mostrar brevemente cada imagen procesada
            else:
                print(f"  ✗ No se detectó el tablero en esta imagen")

        cv2.destroyAllWindows()
        
        # Verificar que se hayan encontrado suficientes imágenes válidas
        if len(self.puntos_3d) == 0:
            print("\n" + "=" * 60)
            print("ERROR: No se detectó el tablero en ninguna imagen")
            print("=" * 60)
            print("Posibles causas:")
            print("- Las dimensiones del tablero no coinciden (actualmente: 6x4)")
            print("- Las imágenes no muestran claramente el tablero de ajedrez")
            print("- El tablero está muy borroso o mal iluminado")
            print("=" * 60)
            return np.eye(3), np.zeros((5, 1))
        
        print(f"\n✓ Se detectaron {len(self.puntos_3d)} tableros válidos")
        print("Realizando calibración de la cámara...")
        
        # Calibración de la cámara
        ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(
            self.puntos_3d, 
            self.puntos_img, 
            self.tam_frame, 
            None, 
            None
        )
        
        if ret:
            print("✓ Calibración completada exitosamente")
            print(f"Error de reproyección: {ret:.4f}")
        
        return cameraMatrix, dist
    