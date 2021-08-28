import subprocess
import time



def cb(err,name):
    if err:
        print(f"Error in {name}\n")
        raise Exception("Some error occured")
    
    print(f"Success in {name}\n")


def run_command(command,commandname,cb,fallback):
    command_sh= command["run"]
    print(f"Running {command_sh} {commandname}\n")
    process = subprocess.Popen(command_sh, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    t_end = time.time() + 100
    while time.time() < t_end:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode('utf-8').strip(),"\n")
    rc = process.poll()
    if(rc is not None and rc==0):
        if "revert" in command.keys():
            fallback.append({
                'command':{
                    'run':command["revert"],
                },
                'name': f'{commandname} revert'
            })
        return cb(None,commandname)
    else:
        return cb(True,commandname)


def run_multiple(commands,blockname,callback,fallback=[]):
    for obj in commands:
        run_command(obj['command'],obj['name'],callback,fallback)