from typing import (
    Dict
)
import os
from django.conf import settings

base_dir = settings.BASE_DIR

config_files ={
    "node" :os.path.join(base_dir,'nginx_files/node.conf'),
    "django":os.path.join(base_dir,'nginx_files/django.conf'),
}

password=os.environ.get("SERVER_PASSWORD")



"""=====================================NGINX COMMAND HELPER========================================="""
def copy_nginx_conf(app_type,deployment,domain)->Dict:
    obj["run"] =  f"cp ${config_files[appType]} /etc/nginx/sites-available/${deployname}.${domain}.conf"
    obj["revert"]= f"cp ${config_files[appType]} /etc/nginx/sites-available/${deployname}.${domain}.conf"
    return revert

def enable_file(filename):
    obj["run"]=f"echo ${pass} | sudo ln -s /etc/nginx/sites-available/${filename} /etc/nginx/sites-enabled/"
    return obj

def restart_nginx():
    obj["run"]=f"echo ${pass} | sudo systemctl restart nginx"
    return obj

def check_nginx():
    obj["run"]=f"echo ${pass} | ngnix -t"
    return obj
"""==================================================================================================="""


commands:Dict = {
    "cpDefault":copy_nginx_conf,
    "restart":restart_nginx,
    "enable": enable_file
    "check" : check_nginx
}
