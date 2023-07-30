import cv2
import dlib
import numpy as np
from pythonosc import udp_client

# Initialize dlib's face detector
detector = dlib.get_frontal_face_detector()

# Load the dlib facial landmark predictor model
predictor = dlib.shape_predictor('../../resources/dat/shape_predictor_68_face_landmarks.dat')

# Set up the OSC client
client = udp_client.SimpleUDPClient('localhost', 10000)

# Function to detect face and the direction
def detect_and_direct(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)

    # Iterate over each face found
    for rect in faces:
        # Draw a green rectangle around the face
        x = rect.left()
        y = rect.top()
        w = rect.width()
        h = rect.height()
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Use dlib to get the facial landmarks
        shape = predictor(gray, rect)

        # Calculate the center of gravity of the eyes
        left_eye = np.mean([(shape.part(n).x, shape.part(n).y) for n in range(36, 42)], axis=0)
        right_eye = np.mean([(shape.part(n).x, shape.part(n).y) for n in range(42, 48)], axis=0)
        eye_center = (left_eye + right_eye) / 2

        # Calculate the direction vector
        direction_vector = eye_center - np.array([x+w/2, y+h/2])

        # Determine the direction
        if np.linalg.norm(direction_vector) < w/4:
            direction = 'front'
        elif direction_vector[0] > 0:
            direction = 'right'
        else:
            direction = 'left'

        # Put text indicating direction
        cv2.putText(frame, direction, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        # Send the OSC signal with face direction
        client.send_message("/face/direction", direction)

    return frame

# Open the video feed (0 for webcam, or a filename for a video file)
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the video feed
    ret, frame = cap.read()

    if not ret:
        break

    # Apply the face detection and direction estimation
    frame = detect_and_direct(frame)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and close the windows
cap.release()
cv2.destroyAllWindows()
