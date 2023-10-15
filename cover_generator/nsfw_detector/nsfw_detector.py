from os.path import exists

import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub


class NSFWDetector:
    """
    Class for detecting prohibited content (nudes, porno, ...).

    Used library:
        https://github.com/GantMan/nsfw_model
    """

    TRAINED_MODEL_PATH = "./cover_generator/nsfw_detector/nsfw_detector_weights.h5"
    IMAGE_DIM = 224
    CATEGORIES = ['drawings', 'hentai', 'neutral', 'porn', 'sexy']

    def __init__(self):
        if not exists(self.TRAINED_MODEL_PATH):
            raise RuntimeError(
                "Load weights for NSFW detector from "
                "https://github.com/GantMan/nsfw_model/releases/tag/1.1.0"
            )

        self.model = tf.keras.models.load_model(
            self.TRAINED_MODEL_PATH,
            custom_objects={'KerasLayer': hub.KerasLayer},
            compile=False
        )

    def __call__(self, image):
        processed_image = self.process_image(image)
        confidences_per_category = self.classify(processed_image)
        return self.detect_nsfw(confidences_per_category)

    def process_image(self, image):
        processed_image = cv2.resize(image, (self.IMAGE_DIM, self.IMAGE_DIM))
        processed_image = processed_image / 255
        return np.asarray(processed_image)[None, ...]

    def classify(self, image):
        confidences = self.model.predict(image)[0]

        confidences_per_category = {}
        for category_ind, confidence in enumerate(confidences):
            confidences_per_category[self.CATEGORIES[category_ind]] = float(confidence)

        return confidences_per_category

    @staticmethod
    def detect_nsfw(confidences):
        return confidences['sexy'] + confidences['hentai'] + confidences['porn'] > 0.3
