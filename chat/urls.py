# -*- coding: utf-8 -*-
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('history/', views.chat_history, name='history'),
]
