from django.test import TestCase,Client
from .models import *
from loguru import logger

# Create your tests here.
def createDjango():
    return Framework.objects.create(
        name="django"
    )

class ProjectDjangoTestCase(TestCase):
    project_name=None
    repo_url = None
    framework = None
    db=None
    client = None


    def setUp(self):
       self.framework=createDjango()
       self.client = Client()

    def test_django_postgres_project_create(self):
        self.project_name = "test_project"
        self.repo_url = "https://github.com/dushyant19/SwcTeams.git"
        self.db="sqlite"
        
        data =  {
            "db":self.db,
            "project_name":self.project_name,
            "repo_url":self.repo_url,
            "project_description":"This is a test project"
        }
        
        response = self.client.post('/project/create/',data=data,content_type="application/json")
        logger.debug(response.data) 
        self.assertEqual(response.status_code, 201)


        
