
def clone(url,name):
    obj = {}
    obj["run"]=f"git clone {url} {name}"
    return obj

def mkdir(name):
    obj = {}
    obj["run"]=f"mkdir -p {name}"
    return obj

def touch(name):
    obj={}
    obj["run"]=f"touch {name}"
    return obj

commands ={
    "mkdir":mkdir,
    "clone":clone,
    "touch":touch
}