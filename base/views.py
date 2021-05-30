from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .models import *
from uuid import uuid4

# TODO: распределить функции по модулям


def auth(request):
    """
    Авторизовать по логину и паролю и вернуть токен
    login: Логин пользователя
    password: Пароль пользователя
    """
    login = request.GET.get('login')
    password = request.GET.get('password')
    user = authenticate(username=login, password=password)
    data = Token.objects.get(User=user).UUID if user else ''
    return JsonResponse({'Token': data})


def reg(request):
    """
    Метод регестрирует пользователя и генерирует токен
    login: Логин пользователя
    password: Пароль пользователя
    email: Электронная почта нового пользователя
    """
    login = request.GET.get('login')
    password = request.GET.get('password')
    email = request.GET.get('email')
    if not(login and password):
        response = JsonResponse({'Error': 'Input login and password'})
    elif DUser.objects.filter(username__exact=login).exists():
        response = JsonResponse({'Error': 'User with this login already exists'})
    else:
        user = DUser.objects.create_user(login, email, password)
        user.save()
        uuid = uuid4()
        while Token.objects.filter(UUID__exact=uuid).exists():
            uuid = uuid4()
        token = Token(UUID=uuid, User=user)
        token.save()
        response = JsonResponse({'Token': uuid})
    return response


def index(request):
    data = list(Content.objects.all()[0:1].values())
    return JsonResponse({'Graphs': data})


def my_graphs(request):
    """
    Получить все графы текущего пользователя
    token: Уникальный токен пользователя
    """
    token = request.GET.get('token')
    try:
        user = Token.objects.get(UUID=token).User
        data = list(Graph.objects.filter(User=user).values())
        response = JsonResponse({'Graphs': data})
    except (ObjectDoesNotExist, MultipleObjectsReturned):
        response = JsonResponse({'Error': 'Bad token'})
    return response


def base_node(request):
    """
    Получить базовый узел заданного графа
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    """
    token = request.GET.get('token')
    graph_id = request.GET.get('graph_id')
    if not(token and graph_id):
        response = JsonResponse({'Error': 'Input token and graph_id'})
    else:
        try:
            user = Token.objects.get(UUID=token).User
            if Graph.objects.filter(ReadableUser=user, id=graph_id).exists():
                graph = Graph.objects.get(id=graph_id)
                data = list(Node.objects.filter(Graph=graph, IsBase=True)[0:1].values())
                response = JsonResponse({'Nodes': data})
            else:
                response = JsonResponse({'Error': "You don't have access to this graph or bad graph id"})
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            response = JsonResponse({'Error': 'Bad token'})
    return response


def graph_nodes(request):
    """
    Получить все узлы принадлежащие графу
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    """
    token = request.GET.get('token')
    graph_id = request.GET.get('graph_id')
    if not(token and graph_id):
        response = JsonResponse({'Error': 'Input token and graph_id'})
    else:
        try:
            user = Token.objects.get(UUID=token).User
            if Graph.objects.filter(ReadableUser=user, id=graph_id).exists():
                graph = Graph.objects.get(id=graph_id)
                data = list(Node.objects.filter(Graph=graph).values())
                response = JsonResponse({'Nodes': data})
            else:
                response = JsonResponse({'Error': "You don't have access to this graph or bad graph id"})
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            response = JsonResponse({'Error': 'Bad token'})
    return response


def links_from(request):
    """
    Получить все узлы, в которые можно попасть из этого узла
    token: Уникальный токен пользователя
    node_id: Идентификатор графа
    """
    token = request.GET.get('token')
    node_id = request.GET.get('node_id')
    if not(token and node_id):
        response = JsonResponse({'Error': 'Input token and node_id'})
    else:
        try:
            user = Token.objects.get(UUID=token).User
            try:
                node = Node.objects.get(id=node_id)
                if Graph.objects.filter(ReadableUser=user, id=node.Graph.id).exists():
                    links = Link.objects.filter(StartNode=node).values('EndNode')
                    data = list(Node.objects.filter(id__in=links).values())
                    response = JsonResponse({'Nodes': data})
                else:
                    response = JsonResponse({'Error': "You don't have access to this node"})
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad node id'})
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            response = JsonResponse({'Error': 'Bad token'})
    return response


def links_to(request):
    """
    Получить все узлы, из которых можно попасть в этот узел
    token: Уникальный токен пользователя
    node_id: Идентификатор графа
    """
    token = request.GET.get('token')
    node_id = request.GET.get('node_id')
    if not(token and node_id):
        response = JsonResponse({'Error': 'Input token and node_id'})
    else:
        try:
            user = Token.objects.get(UUID=token).User
            try:
                node = Node.objects.get(id=node_id)
                if Graph.objects.filter(ReadableUser=user, id=node.Graph.id).exists():
                    links = Link.objects.filter(EndNode=node).values('StartNode')
                    data = list(Node.objects.filter(id__in=links).values())
                    response = JsonResponse({'Nodes': data})
                else:
                    response = JsonResponse({'Error': "You don't have access to this node"})
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad node id'})
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            response = JsonResponse({'Error': 'Bad token'})
    return response


def node_content(request):
    """
    Получить контент заданного узла
    """
    token = request.GET.get('token')
    node_id = request.GET.get('node_id')
    if not(token and node_id):
        response = JsonResponse({'Error': 'Input token and node_id'})
    else:
        try:
            user = Token.objects.get(UUID=token).User
            try:
                node = Node.objects.get(id=node_id)
                if Graph.objects.filter(ReadableUser=user, id=node.Graph.id).exists():
                    data = list(Content.objects.filter(Node=node).values())
                    response = JsonResponse({'Contents': data})
                else:
                    response = JsonResponse({'Error': "You don't have access to this node"})
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad node id'})
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            response = JsonResponse({'Error': 'Bad token'})
    return response


def append_node(request, graph_id, content=None):
    """
    Добавить узел в граф
    Исходя из контента делает обход по графу и создаёт веса и связи
    Если не найдено с чем связать, связывает с базовым узлом
    """
    # TODO: Самый важный метод


def ordered_nodes(request, graph_id):
    """
    Получить все узлы графа в топографически отсортированном виде относительно базового узла
    """


def create_graph(request):
    """
    Создать граф и базовый узел в нём. Не должно существовать графов без узла
    """
