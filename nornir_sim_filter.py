from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.core.filter import F

nr = InitNornir(config_file = 'config.yaml' , dry_run = True)

def lb_function(lb_task):
    lb_task.run(netmiko_send_config , config_file = 'test_conf_filter' )
    lb_task.run(netmiko_send_command , command_string = 'show banner motd')

eos_host = nr.filter(F(groups__contains='ios_switches') |
                        F(groups__contains='ios_routers'))

targets = eos_host.filter(country = 'usa')
results = targets.run(task = lb_function)

print_result(results)