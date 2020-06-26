from nornir import InitNornir
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command, netmiko_send_config
from nornir.core.filter import F


def lb_text(lb_task):
    lb_task.run(task = netmiko_send_config , config_file = "test_conf")
    lb_task.run(task = netmiko_send_command , command_string = 'show ip interface brief')

nr = InitNornir(config_file="config.yaml", dry_run=True)

eos_host = nr.filter(F(groups__contains='ios_switches') |
                        F(groups__contains='ios_routers'))

results = nr.run(task = lb_text)

print_result(results)
