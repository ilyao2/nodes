from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('auth', views.auth, name='auth'),
    path('reg', views.reg, name='reg'),
    path('my_graphs', views.get_my_graphs, name='my_graphs'),
    path('base_node', views.get_base_node, name='base_node'),
    path('graph_nodes', views.get_graph_nodes, name='graph_nodes'),
    path('links_from', views.get_links_from, name='links_from'),
    path('links_to', views.get_links_to, name='links_to'),
    path('node_content', views.get_node_content, name='node_content'),
    path('append_node', views.append_node, name='append_node'),
]
