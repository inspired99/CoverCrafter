import mimetypes
import os
from time import sleep

from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render

from cover_generator.cover_generator import CoverGenerator
from .forms import CoverForm
from .models import VideoFile


def index(request):
    if not os.path.exists("media"):
        os.makedirs("media")

    cover_options_form = CoverForm()
    video_form = VideoFile()

    if request.method == 'POST':
        if 'actual_path' in request.POST:
            end = request.POST['end']
            file = request.FILES['file'].read()
            file_name = request.POST['filename']
            actual_path = request.POST['actual_path']
            next_slice = request.POST['next_slice']

            request.session['file_name'] = file_name

            if not file or not file_name or not actual_path or not end or not next_slice:
                inv_dict = {'data': 'Invalid request'}
                response = JsonResponse(inv_dict)
                return response

            if actual_path == 'null':
                path = 'media/' + file_name

                with open(path, 'wb+') as f:
                    f.write(file)

                video_form.actual_path = file_name
                video_form.eof = end
                video_form.name = file_name
                video_form.save()

                if int(end):
                    message = 'Загрузка прошла успешно'
                    succ_dict = {'data': message, 'actual_path': file_name}
                    response = JsonResponse(succ_dict)
                else:
                    response = JsonResponse({'actual_path': file_name})

                return response

            path = 'media/' + actual_path
            model_id = VideoFile.objects.get(actual_path=actual_path)

            if model_id.name == file_name:
                if not model_id.eof:
                    with open(path, 'ab+') as f:
                        f.write(file)
                    if int(end):
                        model_id.eof = int(end)
                        model_id.save()

                        message = 'Загрузка прошла успешно'
                        succ_dict = {'data': message, 'actual_path': model_id.actual_path}
                        response = JsonResponse(succ_dict)
                    else:
                        response = JsonResponse(
                            {'actual_path': model_id.actual_path}
                        )
                    return response

                eof_dict = {'data': 'Invalid request! Cause: end of the file found.'}
                response = JsonResponse(eof_dict)

                return response

            no_such_dict = {'data': 'No such file :('}
            return JsonResponse(no_such_dict)
        elif 'background_type' in request.POST:
            cover_options_form = CoverForm(request.POST, request.FILES)
            print(f"valid: {cover_options_form.is_valid()}")
            if cover_options_form.is_valid():
                cover_options_form.save()
                for k, v in cover_options_form.cleaned_data.items():
                    if v:
                        request.session[k] = v if k != 'face_picture' else v.name

    context = {
        "cover_options_form": cover_options_form,
        "video_form": video_form,
        "navbar": 'generate'
    }

    return render(request, 'index.html', context)


def download(request):
    filename = 'cover.png'

    if filename:
        file_path = 'result/' + filename
        path = open(file_path, 'rb')

        file_type = mimetypes.guess_type(file_path)

        response = HttpResponse(path, content_type=file_type)
        response['Content-Disposition'] = "attachment; filename=%s" % filename

        return response

    return render(request, 'index.html')


def run_pipeline(request):
    # TODO: change to NONE
    # 1. MODE = "FAKE" псевдо-работа, зависание на 10 секунд
    # 2. MODE = "NONE" или что угодно другое, чтобы запустить весь пайплайн
    MODE = "NONE"

    f_name = request.session['file_name']
    params = {}
    params['video_path'] = f"media/{request.session['file_name']}"
    params['face_path'] = f"media/face/{request.session['face_picture']}" if 'face_picture' in request.session else None
    params['background_type'] = request.session['background_type']
    params['text'] = request.session['description_text']
    params['text_decor'] = request.session['text_decor']
    if f_name:
        print((10 * "-") + "PIPELINE IS RUNNING" + (10 * "-"), "for file", f_name)
        if MODE == "FAKE":
            sleep(5)
        else:
            cg = CoverGenerator()
            cg(params)
        return JsonResponse({"pipeline_status": "done"})

    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html', {'navbar': 'about'})


def report(request):
    return render(request, 'report.html', {'navbar': 'report'})
