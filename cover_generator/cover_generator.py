from image_matting.image_matting_model import ImageMattingModel


class CoverGenertor:
    def __int__(self):
        self.image_matting_model = ImageMattingModel()

    def __call__(self, params):
        return self.image_matting_model(params.image)
