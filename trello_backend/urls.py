from django.urls import path
from .views import homePageView


urlpatterns = [
    path('<str:msg>', homePageView, name='login')
]