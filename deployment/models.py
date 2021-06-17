from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Framework(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=150)

class Project(models.Model):
    created_by = models.ForeignKey(CustomUser,related_name='projects',on_delete=models.CASCADE)
    members = models.ManyToManyField(CustomUser)
    project_name = models.CharField(max_length=200,unique=True)
    domain = models.URLField(unique=True)
    platform = models.CharField(max_length=255)
    repo_url = models.URLField(unique=True)
    # we will add project as foreign key in database model
    # we will add projectas foreign key in config vars model
    database_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_build_version = models.IntegerField(default=0)
    project_description = models.TextField(unique=True)
    project_image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=150)
    sentry_url = models.URLField(max_length=200)
    platforms = models.OneToOneField(to=Framework, on_delete=models.CASCADE, parent_link=False)




    def __str__(self):
        return self.project_name


class Database(models.Model):
    project = models.ForeignKey(Project,related_name='databases',on_delete=models.CASCADE)
    container_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    db_type = models.CharField(max_length=255)
    port = models.IntegerField(default=8001)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Configs(models.Model):
    key = models.CharField(max_length=100)
    value = models.CharField(max_length=300)
    project = models.ForeignKey(Project,related_name='config_vars',on_delete=models.CASCADE)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return f'[{self.key},{self.value}]'

class Service(models.Model):
    service_defaults = models.ForeignKey(to=Framework, related_name='services', on_delete=models.CASCADE)
    service_name = models.CharField(max_length=100)
    service_settings = models.JSONField(default=dict)
    projects = models.ManyToManyField(Project, related_name='services')



