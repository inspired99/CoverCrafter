# Video cover generation with CoverCrafter

## Description

Web application for cover generation, based on the provided video, description, and optional parameters.

It can be handy for people without design experience or for those who wish to get a cool cover as soon as possible.

The resulting cover consists of:
- Speaker 
- Clickbait Text
- Nice and High-Resolution Background

Please, take a look at our [presentation](CoverCrafter.pdf) for more details and examples.

## UI

<img width="956" alt="Снимок экрана 2023-10-16 в 15 55 22" src="https://github.com/inspired99/CoverCrafter/assets/64794482/059d822b-4581-4bff-aa8c-e0d4ea4b2057">

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
  - Frontend
  - Backend
- Cover generation module
  - People Face detection - [RetinaFace](https://github.com/serengil/retinaface)
  - Human image matting (segmentation) - [MODNet](https://github.com/ZHKKKe/MODNet)
  - Text summarization for keywords - [PyMorphy2](https://pypi.org/project/pymorphy2/)
  - Text summarization for a clickbait phrase - [T5-Russian](https://huggingface.co/UrukHan/t5-russian-summarization)
  - Background generation - [Kandinsky 2.2](https://huggingface.co/docs/diffusers/api/pipelines/kandinsky_v22)
  - Translation prompts - [FSMT](https://huggingface.co/docs/transformers/model_doc/fsmt)

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

## Generation Example

Here you can see an automatic generation of video preview by user with text prompt about cooking video. The person is taken from video, background was generated automatically and clickbait was also generated based on user preferences and video topic

![1](https://github.com/inspired99/CoverCrafter/assets/64794482/2d1a82d6-099f-4bc6-afec-37ffa2002172)

## Technology stack
```
🐍 Python [Django]

⏳ Javascript [AJAX]

🤗 HuggingFace [Diffusers]
```


## Our Dream Team 

1. Vadim Shabashov (ITMO) - Image Matting + People Detection

2. Elisey Evseev (ITMO) - Background Generation + Processing Text Background

3. Anvar Tliamov (ITMO) - Text summarization + Prompt summarization

4. Dmitriy Saifulin (ITMO) - Backend + Frontend
   
