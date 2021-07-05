
def clone(url,name):
    obj = {}
    obj["run"]=f"git clone ${url} ${name}"
    return obj

def mkdir(name):
    obj = {}
    obj["run"]=f"mkdir {name}"
    return obj

commands ={
    "mkdir":mkdir,
    "clone":clone
}