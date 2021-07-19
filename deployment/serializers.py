from rest_framework import serializers
from .models import *

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields='__all__'


class FrameWorkSerializer(serializers.ModelSerializer):
    additional_services = ServiceSerializer(many=True, required=False)
    default_services = ServiceSerializer(many=True, required=False)
    class Meta:
        model=Framework
        fields='__all__'
    


class ProjectSerializer(serializers.ModelSerializer):
    platform = FrameWorkSerializer(required=False)
    class Meta:
        model=Project
        fields='__all__'

#making serializer according to our requirement
class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields='__all__'

