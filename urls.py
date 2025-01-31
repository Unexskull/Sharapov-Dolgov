from django.urls import path
from . import views

urlpatterns = [
    #sidebar
    path('', views.base_view, name ='base'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('servers/', views.servers_view, name='servers'),
    path('account/', views.account_view, name='account'),
    #servers
    path('add_server/', views.add_server_view, name='add_server'),
    path('list_servers/', views.list_servers_view, name='list_servers'),
    path('edit_server/<int:id>/', views.edit_server, name='edit_server'),
    path('delete_server/<int:id>/', views.delete_server, name='delete_server'),
    path('ssh_parameters/', views.ssh_parameters_view, name='ssh_parameters'),
    path('server_resource_graph/', views.server_resource_graph, name='server_resource_graph'),
    path('get_server_data/', views.get_server_data, name='get_server_data'),
    path('volumes/', views.server_resource_graph, name='volumes'),
]
