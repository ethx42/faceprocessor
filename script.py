# # add a description of the next code lines


# import dlib
# import cv2
# import os
# import time
# import uuid
# import shutil

# # Cargar el detector de rostros de dlib
# detector = dlib.get_frontal_face_detector()

# # Cargar el predictor de puntos de referencia faciales
# predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")

# # Crea los directorios para guardar las imágenes recortadas y archivadas
# os.makedirs('./images/head_shots', exist_ok=True)
# os.makedirs('./images/archive', exist_ok=True)

# # Directorio de imágenes para procesar
# path = "./images/processme/"

# # List of allowed image file extensions
# allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

# for filename in os.listdir(path):
#     ext = os.path.splitext(filename)[1]
#     if ext.lower() in allowed_extensions:

#         # Cargar una imagen
#         img = cv2.imread(path + filename)

#         # Convierte la imagen a escala de grises
#         gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

#         # Usa el detector para encontrar rostros en la imagen
#         faces = detector(gray)

#         for face in faces:
#             # Genera un UUID para las imágenes resultantes
#             img_id = uuid.uuid4()

#             # Usa el predictor para encontrar puntos de referencia
#             landmarks = predictor(image=gray, box=face)

#             # Recorta las regiones de interés y guarda las imágenes
#             top_margin = 100  # Aumenta este valor para capturar más de la parte superior de la cabeza
#             bottom_margin = 2 * top_margin  # Este valor puede ajustarse para cambiar cuánto del cuello y los hombros se captura

#             # Asegúrate de no recortar más allá de los límites de la imagen
#             head_img = img[max(0, landmarks.part(24).y - top_margin):min(img.shape[0], landmarks.part(8).y + bottom_margin), 0:img.shape[1]]
#             cv2.imwrite(f'./images/head_shots/head_{img_id}{ext}', head_img)

#         # Mueve la imagen procesada al directorio de archivo con un nombre modificado
#         timestamp = time.strftime("%Y%m%d-%H%M%S")
#         shutil.move(path + filename, f'./images/archive/{os.path.splitext(filename)[0]}_OK_{timestamp}{ext}')










import dlib
import numpy as np
import cv2
import os
import time
import uuid
import shutil

# Cargar el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()

# Cargar el predictor de puntos de referencia faciales
predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")

# Crea los directorios para guardar las imágenes recortadas y archivadas
os.makedirs('./images/facets/eyes', exist_ok=True)
os.makedirs('./images/facets/mouth', exist_ok=True)
os.makedirs('./images/facets/nose', exist_ok=True)
os.makedirs('./images/facets/forehead', exist_ok=True)
os.makedirs('./images/facets/chin', exist_ok=True)
os.makedirs('./images/facets/neck', exist_ok=True)
os.makedirs('./images/archive', exist_ok=True)

# Directorio de imágenes para procesar
path = "./images/head_shots/"

# List of allowed image file extensions
allowed_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

for filename in os.listdir(path):
    ext = os.path.splitext(filename)[1]
    if ext.lower() in allowed_extensions:
        # Genera un UUID para las imágenes resultantes
        img_id = uuid.uuid4()

        # Cargar una imagen
        img = cv2.imread(path + filename)

        # Convierte la imagen a escala de grises
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)

        # Usa el detector para encontrar rostros en la imagen
        faces = detector(gray)

        for face in faces:
            # Usa el predictor para encontrar puntos de referencia
            landmarks = predictor(image=gray, box=face)

            # Recorta las regiones de interés y guarda las imágenes
            margin = 40  # Puedes ajustar este valor para cambiar el margen

            # Asegúrate de no recortar más allá de los límites de la imagen
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

        # Mueve la imagen procesada al directorio de archivo con un nombre modificado
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        shutil.move(path + filename, f'./images/archive/{os.path.splitext(filename)[0]}_OK_{timestamp}{ext}')





# import cv2
# import dlib
# import numpy as np
# from PIL import Image
# import os

# predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")
# detector = dlib.get_frontal_face_detector()
# path = './images/processme/'

# # Lista de nombres de las partes del rostro
# parts = ["forehead", "eyes", "nose", "mouth", "chin", "neck"]

# for filename in os.listdir(path):
#     if filename.endswith(".png"):
#         # Cargar la imagen
#         img = dlib.load_rgb_image(path+filename)
        
#         # Detectar los rostros
#         dets = detector(img, 1)
#         for k, d in enumerate(dets):
#             # Predecir los puntos de referencia
#             shape = predictor(img, d)

#             # Dibujar los puntos de referencia en la imagen
#             for i in range(shape.num_parts):
#                 p = shape.part(i)
#                 cv2.circle(img, (p.x, p.y), 2, (0, 255, 0), -1)
#                 cv2.putText(img, str(i), (p.x, p.y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        
#         # Convertir la imagen de BGR a RGB
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#         # Mostrar la imagen
#         cv2.imshow('image', img)
#         cv2.waitKey(0)  # Espera hasta que se presione una tecla para cerrar la ventana
#         cv2.destroyAllWindows()
