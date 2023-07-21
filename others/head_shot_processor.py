import dlib
import cv2
import os
# import time
import uuid
import shutil

detector = dlib.get_frontal_face_detector()

predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")

os.makedirs('../resources/images/head_shots', exist_ok=True)
os.makedirs('../resources/images/archive', exist_ok=True)

path = "../resources/images/process_me/"

allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

for filename in os.listdir(path):
    ext = os.path.splitext(filename)[1]

    if ext.lower() in allowed_extensions:
        img = cv2.imread(path + filename)
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            img_id = uuid.uuid4()
            landmarks = predictor(image=gray, box=face)

            top_margin = 100
            bottom_margin = 2 * top_margin

            head_img = img[max(0, landmarks.part(24).y - top_margin):min(img.shape[0], landmarks.part(8).y + bottom_margin), 0:img.shape[1]]
            cv2.imwrite(f'./images/head_shots/head_{img_id}{ext}', head_img)

        shutil.move(path + filename, f'resources/images/archive/{os.path.splitext(filename)[0]}_HS{ext}')