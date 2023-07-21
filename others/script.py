from abc import ABC, abstractmethod


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


class OpenCVImageHandler(ImageHandler):

    def read_image(self, path):
        return cv2.imread(path)

    def save_image(self, path, image):
        cv2.imwrite(path, image)

    def move_image(self, src, dest):
        shutil.move(src, dest)


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


if __name__ == "__main__":
    model_path = "../resources/dat/shape_predictor_68_face_landmarks.dat"
    image_dir = "../resources/images/process_me/"
    archive_dir = "../resources/images/archive/"
    headshot_dir = "../resources/images/head_shots/"
    facet_dir = "../resources/images/facets/"
    extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    image_handler = OpenCVImageHandler()
    image_processor = DlibImageProcessor(model_path)

    service = ImageService(image_dir, archive_dir, headshot_dir, facet_dir, extensions, image_handler, image_processor)
    service.process_images()
