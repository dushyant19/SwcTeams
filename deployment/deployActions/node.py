import subprocess
from deployment.commands.basic_commands import commands as basic_commands
from deployment.commands.docker import commands as docker_commands
from ..utils import run_multiple,cb
import os
from django.conf import settings
from loguru import logger

Base_Dir = settings.BASE_DIR

server_base_path=os.environ.get("SERVER_BASE_PATH")
server_pass=os.environ.get("SERVER_PASS")

@logger.catch
def get_project_conf(project):
    #main_file=project.configs.filter(key="main_file").first()
    env={
        "project_dir":server_base_path+project.project_name,
        #"main_file":main_file
    }
    logger.debug("Created env for project")
    logger.debug(env)
    return env

@logger.catch
def parse_docker_compose(project,docker_compose):
  env = get_project_conf(project)
  global_docker_compose = open(docker_compose,'r')
  old_text = global_docker_compose.read()
  newtext = old_text.replace('<project>',project.project_name)
  project_docker_compose = open(env['project_dir']+'/docker-compose.yaml','w')
  project_docker_compose.write(newtext)
  global_docker_compose.close()
  project_docker_compose.close()

@logger.catch
def copy_docker_file(project,docker_file):
  env = get_project_conf(project)
  global_docker_file = open(docker_file,'r')
  text = global_docker_file.read()
  project_docker_file = open(env['project_dir']+'/Dockerfile','w')
  project_docker_file.write(text)
  global_docker_file.close()
  project_docker_file.close()



@logger.catch
def add_docker_file(project):
  env=get_project_conf(project)
  docker_compose = None
  dockerfile=None
  if project.platform.name=="django":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.django')
    if project.db=="sqlite":
      docker_compose = os.path.join(Base_Dir,"files","compose",'docker_compose.django_sqlite.yaml')
    elif project.db=="postgres":
      docker_compose = os.path.join(Base_Dir,"files","compose",'docker_compose.django_postgres.yaml')
  elif project.platform.name=="nodejs":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.node')
    docker_compose = os.path.join(Base_Dir,"files","compose",'docker-compose.node.yml')
  elif project.platform.name=="react":
    dockerfile = os.path.join(Base_Dir,"files","docker_files",'Dockerfile.react')
    docker_compose = os.path.join(Base_Dir,"files","compose",'docker-compose.react.yml')

  parse_docker_compose(project,docker_compose)
  copy_docker_file(project,dockerfile)

@logger.catch
def containers_setup(project):
  env=get_project_conf(project)
  # configured_services = " ".join(project.configured_services)

  return [{
    "command":docker_commands["docker_compose_up"](env['project_dir'],""),
    "name":"Spinning up the docker containers"
  }]

@logger.catch
def add_container_entrypoints(project):
  env=get_project_conf(project)
  return [{
    "command":{
      "run":f"cp files/entrypoints/* {env['project_dir']}",
    },
    "name":"Copyinng all the entrypoints inside the project dir"
  }]


@logger.catch
def copy_project_env(project):
  env=get_project_conf(project)
  return [{
    "command":{
      "run":f"cp {env['project_dir']}/src/.env {env['project_dir']}/.env",
    },
    "name":"Copyinng repo env variables"
  }]


@logger.catch
async def performinitialsetup(project):
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
            "command":basic_commands["touch"](f"-p {env['project_dir']}/.env"),
            "name":"Creating source folder"
        },
        {
            "command":basic_commands["clone"](project.repo_url,env['project_dir']+"/src"),
            "name":"Clone repo"
        },
    ]

    fallback_arr=[]
    try : 
      # fallback_arr.append({
      #     "command":{
      #         "run":f"rm -rf {env['project_dir']}",
      #     },
      #     "name":"reverting all the chnages"
      # })
      #==================== ADD ALL THE NECCESSARY DOCKER FILES TO PROJECT DIR ===========================#
      run_multiple(setup,"===================BASIC FILE SETUP ====================",cb)
      try:
        run_multiple(copy_project_env(project),"================== COPY ENV  =====================",cb)
      except: 
        pass
      add_docker_file(project)
      run_multiple(add_container_entrypoints(project),"================== CONTAINERS SETUP =====================",cb)
      run_multiple(containers_setup(project),"================== CONTAINERS SETUP(Docker compose up) =====================",cb)
      
    except Exception as e:
      logger.debug(repr(e))
      fallback_arr.reverse()
      run_multiple(fallback_arr,"===================Revert changes====================",cb)


#this need to be changes if we ask branch from user
def redeploy(project):
  env = get_project_conf(project)
  setup = [
    {
      "command":{
        "run":f"cd {env['project_dir']+'/src'} && git pull",
        "name":"creating base repo"
      }
    }
  ] + [{
    "command":docker_commands["docker_compose_down"](env['project_dir']),
    "name":"Spinning down the docker containers"
  }]
  setup+=containers_setup(project) # mergining the list with docker compose up 
  
  fallback_arr = []
  try :
    run_multiple(setup,"===================Redeploy ====================",cb)
      
  except Exception as e:
    repr(e)
    fallback_arr.reverse()
    run_multiple(fallback_arr,"===================Revert changes====================",cb)
      
    