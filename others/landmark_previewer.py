import cv2
import dlib
# import numpy as np
# from PIL import Image
import os

predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")
detector = dlib.get_frontal_face_detector()
path = '../resources/images/process_me/'

parts = ["forehead", "eyes", "nose", "mouth", "chin", "neck"]

for filename in os.listdir(path):
    if filename.endswith(".png"):
        img = dlib.load_rgb_image(path+filename)

        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = predictor(img, d)

            for i in range(shape.num_parts):
                p = shape.part(i)
                cv2.circle(img, (p.x, p.y), 2, (0, 255, 0), -1)
                cv2.putText(img, str(i), (p.x, p.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        cv2.imshow('image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
