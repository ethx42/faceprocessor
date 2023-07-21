import cv2
import mediapipe as mp

# Crear un objeto de la clase Hands de mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Crear un objeto de la clase DrawingUtils de mediapipe para dibujar los resultados
mp_drawing = mp.solutions.drawing_utils

# Iniciar la captura de video de la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Capturar un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Cambiar el espacio de color de BGR a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar el frame con el modelo de detección de manos
    results = hands.process(rgb_frame)

    # Dibujar los resultados en el frame original
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Mostrar el frame
    cv2.imshow('Frame', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar los recursos de la cámara y cerrar las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
