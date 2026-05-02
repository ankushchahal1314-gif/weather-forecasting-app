from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), # Ye seedha aapke 'home' function ko chalayega
]