def clone(url,name):
    obj["run"]=f"git clone ${url} ${name}"
    return obj

def changeinfile(old,new,file,seperator="/"):
    obj["run"]= f"echo ${pass} | sudo -S sed -i 's${separator}${old}${separator}${new_entry}${separator}g' ${file}"
    return obj

def mkdir(name):
    obj["run"]=f"mkdir {name}"
    return obj

commands ={
    "mkdir":mkdir,
    "changeinfile":changeinfile,
    "clone":clone
}