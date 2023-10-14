from cover_generator import CoverGenerator

import cv2


def test():
    video = cv2.VideoCapture("/home/cats/Downloads/train_dataset_train_dataset/rutube_hackathon_sochi/videos/16.mp4")
    cover_generator = CoverGenerator()
    frame = cover_generator.detect_person(video)
    mask = cover_generator.extract_person(frame)
    cv2.imwrite("/home/cats/Downloads/tmp1.png", frame)
    cv2.imwrite("/home/cats/Downloads/tmp2.png", mask)


if __name__ == "__main__":
    test()
