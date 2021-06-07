from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max
from .models import *
from uuid import uuid4

# TODO: распределить функции по модулям


def check_token(func):
    """
    Декоратор проверяющий наличие токена и его правльность.
    """
    def inner(*args, **kwargs):
        request = args[0]
        token = request.GET.get('token') or request.POST.get('token')
        if not token:
            response = JsonResponse({'Error': 'Input token'})
        else:
            try:
                user = Token.objects.get(UUID=token).User
                response = func(*args, user=user, **kwargs)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad token'})
        return response
    return inner


def check_graph(func, user_param=None):
    """
    Декоратор проверяющий наличие и доступ к переданному графу
    """
    def inner(*args, user=user_param, **kwargs):
        request = args[0]
        graph_id = request.GET.get('graph_id') or request.POST.get('graph_id')
        if not graph_id:
            response = JsonResponse({'Error': 'Input graph_id'})
        else:
            try:
                graph = Graph.objects.get(ReadableUser=user, id=graph_id)
                response = func(*args, user=user, graph=graph, **kwargs)
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': "You don't have access to this graph or bad graph id"})
        return response
    return inner


def check_node(func, user_param=None):
    """
    Декоратор проверяющий наличие и доступ к переданному узлу
    """
    def inner(*args, user=user_param, **kwargs):
        request = args[0]
        node_id = request.GET.get('node_id') or request.POST.get('node_id')
        if not node_id:
            response = JsonResponse({'Error': 'Input node_id'})
        else:
            try:
                node = Node.objects.get(id=node_id)
                if Graph.objects.filter(ReadableUser=user, id=node.Graph.id).exists():
                    response = func(*args, user=user, node=node, **kwargs)
                else:
                    response = JsonResponse({'Error': "You don't have access to this node"})
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad node id'})
        return response
    return inner


def check_content(func, user_param=None):
    """
    Декоратор проверяющий наличие и доступ к переданному узлу
    """
    def inner(*args, user=user_param, **kwargs):
        request = args[0]
        content_id = request.GET.get('content_id') or request.POST.get('content_id')
        if not content_id:
            response = JsonResponse({'Error': 'Input content_id'})
        else:
            try:
                content = Content.objects.get(id=content_id)
                node = Node.objects.get(id=content.Node)
                if Graph.objects.filter(ReadableUser=user, id=node.Graph.id).exists():
                    response = func(*args, user=user, content=content, node=node, **kwargs)
                else:
                    response = JsonResponse({'Error': "You don't have access to this content"})
            except (ObjectDoesNotExist, MultipleObjectsReturned):
                response = JsonResponse({'Error': 'Bad content id'})
        return response
    return inner


def auth(request):
    """
    Авторизовать по логину и паролю и вернуть токен
    login: Логин пользователя
    password: Пароль пользователя
    """
    login = request.POST.get('login')
    password = request.POST.get('password')
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
    login = request.POST.get('login')
    password = request.POST.get('password')
    email = request.POST.get('email')
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


@check_token
def get_my_graphs(request, user=None):
    """
    Получить все графы текущего пользователя
    token: Уникальный токен пользователя
    """
    data = list(Graph.objects.filter(User=user).values())
    response = JsonResponse({'Graphs': data})
    return response


@check_token
@check_graph
def get_base_node(request, user=None, graph=None):
    """
    Получить базовый узел заданного графа
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    """
    data = list(Node.objects.filter(Graph=graph, IsBase=True)[0:1].values())
    response = JsonResponse({'Nodes': data})
    return response


@check_token
@check_graph
def get_graph_nodes(request, user=None, graph=None):
    """
    Получить все узлы принадлежащие графу
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    """
    data = list(Node.objects.filter(Graph=graph).values())
    response = JsonResponse({'Nodes': data})
    return response


@check_token
@check_node
def get_links_from(request, user=None, node=None):
    """
    Получить все узлы, в которые можно попасть из этого узла
    token: Уникальный токен пользователя
    node_id: Идентификатор графа
    """
    links = Link.objects.filter(StartNode=node).values('EndNode')
    data = list(Node.objects.filter(id__in=links).values())
    response = JsonResponse({'Nodes': data})
    return response


@check_token
@check_node
def get_links_to(request, user=None, node=None):
    """
    Получить все узлы, из которых можно попасть в этот узел
    token: Уникальный токен пользователя
    node_id: Идентификатор графа
    """
    links = Link.objects.filter(EndNode=node).values('StartNode')
    data = list(Node.objects.filter(id__in=links).values())
    response = JsonResponse({'Nodes': data})
    return response


@check_token
@check_node
def get_node_content(request, user=None, node=None):
    """
    Получить контенты заданного узла отсортированные по указанному порядку
    token: Уникальный токен пользователя
    node_id: Идентификатор графа
    """
    data = list(Content.objects.filter(Node=node).order_by('Ord').values())
    response = JsonResponse({'Contents': data})
    return response


@check_token
@check_graph
def append_node(request, user=None, graph=None):
    """
    Добавить узел в граф
    Исходя из контента делает обход по графу, создаёт связи и распределяет веса
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    title: Заголовок узла

    content:
        text:
        data:
    """
    if request.POST:
        title = request.POST.get('title')
        text = request.POST.get('text')
        data = request.POST.get('data')
        if Node.objects.filter(Graph=graph, Title__iexact=title).exists():
            return HttpResponse(status=201)
        node = Node(Title=title, Graph=graph, IsBase=False)
        node.save()
        if text or data:
            content = Content(Text=text, Data=data, Node=node, Ord=1)
            content.save()
        create_links(node)
        return HttpResponse(status=200)
    return HttpResponse(status=201)


def create_links(node):
    """
    Метод создаёт связи и распределяет веса между узлом и другими узлами
    Если не найдено с чем связать, связывает с базовым узлом
    """
    other_nodes = Node.objects.filter(Graph=node.Graph, IsBase=False).exclude(id=node.id)
    other_contents = Content.objects.filter(Node__in=other_nodes)
    node_contents = Content.objects.filter(Node=node)
    links_dict = {}
    for other_content in other_contents:
        text = other_content.Text
        weight = text.count(node.Title) if text else 0
        if weight > 0:
            other_node = other_content.Node
            if (other_node, node) in links_dict:
                links_dict[(other_node, node)] += weight
            else:
                links_dict[(other_node, node)] = weight
    if not links_dict:
        base_node = Node.objects.get(Graph=node.Graph, IsBase=True)
        links_dict[(base_node, node)] = 1
    for other_node in other_nodes:
        for content in node_contents:
            text = content.Text
            weight = text.count(other_node.Title) if text else 0
            if weight > 0:
                if (node, other_node) in links_dict:
                    links_dict[(node, other_node)] += weight
                else:
                    links_dict[(node, other_node)] = weight

    links = [Link(StartNode=link[0], EndNode=link[1], Weight=links_dict[link]) for link in links_dict]
    Link.objects.bulk_create(links)


def get_ordered_nodes(request, graph_id):
    """
    Получить все узлы графа в топографически отсортированном виде относительно базового узла
    """
    # TODO: топографическая сортировка
    # TODO: сортировка по рейтингу


@check_token
def create_graph(request, user=None):
    """
    Создать граф и базовый узел в нём. Не должно существовать графов без узла
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    title: название графа
    """
    if request.POST:
        title = request.POST.get('title')
        graph = Graph(Title=title, User=user, ReadableUser=[user])
        graph.save()
        node = Node(Graph=graph, Title=f'{graph.Title}_{graph.id}_base_node', IsBase=True)
        node.save()
        return HttpResponse(status=200)
    return HttpResponse(status=201)


@check_token
@check_node
def append_content(request, user=None, node=None):
    """
    Добавить контент к узлу графа
    token: Уникальный токен пользователя
    node_id: Идентификатор узла
    content:
        text:
        data:
    """
    if request.POST:
        text = request.POST.get('text')
        data = request.POST.get('data')
        if text or data:
            content_ord = Content.objects.filter(Node=node).aggregate(max_ord=Max('Ord'))['max_ord'] + 1
            content = Content(Text=text, Data=data, Node=node, Ord=content_ord)
            content.save()
            links = Link.objects.filter(StartNode=node) | Link.objects.filter(EndNode=node)
            links.delete()
            create_links(node)
        return HttpResponse(status=200)
    return HttpResponse(status=201)


@check_token
@check_graph
def delete_graph(request, user=None, graph=None):
    """
    Удалить заданный граф (все его узлы и связи)
    token: Уникальный токен пользователя
    graph_id: Идентификатор графа
    """
    graph.delete()


@check_token
@check_node
def delete_node(request, user=None, node=None):
    """
    Удалить заданный узел (и все связи с ним)
    token: Уникальный токен пользователя
    node_id: Идентификатор узла
    """
    node.delete()


@check_token
@check_content
def delete_content(request, user=None, node=None, content=None):
    """
    Удалить заданный контент
    token: Уникальный токен пользователя
    content_id: Идентификатор узла
    """
    content.delete()
    links = Link.objects.filter(StartNode=node) | Link.objects.filter(EndNode=node)
    links.delete()
    create_links(node)

