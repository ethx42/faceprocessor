# Face Image Processor

This project is an image processing application that uses computer vision libraries such as Dlib and OpenCV to identify and segment different facets or regions of human faces in photographs. The facets include eyes, mouth, nose, forehead, chin, and neck.

The project is organized in a modular, object-oriented structure, facilitating the extensibility and maintainability of the code.

## Project Structure

The project is structured as follows:

```
.
├── main.py
├── resources
│   ├── dat
│   │   └── shape_predictor_68_face_landmarks.dat
│   └── images
│       ├── archive
│       ├── facets
│       │   ├── chin
│       │   ├── eyes
│       │   ├── forehead
│       │   ├── mouth
│       │   ├── neck
│       │   └── nose
│       ├── head_shots
│       └── process_me
├── scripts
│ └── cleanup.sh
└── src
    ├── handlers
    │   └── image_handler.py
    ├── processors
    │   └── image_processor.py
    └── services
        └── image_service.py
```

## Usage Instructions

1. Make sure you have Python 3.6 or above installed on your machine.

2. Install the project dependencies with the following command:

```
pip3 install -r requirements.txt
```

3. Place the images you want to process in the `resources/images/process_me/` directory.

4. Run the `main.py` file with the following command:

```
python3 main.py
```

The program will process all images in the `process_me` directory, generate headshots, and segment the facets of each detected face. The processed images will be moved to the `archive` directory.

## Cleanup Script

A cleanup script (`cleanup.sh`) is included in the `scripts/` directory to delete all processed images. You can run it with the following command:

```
sh ./scripts/cleanup.sh
```

By default, this script will not delete the images in the `archive` directory unless the `-all` option is used.

```
sh ./scripts/cleanup.sh -all
```

## Contributing

Contributions to this project are welcome. Please open an Issue to discuss proposed changes before making a Pull Request.

## License

This project is licensed under the terms of the MIT license.

### Requirements.txt
```
dlib==19.22.0
opencv-python==4.5.3.56
```