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
    env={
        "project_dir":server_base_path+project.project_name,
    }
    return env


@logger.catch
def parse_and_create(project,docker_file,file_dest):
  env = get_project_conf(project)
  global_docker_file = open(docker_file,'r')
  text = global_docker_file.read()
  text = text.replace('<project>',project.project_name)
  project_docker_file =open(file_dest,'w')
  project_docker_file.write(text)
  global_docker_file.close()
  project_docker_file.close()


@logger.catch
def add_docker_file(project):
  env=get_project_conf(project)
  dockerfile = os.path.join(Base_Dir,"deployment","files","docker_files",f"Dockerfile.{project.platform.name}")
  docker_compose = os.path.join(Base_Dir,"deployment","files","compose",f"docker-compose.{project.platform.name}.yml")

  # Replace <project> and create file in destination folders
  parse_and_create(project,dockerfile,env['project_dir']+'/Dockerfile')
  parse_and_create(project,docker_compose,env['project_dir']+'/docker-compose.yaml')


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
      "run":f"cp {Base_Dir}/deployment/files/entrypoints/* {env['project_dir']}",
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
            "command":basic_commands["mkdir"](f"{env['project_dir']}"),
            "name":"make project dir"
        },
        {
            "command":basic_commands["mkdir"](f"{env['project_dir']}/src"),
            "name":"Creating source folder"
        },
        {
            "command":basic_commands["touch"](f"{env['project_dir']}/.env"),
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
              "run":f"rm -rf {env['project_dir']}",
          },
          "name":"reverting all the chnages"
      })
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
      
    