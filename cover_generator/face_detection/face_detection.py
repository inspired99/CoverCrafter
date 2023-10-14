from retinaface import RetinaFace


class FaceDetectionModel:
    """
    Class that performs face detection on a provided image.

    Used libraries:
        https://pypi.org/project/retina-face/
        https://github.com/deepinsight/insightface/tree/master/detection/retinaface
    """

    def __init__(self):
        self.model = RetinaFace.build_model()

    def __call__(self, img):
        return RetinaFace.detect_faces(img, model=self.model)
