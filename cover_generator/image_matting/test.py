from image_matting import ImageMattingModel

import cv2


def test():
    image_matting_model = ImageMattingModel()
    img = cv2.imread("~/Downloads/Screenshot from 2023-10-14 01-10-19.png")
    mask = image_matting_model(img)
    cv2.imwrite("~/Downloads/mask.png", mask)


if __name__ == "__main__":
    test()
