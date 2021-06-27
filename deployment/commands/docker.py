"""===================================== COMMAND HELPERS ================================="""
def create_volume(name):
    obj = {}
    obj['run'] = f'docker volume create {name}'
    obj['revert'] = f'docker volume rm {name}'
    return obj

def remove(type,name):
    obj = {}
    obj['run'] = f'docker {type} rm -f {name}'
    return obj

def docker_build_context(version,name):
    obj = {}
    obj['run'] = f'docker build -t {name}:{version} .'
    obj['revert'] = f'docker rm -f {name}'
    return obj

def docker_run(options,container):
    obj = {}
    obj['run'] = f'docker run {options}'
    obj['revert'] = f'docker rm -f {container}'
    return obj

def docker_list():
    obj = {}
    obj['run'] = f'docker ps'
    return obj

def network_create(name):
    obj = {}
    obj['run'] = f"docker network create {name}_network"
    return obj

"""========================================================================================="""
def docker_compose(projectDir,services):
    obj={}
    obj["run"]=f"cd {projectDir}&& docker-compose up ${services}"
    obj["revert"]=f"cd {projectDir}&& docker-compose down --volumes"
    return obj


def docker_compose_down(projectDir):
    obj={}
    obj["run"]=f"cd {projectDir}&& docker-compose down --volumes"
    return obj


commands = {
    'create_volume': create_volume,
    'remove': remove,
    'docker_build_context': docker_build_context,
    'docker_run':docker_run,
    'docker_list':docker_list,
    'docker_net':network_create
    "docker_compose_up":docker_compose,
    "docker_compose_down":docker_compose_down
}