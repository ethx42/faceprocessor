import dlib
import cv2
import os
# import time
import uuid
import shutil

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")

os.makedirs('../resources/images/facets/eyes', exist_ok=True)
os.makedirs('../resources/images/facets/mouth', exist_ok=True)
os.makedirs('../resources/images/facets/nose', exist_ok=True)
os.makedirs('../resources/images/facets/forehead', exist_ok=True)
os.makedirs('../resources/images/facets/chin', exist_ok=True)
os.makedirs('../resources/images/facets/neck', exist_ok=True)
os.makedirs('../resources/images/archive', exist_ok=True)

path = "../resources/images/head_shots/"

allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

for filename in os.listdir(path):
    ext = os.path.splitext(filename)[1]
    if ext.lower() in allowed_extensions:
        img_id = uuid.uuid4()
        img = cv2.imread(path + filename)
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            landmarks = predictor(image=gray, box=face)
            margin = 40

            eye_img = img[max(0, landmarks.part(37).y - margin):min(img.shape[0], landmarks.part(41).y + margin), 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/eyes/eye_{img_id}{ext}', eye_img)

            mouth_img = img[max(0, landmarks.part(48).y - margin):min(img.shape[0], landmarks.part(57).y + margin), 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/mouth/mouth_{img_id}{ext}', mouth_img)

            nose_margin = 12
            nose_img = img[max(0, landmarks.part(27).y - nose_margin):min(img.shape[0], landmarks.part(33).y + nose_margin), 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/nose/nose_{img_id}{ext}', nose_img)

            forehead_img = img[0:min(img.shape[0], landmarks.part(21).y), 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/forehead/forehead_{img_id}{ext}', forehead_img)

            chin_img = img[max(0, landmarks.part(57).y):min(img.shape[0], landmarks.part(8).y + margin), 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/chin/chin_{img_id}{ext}', chin_img)

            neck_img = img[max(0, landmarks.part(8).y):img.shape[0], 0:img.shape[1]]
            cv2.imwrite(f'./images/facets/neck/neck_{img_id}{ext}', neck_img)

        shutil.move(path + filename, f'resources/images/archive/{os.path.splitext(filename)[0]}{ext}')
