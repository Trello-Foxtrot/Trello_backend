from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('sign_up', views.sign_up)
]
