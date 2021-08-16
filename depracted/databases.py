from .docker import *
from deployment.models import Database,Configs
from deployment.utils import run_command,run_multiple,cb
from .docker import *


def mongodb_setup(project):
    project_name = project.name.lower()
    conatiner_name = "mongo_" + project_name
    volume_name = "mongodb_" + project_name
    volume_config = "mongodb_config_" + project_name

    total_mongo_db = Database.objects.count()
    port = 27017 + total_mongo_db
    fallback = []
    try:
        function = commands['create_volume'](volume_name)
        run_command(function,"create mongodb volume",cb,fallback)
        function = commands['create_volume'](volume_config)
        run_command(function,"create mongo config volume",cb,fallback)
        function = commands["docker_run"](f'-dit --rm --name {conatiner_name} --net {project_name}_network -p {port}:27017 mongo',conatiner_name)
        run_command(function,f"running mongo container {project_name}",cb,fallback)
    except Exception as e:
        repr(f"Revreting changes {e}")
        run_multiple(fallback,"mongodb creation block",cb,fallback)
        raise Exception(e.message)
    
    database = Database.objects.create(
        project=project,
        conatiner_name=conatiner_name,
        name="mongo",
        port=port,
        db_type="NoSql"
    )
    configs = Configs.objects.create(
        key="MONGO_URI",
        value=f"mongodb://{containername}:27017/{project.name}",
        project=project,
        is_private=True
    )
    
# We are here

def postgres_setup(project):
    project_name = project.name.lower()
    conatiner_name = "postgres_" + project_name
    volume_name = "postgres_" + project_name

    total_mongo_db = Database.objects.count()
    port = 5432 + total_mongo_db
    fallback = []
    try:
        function = commands['create_volume'](volume_name)
        run_command(function,"create postgres volume",cb,fallback)
        function = commands["docker_run"](f'-dit --rm --name {conatiner_name} --net {project_name}_network -p {port}:27017 mongo',conatiner_name)
        run_command(function,f"running mongo container {project_name}",cb,fallback)
    except Exception as e:
        repr(f"Revreting changes {e}")
        run_multiple(fallback,"mongodb creation block",cb,fallback)
        raise Exception(e.message)
    
    database = Database.objects.create(
        project=project,
        conatiner_name=conatiner_name,
        name="postgres",
        port=port,
        db_type="Sql"
    )
    
    configs=[
      { "key": "DATABASE_URI", "value": f"{container_name}:${port}" },
      { "key": "POSTGRES_USER", "value": "{project.user.username}" },
      { "key": "POSTGRES_HOST", "value": f"${contianername}" },
      { "key": "POSTGRES_PASSWORD", "value": f"{contianername}" },
      { "key": "POSTGRES_DB", "value": "{project.name}"},
      { "key": "POSTGRES_PORT", "value": "{project.port}"},
    ]
    for config in configs:
        configs = Configs.objects.create(
            key=config.key,
            value=config.value,
            project=project,
            is_private=True
        )