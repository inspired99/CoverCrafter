import random
import cv2
import numpy as np


class FrameBackground:
    """
    Stitching two random frames into one with center crop or just pick random frame from video
    """

    def __init__(self):
        self.mode = "double-frame"

    def random_choice(self):
        if random.random() > 0.5:
            self.mode = "single-frame"

    def get_single_frame(self, path_to_video):
        vid_cap = cv2.VideoCapture(path_to_video)
        success, image = vid_cap.read()

        count = 0
        total_frames = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frame = random.randrange(total_frames)

        while success:
            if count == random_frame:
                break
            success, image = vid_cap.read()
            count += 1

        return image

    @staticmethod
    def merge_images(frames):
        margin = 40
        cropped_images = []
        for img in frames:
            img_y = img.shape[1] // 2
            cropped_img = img[:, img_y - img.shape[1] // 4: img_y + img.shape[1] // 4]
            cropped_images.append(cropped_img)

        result = cv2.hconcat(cropped_images)
        result_y = result.shape[1] // 2

        blur_first = cv2.GaussianBlur(result, (31, 31), 0)
        result[:, result_y - margin: result_y + margin] = 0
        out_first = np.where(result != 0, result, blur_first)

        blur_second = cv2.GaussianBlur(out_first, (15, 15,), 0)
        out_first[:, result_y - margin * 2: result_y - margin] = 0
        out_first[:, result_y + margin: result_y + margin * 2] = 0
        out_second = np.where(out_first != 0, out_first, blur_second)

        blur_final = cv2.GaussianBlur(out_second, (5, 5,), 0)
        out_second[:, result_y - margin * 3: result_y - margin * 2] = 0
        out_second[:, result_y + margin * 2: result_y + margin * 3] = 0
        final = np.where(out_second != 0, out_second, blur_final)

        return final

    def get_double_frame(self, path_to_video):
        vid_cap = cv2.VideoCapture(path_to_video)
        total_frames = int(vid_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        random_frames = random.sample(range(0, total_frames), 2)

        success, image = vid_cap.read()
        count = 0
        frames = []

        while success:
            if count in random_frames:
                frames.append(image)
                if len(frames) == 2:
                    break

            success, image = vid_cap.read()
            count += 1

        merged_image = self.merge_images(frames)
        return merged_image

    def get_background(self, path_to_video):
        self.random_choice()
        if self.mode == 'single-frame':
            background = self.get_single_frame(path_to_video)
        else:
            background = self.get_double_frame(path_to_video)

        return background
