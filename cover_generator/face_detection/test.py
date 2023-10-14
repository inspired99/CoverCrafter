from face_detection import FaceDetectionModel

import cv2
import numpy as np


def test():
    face_detection_model = FaceDetectionModel()
    img = np.array(cv2.imread("/home/cats/Downloads/Screenshot from 2023-10-14 01-10-19.png"))
    print(type(img))
    detections = face_detection_model(img)

    print(detections)

    if detections:
        cv2.rectangle(
            img,
            detections["face_1"]["facial_area"][:2],
            detections["face_1"]["facial_area"][2:4],
            (255, 0, 0), 2
        )
        cv2.imwrite("/home/cats/Downloads/detected_face.png", img)


if __name__ == "__main__":
    test()
