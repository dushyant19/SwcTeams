import subprocess

def cb(err,name,data=""):
    if err:
        print(f"Error in {name}\n")
        raise Exception(err)
    print(f"Success in {name}")
    return data


def run_command(command,commandname,cb,fallback):
    command_sh= command["run"]
    print(f"Running {command_sh} {commandname}")
    output = subprocess.run(command_sh,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if(output.returncode==0):
        if "revert" in command.keys():
            fallback.append({
                'command':{
                    'run':command["revert"],
                },
                'name': f'{commandname} revert'
            })
        return cb(None,commandname,output.stdout.decode())
    else:
        return cb(output.stderr,commandname)


def run_multiple(commands,blockname,callback,fallback=[]):
    for obj in commands:
        run_command(obj['command'],obj['name'],callback,fallback)