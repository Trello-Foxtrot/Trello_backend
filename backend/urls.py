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
    path('workspace/boards', views.get_workspace_boards),
    path('workspace/boards/add', views.add_workspace_board),
    path('workspace/boards/delete', views.delete_workspace_board),
    path('workspace/boards/rename', views.rename_workspace_board),
    path('workspace/boards/lists', views.get_boards_lists),
    path('workspace/boards/lists/add', views.add_boards_list),
    path('workspace/boards/lists/delete', views.delete_boards_list),
    path('workspace/boards/lists/rename', views.rename_boards_list),
]
