from nornir import InitNornir
from nornir.plugins.functions.text import print_result, print_title
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config

def lb_create(lb_task):
    lb_task.run(task = netmiko_send_config, config_commands = 'interface loopback100')
    lb_task.run(task = netmiko_send_command, command_string = 'show ip interface brief')

nr = InitNornir(
    config_file="config.yaml", dry_run=True
)
results = nr.run(task = lb_create)

print_result(results)