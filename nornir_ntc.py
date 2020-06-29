from nornir import InitNornir
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result, print_title
from nornir.core.filter import F
import ntc_templates



def main():
    nr = InitNornir(config_file = "config.yaml" , dry_run = True , use_textfsm = True)
    results = nr.run(task = netmiko_send_command , command_string = "show ip interface brief")
    print_result(results)


if __name__ == '__main__':
    main()
