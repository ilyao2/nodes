from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('login/', views.login_view, name='main'),
    path('graphs/', views.graphs_view, name='main'),
    path('graph/', views.graph_view, name='main'),
    path('node/', views.node_view, name='main'),
    path('graph_delete/', views.graph_delete, name='main'),
    path('node_delete/', views.node_delete, name='main'),
    path('content_delete/', views.content_delete, name='main'),
    path('graph_append/', views.graph_append, name='main'),
    path('node_append/', views.node_append, name='main'),
    path('content_append/', views.content_append, name='main'),
]
