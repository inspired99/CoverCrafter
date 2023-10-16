from cover_generator import CoverGenerator


def main():
    params = {
        "video_path": "/home/ubuntu/example.mp4",
        "text": ("Интервью со школьниками. Ребята рассказывают о своих уроках, "
                 "а учителя жалуются на плохое поведение детей."),
        'background_type': 'generate_bg',
        'text_decor': 'white'
    }

    cover_generator = CoverGenerator(debug=True)
    cover_generator(params)


if __name__ == "__main__":
    main()
