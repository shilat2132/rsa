from django.urls import path
from . import views

urlpatterns = [
    path('key_generate/', views.key, name='key'),
    path('decription/', views.decription, name='decription'),
    path('encription/', views.decription, name='encription'),
]