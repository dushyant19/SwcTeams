from django.db.models import query
from django.shortcuts import render
from loguru import logger

logger.debug("That's it, beautiful and simple logging!")
from rest_framework import generics
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator



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


@method_decorator([logger.catch], name='dispatch')
class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer

