from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpRequest
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
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.GET = dict(request.GET)
        req.GET['token'] = token
        byte_data = api.get_my_graphs(req).getvalue()
        my_graphs = json.loads(byte_data.decode())
        return render(request, 'graphs/index.html', {'graphs_list': my_graphs['Graphs']})
    else:
        return redirect('/login/', request)


def graph_view(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.GET = dict(request.GET)
        req.GET['token'] = token
        req.GET['graph_id'] = req.GET['graph_id'][0]
        byte_data = api.get_graph_nodes(req).getvalue()
        nodes = json.loads(byte_data.decode())
        return render(request, 'graph/index.html', {'nodes_list': nodes['Nodes'],
                                                    'graph_id': req.GET['graph_id']})
    else:
        return redirect('/login/', request)


def node_view(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.GET = dict(request.GET)
        req.GET['token'] = token
        req.GET['node_id'] = req.GET['node_id'][0]
        byte_data = api.get_node_content(req).getvalue()
        contents = json.loads(byte_data.decode())
        return render(request, 'node/index.html', {'contents_list': contents['Contents'],
                                                   'node_id': req.GET['node_id']})
    else:
        return redirect('/login/', request)


def graph_delete(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['graph_id'] = req.POST['graph_id'][0]
        api.delete_graph(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)


def node_delete(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['node_id'] = req.POST['node_id'][0]
        api.delete_node(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)


def content_delete(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['content_id'] = req.POST['content_id'][0]
        api.delete_content(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)


def graph_append(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['title'] = req.POST['title'][0]
        api.create_graph(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)


def node_append(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['title'] = req.POST['title'][0]
        req.POST['graph_id'] = req.POST['graph_id'][0]
        api.append_node(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)


def content_append(request):
    token = request.session.get('NodesToken')
    if token:
        req = HttpRequest()
        req.POST = dict(request.POST)
        req.POST['token'] = token
        req.POST['node_id'] = req.POST['node_id'][0]
        req.POST['text'] = req.POST['text'][0]
        api.append_content(req)
        return redirect('/graphs/', request)
    else:
        return redirect('/login/', request)
