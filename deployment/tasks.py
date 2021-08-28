from celery import shared_task
from .models import Project
from .deployActions.node import performinitialsetup

@shared_task
def create_project(project_id):
    project = Project.objects.get(pk=project_id)
    performinitialsetup(project)
