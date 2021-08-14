from django.db.models import query
from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *


# Create your views here.
class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
class ProjectDetailView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

