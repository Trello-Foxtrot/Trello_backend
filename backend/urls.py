from django.urls import path
from . import views

urlpatterns = [
    path('login', views.sign_in),
    path('sign_up', views.sign_up),
    path('workspace', views.get_workspace),
    path('workspace/add', views.add_workspace),
    path('workspace/delete', views.delete_workspace),
    path('workspace/rename', views.rename_workspace),
    path('workspace/members', views.get_workspace_members),
    path('workspace/boards', views.get_workspace_boards)
]
