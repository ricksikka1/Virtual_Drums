
from flask import Flask, render_template, Response
import numpy as np
import cv2
import time
from pygame import mixer

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def gen():
    def play_sound(detected, sound):

        play = detected > hat_thickness[0] * hat_thickness[1] * 0.8

        if play and sound == 1:
            #sound_drum.play()
            time.sleep(0.001)

        elif play and sound == 2:
            #sound_hat.play()
            time.sleep(0.001)

    # This function is to check if the green object is present in the small region
    def detect_in_region(frame, sound):

        # converting BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # creating mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)

        # calc number of green pixels
        detected = np.sum(mask)

        play_sound(detected, sound)

        return mask

    # Importing Video Camera Feed
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    H, W = frame.shape[:2]  # Skips Channel

    # Importing Drum sounds
    #mixer.init()
    #sound_hat = mixer.Sound('./Sounds/hat.ogg')
    #sound_drum = mixer.Sound('./Sounds/snare.wav')

    # Set HSV range for detecting green color
    greenLower = (25, 52, 72)
    greenUpper = (102, 255, 255)

    kernel = np.ones((7, 7), np.uint8)

    # Read the image of High Hat and the Snare drum
    hat = cv2.resize(cv2.imread('./Images/high_hat.png'), (200, 100), interpolation=cv2.INTER_CUBIC)
    snare = cv2.resize(cv2.imread('./Images/snare_drum.png'), (200, 100), interpolation=cv2.INTER_CUBIC)

    # Set region for detecting green
    hat_cntr = [np.shape(frame)[1] * 2 // 8, np.shape(frame)[0] * 6 // 8]
    snare_cntr = [np.shape(frame)[1] * 6 // 8, np.shape(frame)[0] * 6 // 8]

    hat_thickness = [200, 100]
    hat_top = [hat_cntr[0] - hat_thickness[0] // 2, hat_cntr[1] - hat_thickness[1] // 2]
    hat_btm = [hat_cntr[0] + hat_thickness[0] // 2, hat_cntr[1] + hat_thickness[1] // 2]

    snare_thickness = [200, 100]
    snare_top = [snare_cntr[0] - snare_thickness[0] // 2, snare_cntr[1] - snare_thickness[1] // 2]
    snare_btm = [snare_cntr[0] + snare_thickness[0] // 2, snare_cntr[1] + snare_thickness[1] // 2]

    time.sleep(1)

    while True:

        ret, frame = camera.read()
        frame = cv2.flip(frame, 1)

        # Region for the Snare
        snare_region = np.copy(frame[snare_top[1]:snare_btm[1], snare_top[0]:snare_btm[0]])
        mask = detect_in_region(snare_region, 1)

        # Region for the Hi hat
        hat_region = np.copy(frame[hat_top[1]:hat_btm[1], hat_top[0]:hat_btm[0]])
        mask = detect_in_region(hat_region, 2)

        # Output text
        cv2.putText(frame, 'Virtual Drums', (10, 30), 2, 1, (20, 20, 20), 2)
        cv2.putText(frame, 'Rick Sikka', (1100, 30), 2, 1, (20, 20, 20), 2)
        cv2.putText(frame, '"q" to exit', (1100, 70), 2, 1, (20, 20, 20), 2)

        # Display Both transparently
        frame[snare_top[1]:snare_btm[1], snare_top[0]:snare_btm[0]] = cv2.addWeighted(snare, 1, frame[snare_top[1]:snare_btm[1], snare_top[0]:snare_btm[0]], 1, 0)
        frame[hat_top[1]:hat_btm[1], hat_top[0]:hat_btm[0]] = cv2.addWeighted(hat, 1, frame[hat_top[1]:hat_btm[1], hat_top[0]:hat_btm[0]], 1, 0)

        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)