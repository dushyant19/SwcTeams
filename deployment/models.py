from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import pre_save,post_save
from deployment.deployActions.node import performinitialsetup,redeploy
from django.dispatch import receiver


# Create your models here.
class Framework(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=150)
    additional_services = models.ManyToManyField('Service', related_name='frameworks_for_additional')
    default_services = models.ManyToManyField('Service', related_name='frameworks_for_default')


class Project(models.Model):
    #created_by = models.ForeignKey(CustomUser,related_name='projects',on_delete=models.CASCADE)
    #members = models.ManyToManyField(CustomUser)
    project_name = models.CharField(max_length=200,unique=True)
    repo_url = models.URLField(unique=True)
    database_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_build_version = models.IntegerField(default=0)
    project_description = models.TextField()
    project_image = models.ImageField(upload_to="projects/", max_length=150)
    sentry_url = models.URLField(max_length=200,unique=True)
    platform = models.OneToOneField(Framework, on_delete=models.CASCADE,null=True,blank=True) # what is parent_link?

    def __str__(self):
        return self.project_name


class Service(models.Model):
    service_name = models.CharField(max_length=100) # shouldn't it be a choice field
    service_settings = models.JSONField(default=dict) # where is th dict
    projects = models.ManyToManyField(Project, related_name='services')


@receiver(post_save, sender =Project)
def my_callback(sender, instance,created, *args, **kwargs):
    if created:
        try:
            performinitialsetup(instance)
        except Exception as e:
            repr(e)
    else:
        redeploy(instance)




