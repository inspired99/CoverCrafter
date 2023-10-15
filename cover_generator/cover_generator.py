from merge_text_and_image.text_and_image_merger import Joiner
from summarization.token_classificaton import TokenClassification
from summarization.clickbaiter import ClickBaitGenerator
from image_matting.image_matting import ImageMattingModel
from face_detection.face_detection import FaceDetectionModel
from image_generation.diffusion_model.diffusion_model import DiffusionModel
from nsfw_detector.nsfw_detector import NSFWDetector

import cv2


class CoverGenerator:
    def __init__(self):
        self.image_matting_model = ImageMattingModel()
        self.face_detection_model = FaceDetectionModel()
        self.clickbait_generator_model = ClickBaitGenerator()
        self.token_classification = TokenClassification()
        self.merger_image_and_text = Joiner()
        self.diffusion_model = DiffusionModel()
        self.nsfw_detector = NSFWDetector()

    def __call__(self, params):
        """
        params:
            - video_path
            - description
            - text style
            - background style
        """

        # NSFW detector for description (NLP)

        # Get video frame shape
        video_frame_shape = self.get_video_frame_shape(params["video_path"])

        # Find frame with a person
        frame_with_person = self.detect_person(params["video_path"])

        # Extract person (segmentation, matting)
        person_mask = self.get_person_mask(frame_with_person)

        # Summarize description for clickbait phrase
        clickbait_sentence = self.clickbait_generator_model.inference(params["text"])

        # Extract keywords for prompt
        keywords_for_generation = self.token_classification.inference(params["text"])

        # Generate background
        background = self.diffusion_model.generate_image(keywords_for_generation, *video_frame_shape[:2])

        # Merge background and person
        background_and_person = self.merge_background_person(background, frame_with_person, person_mask)

        # Apply image style

        # Draw stylized text on image (background + person)
        cover = self.merger_image_and_text.run(background_and_person, clickbait_sentence,
                                               path_to_ttf='cover_generator/data/main_font.ttf')

        # NSFW detector for final cover
        if self.nsfw_detector(cover):
            raise RuntimeError(
                "Non-appropriated content was generated."
                "Run generation again or change video description."
            )

        return cover

    def detect_person(self, video_path):
        """
        Find frame with a single person and the most detector confidence
        """

        video = cv2.VideoCapture(video_path)

        best_frame = None
        highest_confidence = None
        num_frames = 0

        while True:
            has_frame, frame = video.read()

            if not has_frame:
                break

            num_frames += 1
            if num_frames % 2000 == 0:
                detections = self.face_detection_model(frame)

                if len(detections) == 1 and (best_frame is None or highest_confidence < detections['face_1']['score']):
                    best_frame = frame
                    highest_confidence = detections['face_1']['score']

        return best_frame

    def get_person_mask(self, frame):
        """
        Extract person (in other words, remove background).
        """
        return self.image_matting_model(frame)

    @staticmethod
    def get_video_frame_shape(video_path):
        video = cv2.VideoCapture(video_path)
        has_frame, frame = video.read()

        if not has_frame:
            raise RuntimeError("Empty video was provided")

        return frame.shape

    @staticmethod
    def merge_background_person(background, frame_with_person, person_mask):
        return background * (1 - person_mask) + frame_with_person * person_mask
