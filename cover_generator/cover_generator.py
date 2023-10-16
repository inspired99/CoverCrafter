from cover_generator.merge_text_and_image.text_and_image_merger import Joiner
from cover_generator.summarization.token_classificaton import TokenClassification
from cover_generator.summarization.clickbaiter import ClickBaitGenerator
from cover_generator.image_matting.image_matting import ImageMattingModel
from cover_generator.face_detection.face_detection import FaceDetectionModel
from cover_generator.image_generation.diffusion_model.diffusion_model import DiffusionModel
from cover_generator.nsfw_detector.nsfw_detector import NSFWDetector
from cover_generator.frame_stitching.frame_background import FrameBackground

import cv2
import numpy as np


class CoverGenerator:
    COVER_PATH = 'result/cover.png'

    def __init__(self, debug=False):
        self.debug = debug

        self.image_matting_model = ImageMattingModel()
        self.face_detection_model = FaceDetectionModel()
        self.clickbait_generator_model = ClickBaitGenerator()
        self.token_classification = TokenClassification()
        self.merger_image_and_text = Joiner()
        self.diffusion_model = DiffusionModel()
        self.frame_background = FrameBackground()
        self.nsfw_detector = NSFWDetector()

    def __call__(self, params):
        """
        params:
            - video_path
            - description
            - text style
            - background style
        """

        # Get video frame shape
        video_frame_shape = self.get_video_frame_shape(params["video_path"])

        # Find frame with a person
        if params["face_path"] is not None:
            frame_with_person = cv2.imread(params["face_path"])
        else:
            frame_with_person = self.detect_person(params["video_path"])

        person_mask = None
        if frame_with_person is not None:
            person_mask = self.get_person_mask(frame_with_person)

        # Summarize description for clickbait phrase
        clickbait_sentence = self.clickbait_generator_model.inference(params["text"])

        # Extract keywords for prompt
        keywords_for_generation = self.token_classification.inference(params["text"])

        # Generate background
        background_type = params['background_type']
        if background_type == 'generate_bg':
            background = self.diffusion_model.generate_image(keywords_for_generation, *video_frame_shape[:2])
            background = cv2.resize(np.array(background), (video_frame_shape[1], video_frame_shape[0]))
            background = cv2.cvtColor(background, cv2.COLOR_BGR2RGB)
        elif background_type == 'use_frames':
            background = self.frame_background.get_background(params['video_path'])
        else:
            raise RuntimeError("Unknown background type")

        # Decrease brightness
        background = self.lower_brightness(background)

        # Merge background and person
        background_and_person = background
        if person_mask is not None:
            background_and_person = self.merge_background_person(background, frame_with_person, person_mask)

        # Draw stylized text on image (background + person)
        text_decor = params["text_decor"]
        cover = self.merger_image_and_text.run(background_and_person, clickbait_sentence, text_color=text_decor,
                                               path_to_ttf='cover_generator/data/main_font.ttf')

        if self.debug:
            print("Video frame shape:", video_frame_shape)

            cv2.imwrite("frame_with_person.png", frame_with_person)
            cv2.imwrite("person_mask.png", person_mask * 255)

            print("Clickbait sentence:", clickbait_sentence)
            print("Keywords for generation:", keywords_for_generation)

            cv2.imwrite("background.png", background)
            cv2.imwrite("background_and_person.png", background_and_person)
            cv2.imwrite("cover.png", cover)

        # NSFW detector for final cover
        if self.nsfw_detector(cover):
            raise RuntimeError(
                "Non-appropriated content was generated."
                "Run generation again or change video description."
            )

        # Save cover for web application
        cv2.imwrite(self.COVER_PATH, cover)

        return

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
            if num_frames % 10 == 0:
                detections = self.face_detection_model(frame)

                if len(detections) == 1 and (best_frame is None or highest_confidence < detections['face_1']['score']):
                    best_frame = frame
                    highest_confidence = detections['face_1']['score']

            if num_frames > 10000:
                break

        return best_frame

    def get_person_mask(self, frame):
        """
        Extract person (in other words, remove background).
        """
        return np.expand_dims(self.image_matting_model(frame), axis=2) / 255

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

    @staticmethod
    def lower_brightness(image):
        image = cv2.convertScaleAbs(image, alpha=1, beta=-30)
        return cv2.GaussianBlur(image, (11, 11), 0)
