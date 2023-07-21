import cv2
import dlib

# Cargar el detector de rostros de dlib
detector = dlib.get_frontal_face_detector()

# Cargar el predictor de puntos de referencia faciales
predictor = dlib.shape_predictor("./dat/shape_predictor_68_face_landmarks.dat")

# Comenzar la captura de video de la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturar un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Convertir el frame a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    faces = detector(gray)

    for face in faces:
        # Predecir los puntos de referencia faciales
        landmarks = predictor(gray, face)

        # Dibujar los puntos de referencia en el rostro
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)  # Punto de color verde claro
            cv2.putText(frame, str(n), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)  # Número de identificación del punto

    # Mostrar el frame con los puntos de referencia dibujados
    cv2.imshow("Frame", frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos de la cámara y cerrar las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
