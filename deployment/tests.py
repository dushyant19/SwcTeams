from django.test import TestCase,Client
from .models import *
from loguru import logger

# Create your tests here.
def createDjango():
    return Framework.objects.create(
        name="django"
    )

def createReact():
    return Framework.objects.create(
        name="react"
    )

def createNode():
    return Framework.objects.create(
        name="nodejs"
    )

class ProjectCreateTestCase(TestCase):
    project_name=None
    repo_url = None
    frameworks ={}
    db=None
    client = None
    current_framework=None


    def setUp(self):
       self.current_framework="nodejs"
       self.project_name = "test_project_"+self.current_framework
       self.repo_url = {
           "django":"https://github.com/dushyant19/Swc_teams_django_boilerplate.git",
           "react":"https://github.com/KunalSolanke/react-boilerplate.git",
           "nodejs":"https://github.com/KunalSolanke/Node_boilerplate.git"
       }
       self.frameworks["django"]=createDjango()
       self.frameworks["react"]=createReact()
       self.frameworks["nodejs"]= createNode()
       self.db="sqlite"
       self.client = Client()

    def test_project_create(self):
        data =  {
            "db":self.db,
            "project_name":self.project_name,
            "repo_url":self.repo_url[self.current_framework],
            "project_description":"This is a test project",
            "platform":self.frameworks[self.current_framework].pk
        }
        
        response = self.client.post('/project/create/',data=data,content_type="application/json")
        logger.debug(response.data) 
        self.assertEqual(response.status_code, 201)
    
    

    
    
    


        
