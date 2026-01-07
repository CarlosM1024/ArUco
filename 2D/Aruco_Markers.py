#ArUco
import numpy as np
import cv2, PIL, os
#from cv2 import aruco
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

id = 25 # This is the identifier of the bookmark, you can change it to whatever you need
img_size = 700 # Define the size of the final image
marker_img = cv2.aruco.generateImageMarker(aruco_dict, id, img_size)

plt.imshow(marker_img, cmap='gray', interpolation='nearest')
plt.axis('off')
plt.show()

cv2.imwrite('aruco{}.png'.format(id), marker_img)