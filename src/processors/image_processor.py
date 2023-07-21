from abc import ABC, abstractmethod
import dlib


class ImageProcessor(ABC):

    @abstractmethod
    def detect_faces(self, image):
        pass

    @abstractmethod
    def extract_landmarks(self, image, face):
        pass


class DlibImageProcessor(ImageProcessor):

    def __init__(self, model_path):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(model_path)

    def detect_faces(self, image):
        return self.detector(image)

    def extract_landmarks(self, image, face):
        return self.predictor(image, face)
