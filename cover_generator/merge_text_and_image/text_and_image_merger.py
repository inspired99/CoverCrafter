from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import cv2
import os


class Joiner:
    def __init__(self, base_font_size=200, width_of_line=30):
        self.base_font_size = base_font_size
        self.width_of_line = width_of_line

    def run(self, img, text):
        with Image.open(img) as img:
            width, height = img.size
            draw = ImageDraw.Draw(img)

            # style of text
            font_path = os.path.join(cv2.__path__[0], 'qt', 'fonts', 'DejaVuSans.ttf')
            font = ImageFont.truetype(font_path, size=200)

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
                position = (width - line_width - 10, start_height + i*line_height)
                draw.text(position, line, font=font, fill=text_color)

            # Save the image
            # img.save('image_with_text.jpg')
            return img
