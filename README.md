# Video cover generation

## Description

Web application for cover generation, based on the provided video, description, and optional parameters.

It can be handy for people without design experience or for those who wish to get a cool cover as soon as possible.

The resulting cover consists of:
- Speaker
- Text
- Background

Please, take a look at our [presentation](CoverCrafter.pdf) for more details and examples.

## UI

The user is asked to provide the following parameters:
- Video
- Description
 
    It is used for text and cover background generation.
- Background style:
  - Generate background using a diffusion model
  - Create a background from one or two stitched video frames
- Text color
- User photo [optional]

    Cut the user from the provided photo rather than selecting a random person from the video.

## Components

- Web application
- Cover generation module
  - Person detection - RetinaFace
  - Human image matting (segmentation) - MODNet
  - Text summarization for keywords - PyMorphy2
  - Text summarization for a clickbait phrase - T5-Russian
  - Background generation - Kandinsky 2.2

## Web service start

For running web service, run the following command from the project directory:
```
python3 manage.py runserver [port]
```

A port can be, for example, 8080. The web server can be accessed on:
```
http://127.0.0.1:8080/generate
```

NOTE: the used models are heavy, so two video cards 32 GB are needed.

## Technology stack
```
🐍 Python [Django]

⏳ Javascript [AJAX]
```
