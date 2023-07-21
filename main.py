from src.handlers.image_handler import OpenCVImageHandler
from src.processors.image_processor import DlibImageProcessor
from src.services.image_service import ImageService

if __name__ == "__main__":
    model_path = "resources/dat/shape_predictor_68_face_landmarks.dat"
    image_dir = "resources/images/process_me/"
    archive_dir = "resources/images/archive/"
    headshot_dir = "resources/images/head_shots/"
    facet_dir = "resources/images/facets/"
    extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    image_handler = OpenCVImageHandler()
    image_processor = DlibImageProcessor(model_path)

    service = ImageService(image_dir, archive_dir, headshot_dir, facet_dir, extensions, image_handler, image_processor)
    service.process_images()
