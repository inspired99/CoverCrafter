from summarization.token_classificaton import TokenClassification
from summarization.clickbaiter import ClickBaitGenerator
from image_matting.image_matting import ImageMattingModel
from face_detection.face_detection import FaceDetectionModel


class CoverGenerator:
    def __int__(self):
        self.image_matting_model = ImageMattingModel()
        self.face_detection_model = FaceDetectionModel()
        self.clickbait_generator_model = ClickBaitGenerator()
        self.token_classification = TokenClassification()

    def __call__(self, params):
        """
        params:
            - video
            - description
            - text style
            - background style
        """

        # NSFW detector for description (NLP)

        # Find frame with a person
        frame = self.detect_person(params.video)

        # Extract person (segmentation, matting)
        person = self.extract_person(frame)

        # Summarize description for clickbait phrase
        clickbait_sentence = self.clickbait_generator_model.inference(params.text)

        # Extract keywords for prompt
        keywords_for_generation = self.token_classification.inference(params.text)

        # Generate background

        # Merge background and person

        # Apply text style

        # Apply image style

        # Draw stylized text on image (background + person)
        cover = ...

        # NSFW detector for final cover (CV)

        return cover

    def detect_person(self, video):
        """
        Find frame with a single person and the most detector confidence
        """

        best_frame = []
        for frame in video:
            detections = self.face_detection_model(frame)

            if len(detections) == 1:
                best_frame = frame

        return best_frame

    def extract_person(self, frame):
        """
        Extract person (in other words, remove background).
        """

        return self.image_matting_model(frame)
