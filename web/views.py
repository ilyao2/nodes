from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from base import views as api
import json


def index(request):
    return HttpResponse('Content')


def login_view(request):
    if request.POST:
        byte_data = api.auth(request).getvalue()
        dict_data = json.loads(byte_data.decode())
        token = dict_data.get('Token')
        if token:
            request.session['NodesToken'] = token
            response = redirect('/graphs/')
        else:
            response = redirect('/login/')
        return response
    else:
        return render(request, 'login/index.html')


def graphs_view(request):
    if request.session.get('NodesToken'):
        return HttpResponse('Показывает все графы текущего пользователя. Пользователь по токену из сессии')
    else:
        return redirect('/login/', request)


def graph_view(request):
    return HttpResponse('Показывает базовый узел выбранного графа и все другие узлы')


def node_view(request):
    return HttpResponse('Показывает выбранный узел')
