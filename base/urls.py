from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('auth', views.auth, name='main'),
    path('reg', views.reg, name='main'),
    path('my_graphs', views.my_graphs, name='main'),
    path('base_node', views.base_node, name='main'),
    path('graph_nodes', views.graph_nodes, name='main'),
    path('links_from', views.links_from, name='main'),
    path('links_to', views.links_to, name='main'),
    path('node_content', views.node_content, name='main'),
]
