class VideoUpload {
    constructor(input) {
        this.input = input;
        // размер отрезка видео. 10-20 mb идеально
        this.max_length = 10 * (1024 * 1024);
    }

    upload() {
        this.make_progress_bar();
        this.init_upload();
    }

    init_upload() {
        this.file = this.input.files[0];
        this.file_name = add_hash_to_file_name(this.file.name);
        this.upload_helper(0, null);
    }

    upload_helper(start, given_path) {
        let end = 0,
            self = this,
            actual_path = given_path,
            form_data = new FormData(),
            next_chunk = start + this.max_length + 1,
            curr_chunk = this.file.slice(start, next_chunk),
            upload_chunk = start + curr_chunk.size,
            file_size = this.file.size;

        let file_name = this.file_name;

        console.log("FILENAME: ");
        console.log(file_name);

        end = upload_chunk < file_size ? 0 : 1;

        form_data.append('file', curr_chunk);
        form_data.append('filename', file_name);
        form_data.append('end', end);
        form_data.append('actual_path', actual_path);
        form_data.append('next_slice', next_chunk);


        console.log(form_data)
        $('.filename').text(file_name)
        $('.textbox').html("– Загрузка файла...<br>")
        // $('.textbox').html("Загрузка <br> файла...")

        $.ajaxSetup(
            {
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            }
        )

        $.ajax(
            {
                xhr: () => {
                    let xhr = new XMLHttpRequest();
                    xhr
                        .upload
                        .addEventListener(
                            'progress',
                            (e) => {
                                if (e.lengthComputable) {
                                    const percent =
                                        self.file.size < self.max_length ?
                                            Math.round((e.loaded / e.total) * 100) :
                                            Math.round((upload_chunk / self.file.size) * 100);

                                    $('.progress-bar')
                                        .css('width', percent + '%')
                                        .text(percent + '%');
                                }
                            }
                            )

                    return xhr;
                },
                url: '/generate/',
                type: 'POST',
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                data: form_data,
                error: (xhr) => {
                    alert(xhr.statusText);
                },
                success: (res) => {
                    console.log("RESPONSE")
                    console.log(res);

                    if (next_chunk < self.file.size) {
                        console.log(res);

                        actual_path = res.actual_path;
                        self.upload_helper(next_chunk, actual_path);
                    }
                    // Здесь видео уже загрузилось.
                    // Отображаем текст и выводим кнопку загрузки заглушки.
                    else {
                        console.log("VIDEO DONE");
                        $('.textbox').append("– " + res.data + "<br>");
                        this.show_pipeline_button();
                    }
                }
            }
        )
    }


    make_progress_bar() {
        document
            .getElementById('uploaded_files')
            .innerHTML =
            `<div class="file-details">
                <p class="filename"></p>
                <div class="progress" style="margin-top: 5px; height: 40px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-warning"
                         role="progressbar"
                         aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%">
                    </div>
                </div>
                <small class="textbox"></small>
            </div>`;
    }

    show_pipeline_button() {
        document
            .getElementById('run_pipeline')
            .hidden = false;
    }
}

class PipelineRunner {
    run() {
        this.show_spinner();
        this.hide_pipeline_button();

        let self = this,
            form_data = new FormData();

        form_data.append('pipeline_status', 'empty');

        $.ajaxSetup(
            {
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value,
                }
            }
        )

        $.ajax(
            {
                xhr: () => {
                    let xhr = new XMLHttpRequest();
                    return xhr;
                },
                url: '/generate/run/',
                type: 'POST',
                dataType: 'json',
                cache: false,
                processData: false,
                contentType: false,
                data: form_data,
                error: (xhr) => {
                    console.log("smth went wrong :(");
                    console.log(xhr);
                },
                success: (res) => {
                    console.log("RESPONSE INSIDE FUNC")
                    console.log(res);
                    if (res.pipeline_status === "done") {
                        this.hide_spinner();
                        this.show_result_file();
                    }
                    else {
                        self.run();
                    }

                }
            }
        )
    }

    show_result_file() {
        document
            .getElementById('result_file')
            .hidden = false;
    }

    show_spinner() {
        document
            .getElementById('spinner-box')
            .hidden = false;
    }

    hide_spinner() {
        document
            .getElementById('spinner-box')
            .hidden = true;
    }

    hide_pipeline_button() {
        document
            .getElementById('run_button')
            .hidden = true;
    }
}

function add_hash_to_file_name(full_file_name) {
    // hash stuff
    const length = 8;
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = alphabet.length;
    let hash = '_';

    for (let i = 0; i < length; i++) {
      hash += alphabet.charAt(Math.floor(Math.random() * charactersLength));
   }

    // избавляемся от расширения
    const file_ext = full_file_name.split(".").slice(-1)[0];
    const file_name_without_ext = full_file_name.split(".").slice(0, -1).join(".");

    // добавляем к имени хэш
    const result_file_name = file_name_without_ext + hash + "." + file_ext;

    return result_file_name;
}

(function ($) {
    $('#submit').on('click', (event) => {
        event.preventDefault();
        const uploader = new VideoUpload(document.querySelector('#video_upload'));

        console.log("UPLOADING VIDEO")
        console.log(document.querySelector('#video_upload'));

        uploader.upload();
    });
})(jQuery);


(function ($){
    $('#run_button').on('click', (event) => {
        event.preventDefault();
        const runner = new PipelineRunner();

        console.log("RUNNING PIPELINE INSIDE $");
        runner.run();
    });
})(jQuery)


$(document).ready(function() {
    $('#cover_options_form').submit(function(event) {
        event.preventDefault();  // Prevent traditional form submission

        const formData = new FormData(this);

        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('.textbox').append("– Параметры для генерации обложки успешно отправлены \n");
            },
            error: function(error) {
            }
        });
    });
});
