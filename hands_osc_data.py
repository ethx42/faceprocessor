import cv2
import mediapipe as mp
from pythonosc import udp_client

# Crea un objeto de la clase Hands de mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Crea un objeto de la clase DrawingUtils de mediapipe para dibujar los resultados
mp_drawing = mp.solutions.drawing_utils

# Crea un cliente OSC para enviar mensajes a TouchDesigner
osc_client = udp_client.SimpleUDPClient("localhost", 12345)

# Inicia la captura de video de la cámara web
cap = cv2.VideoCapture(0)

while True:
    # Captura un frame de la cámara
    ret, frame = cap.read()

    if not ret:
        break

    # Cambia el espacio de color de BGR a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesa el frame con el modelo de detección de manos
    results = hands.process(rgb_frame)

    # Dibuja los resultados en el frame original
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
          mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

          # Lista de puntos de interés: muñeca y puntas de los dedos
          points_of_interest = [4, 8, 12, 16, 20]

          # Envia las coordenadas de los puntos de control a TouchDesigner via OSC
          for i in points_of_interest:
              landmark = hand_landmarks.landmark[i]
              osc_client.send_message(f"/hand/{i}/x", landmark.x)
              osc_client.send_message(f"/hand/{i}/y", landmark.y)

    # Muestra el frame
    cv2.imshow('Frame', frame)

    # Si se presiona la tecla 'q', salir del bucle
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera los recursos de la cámara y cierra las ventanas de OpenCV
cap.release()
cv2.destroyAllWindows()
