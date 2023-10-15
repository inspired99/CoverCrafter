from cover_generator import CoverGenerator


def main():
    params = {
        "video_path": "/home/ubuntu/88.mp4",
        "text": "Чай и сахар - наши друзья"
    }

    cover_generator = CoverGenerator()
    cover_generator(params)


if __name__ == "__main__":
    main()
