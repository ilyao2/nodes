from django.shortcuts import render
from django.http import HttpResponse
from base import views as api
import json


def index(request):
    return HttpResponse('Content')


def login_view(request):
    return render(request, 'login/index.html')


def auth(request):
    """Вызывает api-method для получения токена и сохраняет токен в сессию"""
    byte_data = api.auth(request).getvalue()
    dict_data = json.loads(byte_data.decode())
    token = dict_data.get('Token')
    if token:
        response = HttpResponse('redirect good')
    else:
        response = HttpResponse('redirect bad')
    return response


def graphs_view(request):
    return HttpResponse('Показывает все графы текущего пользователя. Пользователь по токену из сессии')


def graph_view(request):
    return HttpResponse('Показывает базовый узел выбранного графа и все другие узлы')


def node_view(request):
    return HttpResponse('Показывает выбранный узел')
