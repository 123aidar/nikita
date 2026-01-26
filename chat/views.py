# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Message

@login_required
def chat_history(request):
    """Получить последние 50 сообщений чата"""
    messages = Message.objects.select_related('user').order_by('-timestamp')[:50]
    messages_list = [{
        'user': msg.user.get_full_name() or msg.user.username,
        'user_id': msg.user.id,
        'message': msg.content,
        'timestamp': msg.timestamp.isoformat()
    } for msg in reversed(messages)]
    return JsonResponse({'messages': messages_list})
