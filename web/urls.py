from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='main'),
    path('login/', views.login_view, name='main'),
    path('auth/', views.auth, name='main'),
    path('graphs/', views.graphs_view, name='main'),
    path('graph/', views.graph_view, name='main'),
    path('node/', views.node_view, name='main'),
]
