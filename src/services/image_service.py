import uuid
import os
import cv2


class ImageService:

    def __init__(self, image_dir, archive_dir, headshot_dir, facet_dir, extensions, image_handler, image_processor):
        self.image_dir = image_dir
        self.archive_dir = archive_dir
        self.headshot_dir = headshot_dir
        self.facet_dir = facet_dir
        self.extensions = extensions
        self.image_handler = image_handler
        self.image_processor = image_processor

    def process_images(self):
        for filename in os.listdir(self.image_dir):
            ext = os.path.splitext(filename)[1]
            if ext.lower() in self.extensions:
                img_path = os.path.join(self.image_dir, filename)
                img = self.image_handler.read_image(img_path)
                gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
                faces = self.image_processor.detect_faces(gray)
                for face in faces:
                    img_id = uuid.uuid4()
                    landmarks = self.image_processor.extract_landmarks(gray, face)
                    self.save_headshot(img, landmarks, img_id, ext)
                    self.save_facets(img, landmarks, img_id, ext)
                self.image_handler.move_image(img_path,
                                              os.path.join(self.archive_dir, f'{os.path.splitext(filename)[0]}{ext}'))

    def save_headshot(self, img, landmarks, img_id, ext):
        top_margin = 100
        bottom_margin = 2 * top_margin
        head_img = img[max(0, landmarks.part(24).y - top_margin):min(img.shape[0], landmarks.part(8).y + bottom_margin),
                   0:img.shape[1]]
        self.image_handler.save_image(os.path.join(self.headshot_dir, f'head_{img_id}{ext}'), head_img)

    def save_facets(self, img, landmarks, img_id, ext):
        margin = 40
        facets = {
            'eyes': img[max(0, landmarks.part(37).y - margin):min(img.shape[0], landmarks.part(41).y + margin),
                    0:img.shape[1]],
            'mouth': img[max(0, landmarks.part(48).y - margin):min(img.shape[0], landmarks.part(57).y + margin),
                     0:img.shape[1]],
            'nose': img[max(0, landmarks.part(27).y - margin):min(img.shape[0], landmarks.part(33).y + margin),
                    0:img.shape[1]],
            'forehead': img[0:min(img.shape[0], landmarks.part(21).y), 0:img.shape[1]],
            'chin': img[max(0, landmarks.part(57).y):min(img.shape[0], landmarks.part(8).y + margin), 0:img.shape[1]],
            'neck': img[max(0, landmarks.part(8).y):img.shape[0], 0:img.shape[1]]
        }
        for facet, image in facets.items():
            self.image_handler.save_image(os.path.join(self.facet_dir, facet, f'{facet}_{img_id}{ext}'), image)
