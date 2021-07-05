import subprocess
from deployment.commands.basic_commands import commands as basic_commands
from deployment.commands.docker import commands as docker_commands
from ..utils import run_multiple,cb
import os
from django.conf import settings

Base_Dir = settings.BASE_DIR

server_base_path=os.eviron.get("SERVER_BASE_PATH")
server_pass=os.environ.get("SERVER_PASS")


def get_project_conf(project):
    #main_file=project.configs.filter(key="main_file").first()
    return {
        "project_dir":server_base_path+project.name,
        #"main_file":main_file
    }


def parse_docker_compose(project,docker_compose):
  env = get_project_conf(project)
  global_docker_compose = open(docker_compose,'r')
  old_text = global_docker_compose.read()
  newtext = old_text.replace('<project>',project.name)
  project_docker_compose = open(env['project_dir']+'/docker-compose.yaml','w')
  project_docker_compose.write(newtext)
  global_docker_compose.close()
  project_docker_compose.close()

def copy_docker_file(project,docker_file):
  env = get_project_conf(project)
  global_docker_file = open(docker_file,'r')
  text = global_docker_file.read()
  project_docker_file = open(env['project_dir']+'/Dockerfile','w')
  project_docker_file.write(text)
  global_docker_file.close()
  project_docker_file.close()

def add_docker_file(project):
  env=get_project_conf(project)
  docker_compose = None
  dockerfile=None
  if project.platform=="Django":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.django')
    if project.db=="sqlite":
      docker_compose = os.path.join(Base_Dir,"files","compose",'docker_compose.django_sqlite.yaml')
    elif project.db=="postgres":
      docker_compose = os.path.join(Base_Dir,"files","compose",'docker_compose.django_postgres.yaml')
  elif project.platform=="Node":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.node')
    docker_compose = os.path.join(Base_Dir,"files","compose",'docker-compose.node.yml')
  elif project.platform=="React":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.react')
    docker_compose = os.path.join(Base_Dir,"files","compose",'docker-compose.react.yml')

  parse_docker_compose(project,docker_compose)
  copy_docker_file(project,dockerfile)

  
def containers_setup(project):
  env=get_project_conf(project)
  configured_services = " ".join(project.configured_service)

  return [{
    "command":docker_commands["docker_compose"](env['project_dir'],configured_services),
    "name":"Spinning up the docker containers"
  }]


def add_container_entrypoints(project):
  env=get_project_conf(project)
  return [{
    "command":{
      "run":f"cp files/entrypoints/* ${env['project_dir']}"
    },
    "name":"Copyinng all the entrypoints inside the project dir"
  }]



def performintialsetup(project):
    env=get_project_conf(project)
    setup=[
        {
            "command":basic_commands["mkdir"](f"-p {env['project_dir']}"),
            "name":"make project dir"
        },
        {
            "command":basic_commands["mkdir"](f"-p {env['project_dir']}/src"),
            "name":"Creating source folder"
        },
        {
            "command":basic_commands["clone"](project.repo_url,env['project_dir']+"/src"),
            "name":"Clone repo"
        },
    ]

    fallback_arr=[]
    try : 
      fallback_arr.append({
          "command":{
              "run":f"rm -rf {env['project_dir']}"
          }
      })
      #==================== ADD ALL THE NECCESSARY DOCKER FILES TO PROJECT DIR ===========================#
      run_multiple(setup,"===================BASIC FILE SETUP ====================",cb)
      add_docker_file(project)
      run_multiple(add_container_entrypoints(project),"================== CONTAINERS SETUP =====================",cb)
      run_multiple(containers_setup(project),"================== CONTAINERS SETUP(Docker compose up) =====================",cb)
      
    except Exception as e:
      repr(e)
      fallback_arr.reverse()
      run_multiple(fallback_arr,"===================Revert changes====================",cb)


#this need to be changes if we ask branch from user
def redeploy(project):
  env = get_project_conf(project)
  setup = [
    {
      "command":{
        "run":f"cd {env['project_dir']+'/src'} && git pull",
      }
    }
  ] + [{
    "command":docker_commands["docker_compose_down"](env['project_dir']),
    "name":"Spinning down the docker containers"
  }]
  setup+=containers_setup(project) # mergining the list with docker compose up 
  
  fallback_arr = []
  try :
    run_multiple(setup,"===================BASIC FILE SETUP ====================",cb)
      
  except Exception as e:
    repr(e)
    fallback_arr.reverse()
    run_multiple(fallback_arr,"===================Revert changes====================",cb)
      
    