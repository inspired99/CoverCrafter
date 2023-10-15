from PIL import Image, ImageDraw, ImageFont
import numpy as np
import textwrap
import cv2
import os


class Joiner:
    def __init__(self, width_of_line=30, background_color=(236, 78, 32)):
        self.width_of_line = width_of_line  # сколько символов в одной линии для текста
        self.background_color = background_color  # задний фон текста

    def preprocess_text(self, text):
        splitted = text.split(' ')
        result = []
        k = 0
        for i, word in enumerate(splitted):
            result.append(word)
            if len(word) > 3 and i != len(splitted) - 1:
                if k >= 1:
                    result.append('\n')
                    k = 0
                else:
                    k += 1
                    result[-1] = result[-1] + ' '
            else:
                result[-1] = result[-1] + ' '
        return ''.join(result)

    def run(self, img, text,  text_color, path_to_ttf, text_size=75):
        offset = 20
        with Image.open(img) as img:
            width, height = img.size
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(path_to_ttf, size=text_size)
            preprocessed_text = self.preprocess_text(text).split('\n')

            lines = []
            for i in preprocessed_text:
                if not i:
                    continue
                if len(i) >= 20:
                    splitted_i = i.split(' ')
                    if splitted_i:
                        lines.append(' '.join(splitted_i[:-1]))

                    lines.append(splitted_i[-1])
                    continue
                lines.append(i)

            start_height = int(height * 4 / 10)

            # Add each line to the image
            for i, line in enumerate(lines):
                line_width, line_height = font.getsize(line)
                position = (width - line_width - offset, start_height + i * line_height)
                position2 = (width - line_width - 4 - offset, start_height + i * line_height + 4)
                # draw.rectangle([position, (position[0] + line_width, position[1] + line_height)],
                #                 fill=background_color)
                draw.text(position, line, font=font, fill='black')  # границы букв
                draw.text(position2, line, font=font, fill=text_color)

            # Save the image
            # img.save('image_with_text.jpg')
            return img
