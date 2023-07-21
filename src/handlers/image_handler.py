from abc import ABC, abstractmethod
import cv2
import shutil


class ImageHandler(ABC):

    @abstractmethod
    def read_image(self, path):
        pass

    @abstractmethod
    def save_image(self, path, image):
        pass

    @abstractmethod
    def move_image(self, src, dest):
        pass


class OpenCVImageHandler(ImageHandler):

    def read_image(self, path):
        return cv2.imread(path)

    def save_image(self, path, image):
        cv2.imwrite(path, image)

    def move_image(self, src, dest):
        shutil.move(src, dest)
