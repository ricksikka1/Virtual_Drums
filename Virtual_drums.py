import numpy as np
import cv2
import time
import pygame.mixer

# Importing Video Camera Feed
camera = cv2.VideoCapture(0)


# Importing Drum pictures

# hat = cv2.resize(cv2.imread('./images/high_hat.png'),(200,100), interpolation=cv2.INTER_CUBIC)
# snare = cv2.resize(cv2.imread('./images/snare_drum.png.png'), (200,100), interpolation=cv2.INTER_CUBIC)

while True:

    ret, frame = camera.read()
    cv2.imshow('VideoCam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
camera.release()