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
    main_file=project.configs.filter(key="main_file").first()
    return {
        "projectdir":server_base_path+project.name,
        "main_file":main_file
    }


# def save_configurations(project, env):
#   dockerfilename = env.projectDir + "/Dockerfile"
  
#   setup = [
#     {
#       "command": {
#         "run": f"touch ${env.projectDir}/src/.env",
#       },
#       "name": "make .env file",
#     },
#   ]

  # for config in project.config_vars.all() {
  #   setup.append{
  #     "command": {
  #       "run":"echo " +config.key +
  #         "=" +
  #         config.value +
  #         f">> {env.projectDir}/src/.env",
  #     },
  #     "name": "make values to .env",
  #   })
  # }

  # return setup



# def docker_setup(project,env):
#     dockerfilename = env.projectDir + "/Dockerfile"
#     dockerignorefile = env.projectDir + "/.dockerignore"
#     setup = [
#         {
#         "command": {
#             "run": f"cp ./docker_config/docker_node/Dockerfile ${dockerfilename}",
#         },
#         "name": "copy docker file",
#         },
#         {
#         "command": {
#             "run": f"cp ./docker_config/docker_node/.dockerignore ${dockerignorefile}",
#         },
#         "name": "copy docker file",
#         },
#     ]

#     return setup

# def docker_build(project, env):
#   total = Project.objects.count()
#   port = 3000 + total
#   linked_containers = ""
#   for db in project.databases.all():
#     linked_containers += f"--link ${db.containername}"
  

#   setup = [
#     {
#       "command": {
#         "run": f"cd {env.projectDir} && {
#           docker_commands["dockerBuildContext"](
#             project.version + ".0",
#             project.name.toLowerCase() + "/test"
#           )["run"]
#         }",
#         "revert": docker_commands["remove"]("image", project.name)["run"],
#       },
#       name: "docker build image",
#     },
#     {
#       "command": docker_commands["dockerRun"](
#         f"-i --rm  --env-file {env.projectDir}/src/.env --name ${project.name.toLowerCase()} -p ${port}:3000 {project.name.toLowerCase()}/test:{project.version}.0 node /usr/src/app/src/{env.mainfile}"
#       ),
#       name: "docker run",
#     },
#   ]

#   project.port = port
#   project.save()
#   return setup


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

  
  





def performintialsetup(project):
    env=get_project_conf(project)
    setup=[
        {
            "command":basic_commands["mkdir"](project)(f"-p {env['projectdir']}"),
            "name":"make project dir"
        },
        {
            "command":basic_commands["mkdir"](project)(f"-p {env['projectdir']}/src"),
            "name":"Creating source folder"
        },
        {
            "command":basic_commands["clone"](project.repo_url,env.projectdir+"/src"),
            "name":"Clone repo"
        },
    ]

    fallback_arr=[]
    try : 
      fallback_arr.append({
          "command":{
              "run":f"rm -rf {env.projectdir}"
          }
      })
      
      ##Perform intial setup
      run_multiple(setup,"==============BASIC SETUP============",cb,fallback_arr)
      ##Create docker container
      # run_multiple(docker_setup(project,env),"==============DOCKER SETUP============",cb,fallback_arr)
      add_docker_file(project)
    except Exception as e:
      repr(e)
      run_multiple(fallback_arr,"===================Revert changes====================",cb)

        
def deploy (project):
    env = getprojectEnv(project)
    fallback_arr = []
    try : 
      run_multiple(
          saveconfigurations(project, env),
          "================UPDATE/CREATE ENV==================",
          cb,
          fallback_arr
      )
      run_multiple(
          docker_build(project, env),
          "====================DOCKER BUILD=====================",
          cb,
          fallback_arr
      )
    except Exception as e:
      repr(e)
      run_multiple(fallback_arr,"===================Revert changes====================",cb)