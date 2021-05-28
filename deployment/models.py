from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Project(models.Model):
    admin = models.ForeignKey(CustomUser,related_name='projects',on_delete=models.CASCADE)
    memebers = models.ManyToManyField(CustomUser)
    project_name = models.CharField(max_length=200,unique=True)
    domain = models.URLField(unique=True)
    platform = models.CharField(max_length=255)
    repo_url = models.URLField(unique=True)
    # we will add project as foreign key in database model
    # we will add projectas foreign key in config vars model
    database_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

