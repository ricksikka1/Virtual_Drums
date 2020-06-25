import numpy as np
import cv2
import time
import pygame.mixer

# Importing Video Camera Feed
camera = cv2.VideoCapture(0)
ret, frame = camera.read()
H, W = frame.shape[:2]  # Skips Channel

# Importing Drum sounds
pygame.mixer.init()
sound_hat = pygame.mixer.Sound('./Sounds/hat.wav')
sound_drum = pygame.mixer.sound('./Sounds/snare.wav')

# Set HSV range for detecting green color
greenLower = (25, 52, 72)
greenUpper = (102, 255, 255)

kernel = np.ones((7, 7), np.uint8)

# Importing Drum pictures
hat = cv2.resize(cv2.imread('./images/high_hat.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
snare = cv2.resize(cv2.imread('./images/snare_drum.png.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

while True:

   # ret, frame = camera.read()
   # cv2.imshow('VideoCam', hat)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
camera.release()