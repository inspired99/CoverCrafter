import os
import cv2
import numpy as np

import onnxruntime


class ImageMattingModel:
    """
    Class for finding person mask from image (segmenting/matting).

    Used libraries:
        https://github.com/ZHKKKe/MODNet
    """
    TRAINED_ONNX_MODEL_PATH = "./pretrained/modnet_photographic_portrait_matting.onnx"

    def __init__(self, ref_size=512):
        # Resizing size
        self.ref_size = ref_size

        # Check trained model existence
        if not os.path.exists(self.TRAINED_ONNX_MODEL_PATH):
            raise RuntimeError(
                "Download trained onnx model for ImageMattingModel from "
                "https://drive.google.com/drive/folders/1umYmlCulvIFNaqPjwod1SayFmSRHziyR"
            )

        # Initialize session and get prediction
        self.session = onnxruntime.InferenceSession(self.TRAINED_ONNX_MODEL_PATH, None)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def __call__(self, image):
        # Initial image shape
        image_h, image_w, _ = image.shape

        # Image preprocessing
        resized_image = self.preprocessing(image, image_h, image_w)

        # Run matting
        inference_result = self.session.run([self.output_name], {self.input_name: resized_image})

        # Process matte
        resized_matte = (np.squeeze(inference_result[0]) * 255).astype('uint8')
        matte = cv2.resize(resized_matte, dsize=(image_w, image_h), interpolation=cv2.INTER_AREA)

        return matte

    def preprocessing(self, image, image_h, image_w):
        # Change colors sequence
        processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Make 3 channels
        if len(processed_image.shape) == 2:
            processed_image = processed_image[:, :, None]
        if processed_image.shape[2] == 1:
            processed_image = np.repeat(processed_image, 3, axis=2)
        elif processed_image.shape[2] == 4:
            processed_image = processed_image[:, :, 0:3]

        # Normalize values to scale it between -1 to 1
        processed_image = (processed_image - 127.5) / 127.5

        # New shape
        x, y = self.get_scale_factor(image_h, image_w)

        # Resize image
        processed_image = cv2.resize(processed_image, None, fx=x, fy=y, interpolation=cv2.INTER_AREA)

        # Prepare input shape
        processed_image = np.transpose(processed_image)
        processed_image = np.swapaxes(processed_image, 1, 2)
        processed_image = np.expand_dims(processed_image, axis=0).astype('float32')

        return processed_image

    def get_scale_factor(self, image_h, image_w):
        """
        Get x_scale_factor and y_scale_factor to resize image
        """

        if max(image_h, image_w) < self.ref_size or min(image_h, image_w) > self.ref_size:
            if image_w >= image_h:
                image_rh = self.ref_size
                image_rw = int(image_w / image_h * self.ref_size)
            elif image_w < image_h:
                image_rw = self.ref_size
                image_rh = int(image_h / image_w * self.ref_size)
        else:
            image_rh = image_h
            image_rw = image_w

        image_rw = image_rw - image_rw % 32
        image_rh = image_rh - image_rh % 32

        x_scale_factor = image_rw / image_w
        y_scale_factor = image_rh / image_h

        return x_scale_factor, y_scale_factor
