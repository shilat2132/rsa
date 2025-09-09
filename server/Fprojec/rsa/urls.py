from django.urls import path
from . import views

urlpatterns = [
    path('keyGeneration/', views.key, name='key'),
    path('decryption/', views.decryption, name='decryption'),
    path('encryption/', views.encryption, name='encryption'),
]