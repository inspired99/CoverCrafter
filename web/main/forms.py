from django import forms

from main.models import UserPhoto


class CoverForm(forms.ModelForm):
    BACKGROUND_CHOICES = (
        ("generate_bg", "Сгенерировать фон"),
        ("use_frames", "Использовать кадры из видео"),
    )
    TEXT_CHOICES = (
        ("dark_decor", "Темный"),
        ("light_decor", "Светлый"),
        ("color_decor", "Яркий")
    )
    COVER_STYLE_CHOICES = (
        ("no_style", "Без стиля"),
        ("anime_style", "Аниме"),
    )

    background_type = forms.ChoiceField(
        label="Тип фона",
        widget=forms.Select(attrs={"class": "form-control"}),
        initial="generate_bg",
        choices=BACKGROUND_CHOICES,
        required=True
    )

    description_text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control', 'rows': 5, 'cols': 40,
        }),
        label="Текстовое сопровождение",
        required=True
    )

    text_decor = forms.ChoiceField(
        label="Оформление текста",
        widget=forms.Select(attrs={"class": "form-control"}),
        initial="dark_decor",
        choices=TEXT_CHOICES,
        required=True
    )

    face_picture = forms.ImageField(
        label='Выберите фото для загрузки',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'file-upload btn btn-primary',
            }),
        required=False
    )

    class Meta:
        model = UserPhoto
        fields = ['face_picture', 'description_text', 'text_decor', 'background_type']
