from django.http import JsonResponse
from .models import *

# TODO: распределить функции по модулям


def index(request):
    data = list(Content.objects.all()[0:1].values())
    return JsonResponse({'data': data})


def my_graphs(request):
    """
    Получить все графы текущего пользователя
    """


def graph_nodes(request, graph_id):
    """
    Получить все узлы принадлежащие графу
    """


def links_from(request, node_id):
    """
    Получить все узлы, в которые можно попасть из этого узла
    """


def links_to(request, node_id):
    """
    Получить все узлы, из которых можно попасть в этот узел
    """


def node_content(request, node_id):
    """
    Получить контент заданного графа
    """


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
