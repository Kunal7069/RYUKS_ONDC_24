from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("analyse/", analyse, name="home"),
    path("history/", history, name="history"),
    path("parameter/", parameter, name="parameter"),
]
