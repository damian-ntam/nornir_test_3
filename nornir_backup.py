from nornir import InitNornir
from nornir.plugins.tasks import networking 
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from datetime import date
import pathlib

def backup_config(backup_task):
    config_dir = "config-archive"
    device_dir = config_dir + "/" + backup_task.host.name
    pathlib.Path(config_dir).mkdir(exist_ok = True)
    pathlib.Path(device_dir).mkdir(exist_ok= True)
    r = backup_task.run( task = networking.napalm_get ,
                         getters = ["config"]) 
    backup_task.run(
            task = write_file , 
            content = r.result["config"]["running"] , 
            filename = f"" + str(device_dir) + "/" + str(date.today()) + ".txt"           
    )

def main():
    nr = InitNornir(config_file = "config.yaml")
    result = nr.run(name = "Creating Backup Archive", task = backup_config)
    print_result(result)

if __name__ == "__main__":
    main() 