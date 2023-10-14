from image_matting.image_matting import ImageMattingModel
from face_detection.face_detection import FaceDetectionModel


class CoverGenerator:
    def __init__(self):
        self.image_matting_model = ImageMattingModel()
        self.face_detection_model = FaceDetectionModel()

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

        # Extract keywords for prompt

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

    def extract_person(self, frame):
        """
        Extract person (in other words, remove background).
        """

        return self.image_matting_model(frame)
