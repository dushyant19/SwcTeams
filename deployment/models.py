from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import pre_save,post_save
from deployment.deployActions.node import performinitialsetup,redeploy
from django.dispatch import receiver
from loguru import logger
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync,sync_to_async


# Create your models here.
class Framework(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="frameworks/",blank=True, null=True)

class Project(models.Model):
    #created_by = models.ForeignKey(CustomUser,related_name='projects',on_delete=models.CASCADE)
    #members = models.ManyToManyField(CustomUser)
    class ProjectStateChoices(models.TextChoices):
        IDLE="I"
        BUILDING ="B"
        RUNNING = "R"

    project_state = models.CharField(max_length=255,default=ProjectStateChoices.IDLE,choices=ProjectStateChoices.choices)
    project_name = models.CharField(max_length=200,unique=True)
    repo_url = models.URLField(unique=True)
    database_configured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_build_version = models.IntegerField(default=0)
    project_description = models.TextField()
    project_image = models.ImageField(upload_to="projects/", max_length=150,blank=True, null=True)
    #db=models.CharField(blank=True, null=True,max_length=255) #depracted
    sentry_url = models.URLField(max_length=200,blank=True, null=True)
    platform = models.OneToOneField(Framework, on_delete=models.CASCADE,null=True,blank=True) # what is parent_link?
    
    def __str__(self):
        return self.project_name

from .tasks import create_project

@logger.catch
def projectToChannel(project):
    logger.debug("Sending log Consumer ")
    create_project.delay(project.id)
    message ="Build Started"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "build_"+project.project_name,
        {'type': 'build_logs', 'message': message}
    )
    


@receiver(post_save, sender =Project)
def my_callback(sender, instance,created, *args, **kwargs):
    logger.debug(f"Created new project {instance}")
    logger.debug(f"isCreated : {created}")
    if created:
        try:
            projectToChannel(instance)
        except Exception as e:
            print("Exception occured ",repr(e))
            repr(e)
    else:
        redeploy(instance)




