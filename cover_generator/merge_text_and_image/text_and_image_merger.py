from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import cv2
import os


class Joiner:
    def __init__(self, width_of_line=30, path_to_ttf=None, background_color=(236, 78, 32)):
        self.width_of_line = width_of_line  # сколько символов в одной линии для текста
        self.background_color = background_color  # задний фон текста
        if path_to_ttf is None:  # стиль текста
            self.path_to_ttf = os.path.join(cv2.__path__[0], 'qt', 'fonts', 'DejaVuSans.ttf')
        else:
            self.path_to_ttf = path_to_ttf

    def run(self, img, text):
        with Image.open(img) as img:
            width, height = img.size
            draw = ImageDraw.Draw(img)

            # style of text
            font = ImageFont.truetype(self.path_to_ttf, size=200)

            # position of text
            textwidth, textheight = draw.textsize(text, font)
            lines = textwrap.wrap(text, width=self.width_of_line)
            start_height = height - 2 * (len(lines) * textheight)

            np_image = np.array(img)
            avg_color_per_row = np.average(np_image, axis=0)
            avg_color = np.average(avg_color_per_row, axis=0)
            if np.mean(avg_color) < 128:
                text_color = "white"
            else:
                text_color = "black"

            # Add each line to the image
            for i, line in enumerate(lines):
                line_width, line_height = font.getsize(line)
                position = (width - line_width - 10, start_height + i * line_height)
                position2 = (width - line_width - 40, start_height + i * line_height + 10)
                draw.rectangle([position, (position[0] + line_width, position[1] + line_height)],
                               fill=self.background_color)
                draw.text(position, line, font=font, fill='blue')  # границы букв
                draw.text(position2, line, font=font, fill=text_color)

            # Save the image
            # img.save('image_with_text.jpg')
            return img
