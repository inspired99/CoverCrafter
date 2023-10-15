from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('about/', views.about, name='about'),
        path('download/', views.download, name='download'),
        path('run/', views.run_pipeline, name='run'),
        path('report/', views.report, name='report'),
]
