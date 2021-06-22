from django.db import models
from deployment.models import Project
from accounts.models import CustomUser
# Create your models here.

class Build(models.Model):
    project = models.ForeignKey(Project,related_name="builds",on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser,related_name='builds',on_delete=models.CASCADE,null=True)
    logs = models.TextField()

    def __str__(self):
        return f'Project-{self.project.pk} Build-{self.pk}'