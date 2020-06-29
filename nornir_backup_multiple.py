from nornir import InitNornir
from nornir.plugins.tasks import networking 
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.files import write_file
from datetime import date
import pathlib

def telemetry_get(telemetry_task):
    commands = ['show cdp neighbors' , 'show ip interfaces' , 'show ip route']
    for command in commands:
        telemetry_dir = "telemetry-archive"
        device_dir = telemetry_dir + "/" + telemetry_task.host.name
        pathlib.Path(telemetry_dir).mkdir(exist_ok = True)
        pathlib.Path(device_dir).mkdir(exist_ok= True)
        date_dir = device_dir +  '/' + str(date.today())
        pathlib.Path(date_dir).mkdir(exist_ok = True)
        r = telemetry_task.run( task = networking.netmiko_send_command ,
                             command_string = command
                         )                         
        telemetry_task.run(
                task = write_file , 
                content = r.result , 
                filename = f"" + str(date_dir) + "/" + str(command) + '_' + str(date.today()) + ".txt"           
    )

def main():
    nr = InitNornir(config_file = "config.yaml")
    result = nr.run(name = "Creating Telemetry Archive", task = telemetry_get)
    print_result(result)

if __name__ == "__main__":
    main() 