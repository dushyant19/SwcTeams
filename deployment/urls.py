from django.urls import path,include,re_path
from .views import *

app_name = 'deployment'

urlpatterns = [
    path('list/', ProjectListView.as_view(),name = 'project_list'),
    path('detail/<int:pk>/', ProjectDetailView.as_view(),name = 'project_detail'),
    path('delete/<int:pk>/', ProjectDeleteView.as_view(),name = 'project_delete'),
    path('create/', ProjectCreateView.as_view(),name = 'project_create'),
    path('update/<int:pk>/', ProjectUpdateView.as_view(),name = 'project_update'),
]
